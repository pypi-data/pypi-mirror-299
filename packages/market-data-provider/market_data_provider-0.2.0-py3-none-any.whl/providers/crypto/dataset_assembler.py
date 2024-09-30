import json
import os
from collections import deque
from datetime import datetime
from typing import List

from indicators.indicator_abstract import BaseIndicator
from providers.common import load_json, prepare_directory, random_string
from providers.crypto.dataset_timeframe_aggregator import DatasetTimeframeAggregator
from target_selector.dataset_selector_abstract import BaseDatasetSelector


class CryptoSeriesDatasetAssembler:
    def __init__(self,
                 instruments: List[str],
                 aggregation_window_sec: int,
                 dataset_selector: BaseDatasetSelector,
                 dataset_out_folder: str,
                 indicators: List[BaseIndicator] = None):
        self.instruments = instruments
        self.aggregation_window_sec = aggregation_window_sec
        self.indicators: List[BaseIndicator] = indicators
        self.dataset_selector: BaseDatasetSelector = dataset_selector
        self.raw_data_folder = './raw_data_folder'
        self.dataset_out_folder = dataset_out_folder

    def generate_dataset(self):
        selector_window_length = self.dataset_selector.training_window_length + self.dataset_selector.prediction_window_length
        selected_series = []
        for instrument in self.instruments:
            self.dataset_selector.reset()
            [indicator.reset() for indicator in self.indicators]
            selected_window = deque(maxlen=selector_window_length)
            timeframe_aggregator = DatasetTimeframeAggregator(self.aggregation_window_sec)
            aggregated_candles = []
            loaded_candles = 0
            for file in self._filter_and_sort_files(instrument):
                series = load_json(file)
                for candle in series:
                    loaded_candles = loaded_candles + 1
                    aggregated_candle = timeframe_aggregator.aggregate(candle)
                    if aggregated_candle:
                        aggregated_candles.append(aggregated_candle)
            aggregated_candle = timeframe_aggregator.get_aggregated_tail()
            if aggregated_candle:
                aggregated_candles.append(aggregated_candle)
            print(
                f'Instrument: {instrument}, loaded candles: {loaded_candles}, aggregated candles: {len(aggregated_candles)}')

            for i, candle in enumerate(aggregated_candles):
                for indicator in self.indicators:
                    indicator_value = indicator.apply(candle)
                    candle[indicator.get_name()] = indicator_value

            aggregated_candles = [candle for candle in aggregated_candles if
                                  all(value is not None for value in candle.values())]
            aggregated_candles = sorted(aggregated_candles, key=lambda x: x['t'])

            indicator_names = [indicator.get_name() for indicator in self.indicators]
            print(f"Instrument: {instrument}, indicators applied: {', '.join(indicator_names)}")

            for candle in aggregated_candles:
                selected_window.append(candle)
                if self.dataset_selector.apply(candle):
                    selected_series.append({instrument: list(selected_window)})

            print(f'{instrument}: {len(selected_series)} examples assembled')

        unique_name = random_string()
        out_folder = os.path.join(self.dataset_out_folder, unique_name)
        prepare_directory(out_folder)

        for series in selected_series:
            for instrument, data in series.items():
                timestamp = data[0]['t']
                filename = f"{instrument}_{timestamp}.json"
                filepath = os.path.join(out_folder, filename)

                with open(filepath, 'w') as f:
                    json.dump(data, f, indent=1)

        config = self._generate_dataset_config_file()
        config_path = os.path.join(self.dataset_out_folder, f'{unique_name}_dataset_config.json')
        with open(config_path, 'w') as config_file:
            json.dump(config, config_file, indent=1)

        print(f"Config saved at: {config_path}")

    def _generate_dataset_config_file(self):
        config = {
            "instruments": self.instruments,
            "aggregation_window_sec": self.aggregation_window_sec,
            "selector_name": self.dataset_selector.get_name(),
            "selector_training_window_size_length": self.dataset_selector.training_window_length,
            "selector_prediction_window_size_length": self.dataset_selector.prediction_window_length,
            "indicators": [
                {
                    "name": indicator.get_name(),
                    "window_length": indicator.window_length
                } for indicator in self.indicators
            ]
        }
        return config

    def _filter_and_sort_files(self, instrument):
        all_files = os.listdir(self.raw_data_folder)
        instrument_files = [f for f in all_files if f.startswith(instrument)]
        instrument_files.sort(key=lambda x: datetime.strptime(x.split('_')[1].split('.')[0], '%Y-%m-%d'))
        return [os.path.join(self.raw_data_folder, f) for f in instrument_files]
