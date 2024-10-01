import datetime
import os
from datetime import datetime, timezone
from typing import Dict, List

import requests
from requests.exceptions import ConnectionError, Timeout, HTTPError, RequestException
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type


class CryptoOhlcLoader:
    def __init__(self, selected_date: datetime, instrument: str, interval: int, interval_type: str = 'second'):
        self.api_token = os.getenv('POLYGON_API_TOKEN')
        if not self.api_token:
            raise EnvironmentError(
                "POLYGON_API_TOKEN is required to access the API. Please set the environment variable.")
        self.selected_date = selected_date
        self.instrument = instrument
        self.interval = interval
        self.interval_type = interval_type

    @retry(stop=stop_after_attempt(15), wait=wait_fixed(10),
           retry=retry_if_exception_type((ConnectionError, Timeout, HTTPError, RequestException)))
    def _download_ohlc_series(self, start_timestamp: int, end_timestamp: int) -> Dict:
        url = (
            f"https://api.polygon.io/v2/aggs/ticker/X:{self.instrument}USD/range/{self.interval}/{self.interval_type}/"
            f"{start_timestamp}/{end_timestamp}?adjusted=true&sort=asc&limit=50000&apiKey={self.api_token}")
        response = requests.get(url)
        response.raise_for_status()
        results = response.json().get('results', [])
        if results:
            first_timestamp = results[0]['t']
            last_timestamp = results[-1]['t']
            start_time = datetime.utcfromtimestamp(first_timestamp / 1000.0).strftime('%Y-%m-%d %H:%M:%S')
            end_time = datetime.utcfromtimestamp(last_timestamp / 1000.0).strftime('%Y-%m-%d %H:%M:%S')

            print(f'Loaded from {start_time} to {end_time} UTC, size {len(results)}')
        return results

    def _map_ohlc_series(self, ohlc_series) -> List[Dict[str, any]]:
        return [
            {
                'datetime': datetime.utcfromtimestamp(point['t'] / 1000.0).strftime("%Y-%m-%d %H:%M:%S"),
                't': point['t'],
                'o': point['o'],
                'h': point['h'],
                'l': point['l'],
                'c': point['c'],
                'v': point['v'],
                **({'n': point['n']} if 'n' in point else {})
            }
            for point in ohlc_series
        ]

    def get_ohlc_series(self) -> List[Dict[str, any]]:
        print(f'OHLC: {self.instrument} {self.selected_date.strftime("%Y-%m-%d")}')
        ohlc_series = []
        for hour in range(0, 24, 6):
            start_timestamp = int(self.selected_date.replace(hour=hour, minute=0, second=0, microsecond=0,
                                                             tzinfo=timezone.utc).timestamp() * 1000)
            end_timestamp = int(self.selected_date.replace(hour=hour + 5, minute=59, second=59, microsecond=999999,
                                                           tzinfo=timezone.utc).timestamp() * 1000)
            ohlc_series += self._download_ohlc_series(start_timestamp, end_timestamp)

        ohlc_series = self._map_ohlc_series(ohlc_series)
        return ohlc_series
