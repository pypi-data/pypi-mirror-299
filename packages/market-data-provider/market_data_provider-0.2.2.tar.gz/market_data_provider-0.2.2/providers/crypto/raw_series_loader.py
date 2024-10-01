import json
import os
from datetime import datetime
from typing import List

from providers.common import generate_date_range, prepare_directory
from .ohlc_loader import CryptoOhlcLoader
from .trades_loader import CryptoTradesLoader


class CryptoRawSeriesDataLoader:
    def __init__(self, instruments: List[str], day_from: datetime, day_to: datetime,
                 interval_sec: int = 60):
        self.interval_sec = interval_sec
        self.selected_days = generate_date_range(day_from, day_to)
        self.instruments = instruments
        self.raw_data_folder = './raw_data_folder'
        prepare_directory(self.raw_data_folder)

    def load_raw_series(self) -> None:
        for instrument in self.instruments:
            for target_day in self.selected_days:
                ohlc_series = CryptoOhlcLoader(target_day, instrument, self.interval_sec).get_ohlc_series()
                grouped_trades = CryptoTradesLoader(target_day, instrument, self.interval_sec).get_grouped_trades()

                updated_series = self._update_ohlc_with_trades(ohlc_series, grouped_trades)

                file_name = f"{instrument}_{target_day.strftime('%Y-%m-%d')}.json"
                file_path = os.path.join(self.raw_data_folder, file_name)

                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(updated_series, f, ensure_ascii=False, indent=4)

    @staticmethod
    def _update_ohlc_with_trades(ohlc_series: List[dict], grouped_trades: dict) -> List[dict]:
        updated_series = []
        ohlc_dict = {candle['t']: candle for candle in ohlc_series}

        for trade_time, trades in grouped_trades.items():
            if trade_time in ohlc_dict:
                candle = ohlc_dict[trade_time]
                candle['trades'] = trades
                if len(trades) != candle['n']:
                    candle_time = datetime.utcfromtimestamp(trade_time / 1000.0).strftime('%Y-%m-%d %H:%M:%S')
                    print(f"Warning: The number of trades for candle at {candle_time} does not match. "
                          f"Expected: {candle['n']}, Found: {len(trades)}")
            else:
                raise ValueError(
                    f"No candle found for trades at {datetime.utcfromtimestamp(trade_time / 1000.0).strftime('%Y-%m-%d %H:%M:%S')}")

            updated_series.append(candle)

        updated_series = sorted(updated_series, key=lambda x: x['t'])

        return updated_series
