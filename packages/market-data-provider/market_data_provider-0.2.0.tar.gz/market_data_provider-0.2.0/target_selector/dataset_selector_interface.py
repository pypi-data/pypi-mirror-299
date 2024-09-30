from abc import ABC, abstractmethod
from typing import Dict


class DatasetSelectorInterface(ABC):
    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def get_training_window_length(self) -> int:
        pass

    @abstractmethod
    def get_prediction_window_length(self) -> int:
        pass

    @abstractmethod
    def apply(self, candle: Dict) -> bool:
        pass

    @abstractmethod
    def reset(self) -> None:
        pass
