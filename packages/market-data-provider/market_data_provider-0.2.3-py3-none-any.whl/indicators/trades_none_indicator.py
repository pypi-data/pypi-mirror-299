from indicators.indicator_abstract import BaseIndicator


class TradesNoneIndicator(BaseIndicator):
    def get_name(self) -> str:
        return "trades"

    def calculate_value(self) -> float:
        return 0