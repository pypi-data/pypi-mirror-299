from abc import ABC, abstractmethod
from typing import Dict, List


class BaseDatasetSelector(ABC):
    def __init__(self, training_window_length: int, prediction_window_length: int):
        self.training_window_length = training_window_length
        self.prediction_window_length = prediction_window_length
        self.window_size = training_window_length + prediction_window_length
        self.candles: List[Dict] = []

    def apply(self, candle: Dict) -> bool:
        self.candles.append(candle)

        if len(self.candles) < self.window_size:
            return False

        result = self.process_window(self.candles[:self.training_window_length],
                                     self.candles[self.training_window_length:])
        self.candles.pop(0)
        return result

    @abstractmethod
    def process_window(self, training_window: List[Dict], prediction_window: List[Dict]) -> bool:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass

    def reset(self) -> None:
        self.candles = []
