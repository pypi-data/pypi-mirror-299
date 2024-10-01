from datetime import datetime, timedelta


class DatasetTimeframeAggregator:
    def __init__(self, aggregation_window_sec):
        self.aggregation_window_sec = aggregation_window_sec
        self.current_window_candles = []
        self.start_time = None

    @staticmethod
    def _parse_datetime(timestamp_ms):
        return datetime.utcfromtimestamp(timestamp_ms / 1000)

    def _aggregate_candles(self):
        open_price = self.current_window_candles[0]['o']
        close_price = self.current_window_candles[-1]['c']
        high_price = max(candle['h'] for candle in self.current_window_candles)
        low_price = min(candle['l'] for candle in self.current_window_candles)
        volume = sum(candle['v'] for candle in self.current_window_candles)
        total_trades = sum(candle['n'] for candle in self.current_window_candles)

        aggregated_trades = []
        for candle in self.current_window_candles:
            aggregated_trades.extend(candle['trades'])

        aggregated_trades.sort(key=lambda trade: trade['t'])

        aggregated_candle = {
            "datetime": self.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "t": int(self.start_time.timestamp() * 1000),
            "o": open_price,
            "h": high_price,
            "l": low_price,
            "c": close_price,
            "v": volume,
            "n": total_trades,
            "trades": aggregated_trades
        }

        if len(aggregated_candle['trades']) != aggregated_candle['n']:
            candle_time = datetime.utcfromtimestamp(aggregated_candle['t'] / 1000.0).strftime('%Y-%m-%d %H:%M:%S')
            print(f"Warning: The number of trades for candle at {candle_time} does not match. "
                  f"Expected: {aggregated_candle['n']}, Found: {len(aggregated_candle['trades'])}")

        return aggregated_candle

    def aggregate(self, new_candle):
        candle_time = self._parse_datetime(new_candle["t"])

        if self.start_time is None:
            self.start_time = candle_time.replace(hour=0, minute=0, second=0, microsecond=0)
            self.current_window_candles.append(new_candle)
            return None

        window_end_time = self.start_time + timedelta(seconds=self.aggregation_window_sec)
        aggregated_candle = None
        while candle_time > window_end_time:
            if self.current_window_candles:
                aggregated_candle = self._aggregate_candles()
                self.current_window_candles = []
            self.start_time = window_end_time
            window_end_time = self.start_time + timedelta(seconds=self.aggregation_window_sec)

        self.current_window_candles.append(new_candle)

        return aggregated_candle

    def get_aggregated_tail(self):
        if self.current_window_candles:
            aggregated_candle = self._aggregate_candles()
            self.current_window_candles = []

            return aggregated_candle
