import datetime
import os
from bisect import bisect_right
from datetime import datetime, timedelta, timezone
from typing import Dict, List

import requests
from requests.exceptions import ConnectionError, Timeout, HTTPError, RequestException
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type

from providers.crypto.exchanges import CryptoExchanges


class CryptoTradesLoader:
    def __init__(self, selected_date: datetime, instrument: str, exchanges: [CryptoExchanges] = None):
        self.api_token = os.getenv('POLYGON_API_TOKEN')
        if not self.api_token:
            raise EnvironmentError(
                "POLYGON_API_TOKEN is required to access the API. Please set the environment variable.")
        self.selected_date = selected_date
        self.instrument = instrument
        self.exchanges = exchanges

    @staticmethod
    def _map_trades(trades_data) -> List[Dict[str, str]]:
        return [
            {
                'datetime': datetime.utcfromtimestamp(trade['participant_timestamp'] / 1e9).strftime(
                    "%Y-%m-%d %H:%M:%S"),
                't': trade['participant_timestamp'],
                'p': trade['price'],
                's': trade['size'],
                'c': "s" if 1 in trade['conditions'] else "b" if 2 in trade['conditions'] else "unknown"
            }
            for trade in trades_data
        ]

    @retry(stop=stop_after_attempt(15), wait=wait_fixed(10),
           retry=retry_if_exception_type((ConnectionError, Timeout, HTTPError, RequestException)))
    def _download_trades(self):
        formatted_date = self.selected_date.strftime("%Y-%m-%d")
        url = f"https://api.polygon.io/v3/trades/X:{self.instrument}USD"
        params = {
            "timestamp": formatted_date,
            "limit": 50000,
            "apiKey": self.api_token
        }

        trades_data = []
        while url:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            trades_data.extend(data.get('results', []))
            url = data.get('next_url', None)
            params = {
                "apiKey": self.api_token
            }

        trades_data = sorted(trades_data, key=lambda x: x['participant_timestamp'])

        if trades_data:
            start_time_ns = trades_data[0]['participant_timestamp']
            end_time_ns = trades_data[-1]['participant_timestamp']

            start_time = datetime.utcfromtimestamp(start_time_ns / 1_000_000_000).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            end_time = datetime.utcfromtimestamp(end_time_ns / 1_000_000_000).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

            print(f"Total trades loaded from {start_time} to {end_time}, size {len(trades_data)}")

        return trades_data

    def _get_trades(self) -> List[Dict[str, any]]:
        trades = self._download_trades()
        if self.exchanges:
            selected_exchange_ids = [exchange.value for exchange in self.exchanges]
            trades = [trade for trade in trades if trade['exchange'] in selected_exchange_ids]
            print(f"Going to use  {self.exchanges}, filtered trades size {len(trades)}")

        trades = self._map_trades(trades)
        trades = sorted(trades, key=lambda x: x['t'])

        return trades

    def get_grouped_trades(self):
        interval_length = 1000
        start_datetime = self.selected_date.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=timezone.utc)
        end_datetime = start_datetime + timedelta(days=1)
        start_time = int(start_datetime.timestamp() * 1000)
        end_time = int(end_datetime.timestamp() * 1000)
        intervals = list(range(start_time, end_time, interval_length))
        grouped_trades = {start: [] for start in intervals}
        trades = self._get_trades()

        for trade in trades:
            trade_time_ms = trade['t'] // 1_000_000
            idx = bisect_right(intervals, trade_time_ms) - 1
            grouped_trades[intervals[idx]].append(trade)

        grouped_trades = {k: v for k, v in grouped_trades.items() if v}

        return grouped_trades
