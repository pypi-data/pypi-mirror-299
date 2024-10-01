from typing import Dict, List

from target_selector.dataset_labeler_abstract import BaseDatasetLabeler


class VolatilityDatasetSelector(BaseDatasetLabeler):
    def get_name(self) -> str:
        return "volatility_selector"

    def process_window(self, training_window: List[Dict], prediction_window: List[Dict]) -> bool:
        training_volatility = self._calculate_volatility(training_window)
        prediction_volatility = self._calculate_volatility(prediction_window)

        if prediction_volatility * 2 <= training_volatility:
            return True
        return False

    @staticmethod
    def _calculate_volatility(window: List[Dict]) -> float:
        highs = [candle['h'] for candle in window]
        lows = [candle['l'] for candle in window]
        return max(highs) - min(lows)