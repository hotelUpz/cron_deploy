# import aiohttp
from typing import Dict, Tuple, Callable, Optional
from b_context import BotContext
from c_log import ErrorHandler, log_time
from c_utils import PositionUtils
from d_bapi import BinancePrivateApi



class Average:
    def __init__(
            self,
            context: BotContext,
            error_handler: ErrorHandler,
        ):
        error_handler.wrap_foreign_methods(self)
        self.context = context
        self.error_handler = error_handler

    def avg_control(
        self,
        grid_orders: list,
        avg_progress_counter: int,
        cur_price: float,
        init_price: float,
        normalized_sign: int,
        nPnL_calc: Callable[[float, float, str], float],
        avg_signal: bool,
        debug_label: str,
    ) -> tuple[int, float]:
        """
        Контроль усреднения.
        Возвращает:
            - обновлённый прогресс (int),
            - объём текущего шага (float), либо 0.0 если усреднение не нужно.
        """
        if not grid_orders or not isinstance(grid_orders, list):
            self.error_handler.debug_info_notes(f"{debug_label} Невалидный grid_orders: ожидался список.")
            return avg_progress_counter, 0.0

        if not isinstance(avg_progress_counter, int) or avg_progress_counter < 0:
            self.error_handler.debug_info_notes(f"{debug_label} Некорректный avg_progress_counter: {avg_progress_counter}")
            return avg_progress_counter, 0.0

        len_grid_orders = len(grid_orders)

        if len_grid_orders <= 1 or avg_progress_counter >= len_grid_orders:
            return avg_progress_counter, 0.0

        step = grid_orders[min(avg_progress_counter, len_grid_orders - 1)]
        indent = -abs(step.get("indent", 0.0))
        volume = step.get("volume", 0.0)

        avg_nPnl = nPnL_calc(cur_price, init_price, debug_label) * normalized_sign

        if avg_nPnl <= indent:
            new_progress = avg_progress_counter + 1

            # ограничим, чтобы не выйти за пределы
            grid_index = min(new_progress, len_grid_orders-1)
            open_by_signal = grid_orders[grid_index].get("signal", False)

            if not open_by_signal or avg_signal:
                return new_progress, volume

        return avg_progress_counter, 0.0

    def check_avg_and_report(
        self,
        cur_price: float,
        symbol_data: dict,
        nPnL_calc: Callable[[float, float, str], float],
        normalized_sign: int,
        avg_signal: bool,
        settings_pos_options: Dict,
        debug_label: str,
    ) -> bool:
        """Проверяет необходимость усреднения и формирует сигнал."""
        grid_cfg = settings_pos_options["entry_conditions"]["grid_orders"]
        cur_avg_progress = symbol_data.get("avg_progress_counter", 1)
        init_price = symbol_data.get("entry_price", 0.0)

        new_avg_progress, avg_volume = self.avg_control(
            grid_cfg,
            cur_avg_progress,
            cur_price,
            init_price,
            normalized_sign,
            nPnL_calc,
            avg_signal,
            debug_label,
        )

        if new_avg_progress == cur_avg_progress or avg_volume == 0.0:
            return False

        symbol_data["avg_progress_counter"] = new_avg_progress
        symbol_data["process_volume"] = avg_volume / 100

        safe_idx = min(new_avg_progress-1, len(grid_cfg) - 1)
        self.error_handler.trades_info_notes(
            f"[{debug_label}] ➗ Усредняем. "
            f"Счётчик {cur_avg_progress} → {new_avg_progress}. "
            f"Cur vol: {avg_volume} "
            f"Cur price: {cur_price} "
            f"Indent: {grid_cfg[safe_idx]}",
            True,
        )
        return True


class MockErrorHandler:
    def debug_info_notes(self, msg): print("INFO:", msg)
    def trades_info_notes(self, msg, *_): print("TRADE:", msg)
    def debug_error_notes(self, msg, *_): print("ERROR:", msg)
    def wrap_foreign_methods(self, obj): pass


class MockContext:
    pass


class MockPosUtils:
    @staticmethod
    def nPnL_calc(cur_price, init_price, debug_label=""):
        # Пример: (cur/init - 1) * 100 для LONG
        return ((cur_price / init_price) - 1.0) * 100
        # return ((cur_price - init_price) / init_price) * 100


def test_average():
    ctx = MockContext()
    err = MockErrorHandler()
    avg = Average(ctx, err)

    symbol_data = {"entry_price": 100.0, "avg_progress_counter": 1}
    grid_cfg = [
        {'indent': 0.0, 'volume': 1, 'signal': True},
        {'indent': -7.0, 'volume': 2, 'signal': False},
        # {'indent': -14.0, 'volume': 3, 'signal': False},
        # {'indent': -21.0, 'volume': 4, 'signal': False},
        # {'indent': -28.0, 'volume': 5, 'signal': False},
        # {'indent': -35.0, 'volume': 6, 'signal': False},
        # {'indent': -42.0, 'volume': 7, 'signal': False},
    ]

    settings = {"entry_conditions": {"grid_orders": grid_cfg}}

    # Симуляция падения цены
    for cur_price in [98, 95, 90, 85, 80, 75, 70, 65, 55, 54, 53, 52, 51, 53, 60, 90, 45]:
        print(f"\n=== Price {cur_price} ===")
        avg.check_avg_and_report(
            cur_price=cur_price,
            symbol_data=symbol_data,
            nPnL_calc=MockPosUtils.nPnL_calc,
            normalized_sign=1,
            avg_signal=False,
            settings_pos_options=settings,
            debug_label="[TEST][LONG]"
        )
        print("Current progress:", symbol_data["avg_progress_counter"])


if __name__ == "__main__":
    test_average()
