
    # def pnl_report(
    #     self,
    #     avg_price: float,
    #     current_price: float,
    #     position_side: str,
    #     debug_label: str
    # ) -> str:
    #     """
    #     Формирует сообщение о результате закрытия позиции с учетом PnL в процентах.
    #     """
        # try:
        #     if avg_price is None or avg_price == 0.0:
        #         self.error_handler.debug_error_notes(
        #             f"{debug_label} ⚠️ avg_price is None или 0.0 — невозможно рассчитать PnL"
        #         )
        #         return f"⚠️ {debug_label} Ошибка: avg_price некорректен (None или 0.0)"

        #     if position_side == "LONG":
        #         pnl_pct = ((current_price - avg_price) / avg_price) * 100
        #     elif position_side == "SHORT":
        #         pnl_pct = ((avg_price - current_price) / avg_price) * 100
        #     else:
        #         raise ValueError(f"Invalid position_side: {position_side}")

        #     if pnl_pct > 0:
        #         msg = f"🟢 Позиция закрыта в плюс."
        #     elif pnl_pct < 0:
        #         msg = f"🔴 Позиция закрыта в минус."
        #     else:
        #         msg = f"⚪ Позиция закрыта без изменения (0.00%)"

        #     self.error_handler.trades_info_notes(
        #         f"{debug_label}: {msg}",
        #         True
        #     )
        #     return msg

        # except Exception as ex:
        #     self.error_handler.debug_error_notes(f"{debug_label} ⚠️ {ex} in pnl_report")
        #     return f"⚠️ {debug_label} Ошибка при расчёте PnL"


        # self.error_handler.debug_info_notes(
        #     f"{debug_label}: take_profit={take_profit}, nPnl={signed_nPnl}, cur_price={cur_price}, avg_price={avg_price}"
        # )


        # self.error_handler.debug_info_notes(
        #     f"[{strategy_name}][{symbol}][{position_side}]: stop_loss={stop_loss}, nPnl={nPnl}, cur_price={cur_price}, avg_price={avg_price}"
        # )


        # self.error_handler.debug_info_notes(
        #     f"{debug_label}[CLOSE_SIGNAL] Условие выполнено: close_by_signal=True, close_signal=True, PnL={cur_nPnl:.4f}"
        # )


        # self.error_handler.debug_info_notes(
        #     f"{debug_label} Усреднение активировано: indent достигнут, volume={avg_volume}%, new_progress={new_avg_progress}"
        # )





        
    # def extract_df(self, symbol):
    #     return self.context.klines_data_cache.get(symbol, pd.DataFrame(columns=self.default_columns))



        
    # def get_signal(
    #         self,  
    #         user_name,
    #         strategy_name,          
    #         symbol,
    #         position_side,
    #         ind_suffics,
    #         long_count: dict,
    #         short_count: dict
    #     ):
    
    #     # print("get_signal")
    #     open_signal, avg_signal, close_signal = False, False, False
    #     try:
    #         # Удобные сокращения
    #         user_settings = self.context.total_settings[user_name]["core"]
    #         strategy_settings = self.context.strategy_notes[strategy_name][position_side]
    #         entry_conditions = strategy_settings.get("entry_conditions", {})
    #         signal_on = entry_conditions.get("grid_orders")[0].get("signal")

    #         symbol_pos_data = self.context.position_vars[user_name][strategy_name][symbol][position_side]
    #         in_position = symbol_pos_data.get("in_position", False)

    #         # Настройки сигналов
    #         gen_signal_func_name = extract_signal_func_name(strategy_name)
    #         entry_rules = entry_conditions.get("rules", {})
    #         is_close_bar = entry_conditions.get("is_close_bar", False)

    #         # Получаем данные
    #         origin_df = self.extract_df(symbol)
            
    #         if not signal_on:
    #             open_signal = True
    #             return

    #         result_df = self.build_indicators_df(origin_df, entry_rules, ind_suffics)
    #         # print(f"result_df: {result_df}")

    #         signal_func = getattr(self, gen_signal_func_name + "_colab", None)
    #         if not callable(signal_func):
    #             self.signals_debug("❌ Signal function not found", symbol)
    #             return

    #         result = signal_func(result_df, symbol, is_close_bar, ind_suffics, entry_rules)
    #         if isinstance(result, (tuple, list)) and len(result) == 2:
    #             long_signal, short_signal = result

    #             open_signal, avg_signal, close_signal = self.signal_interpreter(
    #                 long_signal,
    #                 short_signal,
    #                 in_position,
    #                 position_side,
    #                 long_count[user_name],
    #                 short_count[user_name],
    #                 user_settings.get("long_positions_limit", float("inf")),
    #                 user_settings.get("short_positions_limit", float("inf"))
    #             )

    #     except Exception as e:
    #         tb = traceback.format_exc()
    #         self.signals_debug(
    #             f"❌ Signal function error for [{user_name}][{strategy_name}][{symbol}][{position_side}]: {e}\n{tb}",
    #             symbol
    #         )
    #     finally:
    #         if open_signal:
    #             if position_side == "LONG":
    #                 long_count[user_name] += 1
    #             elif position_side == "SHORT":
    #                 short_count[user_name] += 1
    #         return open_signal, avg_signal, close_signal
        


        
        
    # def get_signal(self, entry_conditions, in_position, symbol, position_side, gen_signal_func_name, ind_suffics):
    #     open_signal, close_signal = False, False
    #     entry_rules = entry_conditions.get("rules", {})
    #     is_close_bar = entry_conditions.get("is_close_bar", False)
    #     min_tfr = self.ukik_suffics_data["min_tfr"]
    #     origin_df = self.extract_df(symbol, min_tfr)

    #     # Кэшируем process_df по tfr, чтобы не грузить по нескольку раз
    #     tfr_cache = {}

    #     for ind_marker, ind_rules in entry_rules.items():
    #         ind_name_raw = ind_rules.get("ind_name")
    #         if not ind_name_raw:
    #             continue

    #         ind_name = ind_name_raw.strip().lower()
    #         calc_ind_func = getattr(self, f"{ind_name}_calc", None)
    #         if not calc_ind_func:
    #             if self.is_debug:
    #                 print(f"Indicator function not found: {ind_name} (Symbol: {symbol})")
    #             continue

    #         tfr = ind_rules.get("tfr")
    #         if tfr not in tfr_cache:
    #             tfr_cache[tfr] = self.extract_df(symbol, tfr)
    #         process_df = tfr_cache[tfr]

    #         new_ind_column = calc_ind_func(process_df, ind_rules)  # только свои правила, а не всё entry_rules

    #         if isinstance(new_ind_column, pd.Series):
    #             unik_column_name = f"{ind_marker.strip()}_{ind_suffics}"
    #             origin_df[unik_column_name] = new_ind_column.reindex(origin_df.index).ffill()
    #             # origin_df[unik_column_name] = new_ind_column.reindex(origin_df.index).ffill().infer_objects(copy=False)

    #         else:
    #             if self.is_debug:
    #                 print(f"Invalid indicator output (not Series). Symbol: {symbol}")
    #         # print(f"[{symbol}] {ind_name}: HVH column type: {type(new_ind_column)}, len: {len(new_ind_column)}")
    #         # print(f"[{symbol}] Index match: {origin_df.index[-1]} vs {new_ind_column.index[-1]}")

    #     del tfr_cache  # на всякий случай, освободим память
    #     # if symbol == "ETHUSDT":
    #     #     print(origin_df.tail(5))
        
    #     signal_function = getattr(self, gen_signal_func_name, None)
        
    #     if signal_function and self.is_valid_dataframe(origin_df):
    #         try:
    #             signal_repl = signal_function(origin_df, symbol, is_close_bar, ind_suffics, entry_rules)
    #             if signal_repl:
    #                 long_signal, short_signal = signal_repl
    #                 # print(long_signal, short_signal)
    #                 open_signal, close_signal = self.signal_interpreter(long_signal, short_signal, in_position, position_side)
    #                 # print(open_signal, close_signal)
    #         except Exception as e:
    #             if self.is_debug:
    #                 print(f"Signal function error: {e} (Symbol: {symbol})")
    #     else:
    #         if self.is_debug:
    #             print(f"Signal function not found or invalid dataframe. Symbol: {symbol}")

    #     return open_signal, close_signal

            
    # def build_indicators_df(self, origin_df, entry_rules, ind_suffics):
    #     """
    #     Строит итоговый DataFrame со всеми индикаторами.
    #     Возвращает: result_df, required_columns
    #     """
    #     tfr_cache = {}
    #     ind_columns = []
    #     required_columns = []

    #     # ✅ Правильная защита от пустого DataFrame
    #     if origin_df is None or origin_df.empty:
    #         return pd.DataFrame(columns=self.default_columns)

    #     for ind_marker, ind_rules in entry_rules.items():
    #         ind_name = (ind_rules.get("ind_name") or "").strip().lower()
    #         if not ind_name:
    #             continue

    #         calc_func = getattr(self, f"{ind_name}_calc", None)
    #         if not callable(calc_func):
    #             self.signals_debug(f"❌ Indicator function not found: {ind_name}")
    #             continue

    #         tfr = ind_rules.get("tfr")
    #         if tfr not in tfr_cache:
    #             try:
    #                 # ⚠️ здесь должна быть уверенность, что origin_df с DatetimeIndex
    #                 tfr_cache[tfr] = aggregate_candles(origin_df, tfr)
    #             except Exception as e:
    #                 self.signals_debug(f"❌ Error aggregating candles: {e}", ind_name)
    #                 continue

    #         try:
    #             series = calc_func(tfr_cache[tfr], ind_rules)
    #             if series is None or not isinstance(series, pd.Series):
    #                 raise ValueError("Indicator calculation returned None or non-Series")
    #             col_name = f"{ind_marker}_{ind_suffics}"
    #             required_columns.append(col_name)
    #             ind_columns.append(series.rename(col_name))
    #         except Exception as e:
    #             self.signals_debug(f"❌ Error in indicator calculation: {e}", ind_name)

    #     if not ind_columns:
    #         return pd.DataFrame(columns=self.default_columns)

    #     indicators_df = pd.concat(ind_columns, axis=1)
    #     result_df = origin_df.join(indicators_df, how='left')

    #     full_cols = ['Open', 'High', 'Low', 'Close', 'Volume'] + required_columns
    #     result_df = result_df[full_cols].ffill().dropna()

    #     return result_df

                  
    # ## UNIVERSAL FOR BT:
    # def volf_calc(self, df: pd.DataFrame, ind_rules: dict) -> pd.Series:
    #     try:
    #         name = "VOLF"
    #         signals = pd.Series(False, index=df.index, name=name, dtype=bool)

    #         if 'Volume' not in df.columns:
    #             self.debug_error_notes("Отсутствует колонка 'Volume'.")
    #             return signals

    #         period = ind_rules.get('period')
    #         mode = ind_rules.get('mode')
    #         if not isinstance(period, int) or period <= 0:
    #             self.error_handler.debug_error_notes(f"Неверный период: {period}")
    #             return signals
    #         if mode not in ('r', 'a'):
    #             self.error_handler.debug_error_notes("Неверный режим расчёта объёма. Допустимы только 'r' или 'a'.")
    #             return signals
    #         if len(df) < period + 1:
    #             self.error_handler.debug_error_notes("Недостаточно данных: len(df) < period + 1.")
    #             return signals

    #         slice_factor = ind_rules.get(mode, {}).get('slice_factor', 1.0)
    #         volume = df['Volume'].abs()

    #         if mode == "r":
    #             # ref_volume = volume.shift(1).rolling(window=period).mean()
    #             # ref_volume = volume.rolling(window=period).mean()
    #             # ref_volume = ta.sma(df['Volume'], length=period)
    #             ref_volume = ta.ema(volume.shift(1), length=period)
    #         else:
    #             ref_volume = volume.shift(1).rolling(window=period).max()

    #         raw_signals = volume > ref_volume * slice_factor
    #         signals.update(raw_signals.fillna(False))  # заполнили NaN = False, и обновили значения

    #         return signals

    #     except Exception as ex:
    #         self.error_handler.debug_error_notes(f"volf_calc ошибка: {ex}")
    #         return pd.Series(False, index=df.index, name="VOLF", dtype=bool)



# class KlineFetcher(WS_STREAMS):
#     def __init__(self) -> None:
#         super().__init__() 

#     def is_valid_dataframe(self, df):
#         return isinstance(df, pd.DataFrame) and not df.empty

#     def extract_df(self, symbol, time_frame):
#         klines_lim = self.ukik_suffics_data.get("klines_lim")
#         suffics = f"_{klines_lim}_{time_frame}"
#         default_df = pd.DataFrame(columns=['Time', 'Open', 'High', 'Low', 'Close', 'Volume'])
#         return self.klines_data_dict.get(f"{symbol}{suffics}", default_df)

#     async def update_klines(self, new_klines, origin_symbol, suffics):
#         symbol = f"{origin_symbol}{suffics}"
#         if symbol not in self.klines_data_dict:          
#             self.klines_data_dict[symbol] = pd.DataFrame(columns=['Time', 'Open', 'High', 'Low', 'Close', 'Volume'])

#         if self.is_valid_dataframe(new_klines):               
#             self.klines_data_dict[symbol] = new_klines
#         else:
#             self.debug_error_notes(f"[update_klines] Невалидные данные для {symbol}.")

#     async def fetch_klines_for_symbols(self, session, symbols, interval, fetch_limit, api_key_list):
#         """
#         Асинхронно получает свечи для списка символов с использованием фиксированного семафора.
#         """
#         MAX_CONCURRENT_REQUESTS = 20  # Жестко заданное ограничение
#         REQUEST_DELAY = 0.1           # 100 мс задержка между запросами

#         semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)

#         async def fetch_kline(symbol):
#             async with semaphore:
#                 try:
#                     await asyncio.sleep(REQUEST_DELAY)
#                     api_key = choice(api_key_list)
#                     return symbol, await self.get_klines(session, symbol, interval, fetch_limit, api_key)
#                 except Exception as e:
#                     self.debug_error_notes(f"Ошибка при получении свечей для {symbol}: {e}")
#                     return symbol, pd.DataFrame(columns=['Time', 'Open', 'High', 'Low', 'Close', 'Volume'])

#         tasks = [fetch_kline(symbol) for symbol in symbols]
#         return await asyncio.gather(*tasks, return_exceptions=False)

#     async def process_timeframe(
#             self, session, time_frame,
#             fetch_symbols,
#             klines_lim, api_key_list
#         ):

#         suffics = f"_{klines_lim}_{time_frame}"
#         klines_result = await self.fetch_klines_for_symbols(
#             session, fetch_symbols, time_frame,
#             klines_lim, api_key_list
#         )
#         for symb, new_klines in klines_result:
#             await self.update_klines(new_klines, symb, suffics)

#     async def total_klines_handler(self, session):
#         # Определение лимита загрузки свечей
#         klines_lim = self.ukik_suffics_data.get("klines_lim")
#         avi_tfr = self.ukik_suffics_data.get("avi_tfr")

#         api_key_list = [settings_val.get("BINANCE_API_PUBLIC_KEY") for _, settings_val in self.father_settings.items()]
        
#         tasks = [self.process_timeframe(
#             session, time_frame,
#             self.fetch_symbols,
#             klines_lim, api_key_list,
#         ) for time_frame in avi_tfr]
#         await asyncio.gather(*tasks)

# class KlinesCacheManager:
#     def __init__(self, context: BotContext, error_handler: ErrorHandler, get_klines: callable):    
#         error_handler.wrap_foreign_methods(self)
#         self.error_handler = error_handler
#         self.context = context
#         self.get_klines = get_klines
#         self.default_columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']

#     def get_klines_scheduler(self, active_symbols, interval_completed):
#         return (
#             (interval_completed and not self.context.first_iter) or 
#             (self.context.first_iter and active_symbols)
#         )

#     async def update_klines(self, new_klines, symbol):
#         if symbol not in self.context.klines_data_cache:
#             self.context.klines_data_cache[symbol] = pd.DataFrame(columns=self.default_columns)

#         if validate_dataframe(new_klines):
#             self.context.klines_data_cache[symbol] = new_klines
#         else:
#             self.error_handler.debug_error_notes(f"[update_klines] Невалидные данные для {symbol}.")

#     async def fetch_klines_for_symbols(self, session, symbols: set, fetch_limit: int, api_key_list: list = None):
#         """
#         Асинхронно получает 1-минутные свечи для списка символов с ограничением количества одновременных запросов.
#         """
#         MAX_CONCURRENT_REQUESTS = 20
#         REQUEST_DELAY = 0.1

#         semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)

#         async def fetch_kline(symbol):
#             async with semaphore:
#                 try:
#                     await asyncio.sleep(REQUEST_DELAY)                    
#                     api_key = choice(api_key_list) if api_key_list else None
                    
#                     return symbol, await self.get_klines(session, symbol, "1m", fetch_limit, api_key)
#                 except Exception as e:
#                     self.error_handler.debug_error_notes(f"Ошибка при получении свечей для {symbol}: {e}")
#                     return symbol, pd.DataFrame(columns=self.default_columns)

#         tasks = [fetch_kline(symbol) for symbol in symbols]
#         return await asyncio.gather(*tasks)

#     async def total_klines_handler(self, session):
#         """
#         Получение и обновление минутных свечей для всех символов.
#         """        
#         klines_result = await self.fetch_klines_for_symbols(
#             session,
#             self.context.fetch_symbols,
#             self.context.klines_lim,
#             self.context.api_key_list
#         )
#         if not klines_result:
#             self.error_handler.debug_error_notes("[ERROR] in total_klines_handler. ")
#             raise

#         for symbol, new_klines in klines_result:
#             await self.update_klines(new_klines, symbol)






                # # Обработка данных по действию
                # if action == "is_opening":
                #     entry_price = validated["price"]
                #     position_data.update({
                #         "entry_price": entry_price,
                #         "avg_price": entry_price,
                #         "comul_qty": validated["qty"],
                #         "in_position": True
                #     })






# import asyncio
# import re
# import pytz
# from a_settings import SETTINGSs

# class Vars(SETTINGSs):
#     """Глобальные переменные и инициализация данных для торговой стратегии."""

#     # Флаги состояния бота
#     first_iter: bool = True    
#     stop_bot: bool = False
#     is_debug: bool = True

#     # Логирование
#     debug_err_list: list = []
#     debug_info_list: list = []

#     trade_secondary_list: list = []
#     trade_info_list: list = []
#     trade_succ_list: list = []
#     trade_failed_list: list = []

#     # Асинхронные механизмы
#     async_lock: asyncio.Lock = asyncio.Lock()
#     ws_async_lock: asyncio.Lock = asyncio.Lock()
#     ws_shutdown_event = asyncio.Event()

#     # Данные о бирже и котировках
#     last_fetch_timestamp: int = 0
#     exchange_data: list = []
#     klines_data_dict: dict = {}
#     symbol_position_data: dict = {}
#     temporary_signal_data: dict = {}

#     # Управление процессами торговли
#     fetch_symbols: set = set()
#     symbol_info: list = []
#     last_trade_suffics: str = ""
#     interval_seconds: int = 0
#     closing_cache: dict = {}

#     # WebSocket-потоки
#     ws_task = None  
#     is_ws_now = False  
#     cur_price_data: dict = {}  
#     max_wb_reconnect_attempts: int = 5  
#     try_to_wb_connect_counter: int = 0  
#     last_symbol_progress: int = 0   
        
#     # Данные по стратегиям
#     position_vars: dict = {} 
#     ukik_suffics_data: dict = {}

#     @staticmethod
#     def _extract_all_periods(rules):
#         """Извлекает все значения period, period1, period2 и т.д. из правил стратегии."""        
#         periods = []

#         for val in rules:
#             for key, v in val.items():
#                 if re.fullmatch(r"period\d*", key, re.IGNORECASE):
#                     try:
#                         period = int(v)
#                         if period > 0:
#                             periods.append(period)
#                     except (ValueError, TypeError):
#                         continue
#         return periods

#     def __init__(self) -> None:
#         """Инициализация переменных, конфигураций и торговых стратегий."""
#         super().__init__()

#         # Отфильтровываем только активные стратегии
#         self.father_settings = {k: v for k, v in self.father_settings.items() if v.get("is_active")}
#         if not self.father_settings:
#             print("father_settings пуст, нечего инициализировать. Бот завершил работу.")
#             self.stop_bot = True
#             return

#         # Формируем символы с quote_asset
#         for name, settings in self.father_settings.items():
#             note = self.strategy_notes.get(name, {})
#             quote_asset = note.get("core", {}).get("quote_asset", "USDT").strip() or "USDT"
#             symbols = settings.get("symbols", [])
#             self.father_settings[name]["symbols"] = [s.strip() + quote_asset for s in symbols]

#         strategy_list = list(self.father_settings)
#         tfr_map = {"1m": 60, "5m": 300, "15m": 900, "30m": 1800, "1h": 3600, "4h": 14400, "1d": 86400}
#         # 

#         avi_tfr = set()
#         klines_lim = []

#         for direct in ("LONG", "SHORT"):
#             rules = [
#                 val
#                 for strategy in strategy_list
#                 for val in self.strategy_notes.get(strategy, {})
#                                             .get(direct, {})
#                                             .get("entry_conditions", {})
#                                             .get("rules", {})
#                                             .values()
#             ]

#             avi_tfr.update(val["tfr"] for val in rules if "tfr" in val)
#             # periods = [val.get("period", 0) for val in rules]
#             # ...
#             periods = self._extract_all_periods(rules)
#             klines_lim.append(int(max(periods) * 5) if periods else 0)

#         min_tfr_key = min(avi_tfr, key=lambda tfr: tfr_map.get(tfr, float("inf")))

#         self.ukik_suffics_data = {
#             "avi_tfr": list(avi_tfr),
#             "min_tfr": min_tfr_key,
#             "klines_lim": max(klines_lim),
#         }
#         self.inspection_interval: str = "1m"

#         # utils config 
#         self.MAX_LOG_LINES: int = self.utils_config.get("MAX_LOG_LINES")
#         self.is_bible_quotes_introduction: bool = self.utils_config.get("is_bible_quotes")
#         self.tz_location = pytz.timezone(self.utils_config.get("tz_location_str"))




# class WebSocketManager:
#     """Менеджер WebSocket-соединения для получения рыночных данных с Binance."""

#     def __init__(self, context: BotContext, error_handler: ErrorHandler, ws_url: str = "wss://fstream.binance.com/"):
#         error_handler.wrap_foreign_methods(self)
#         self.error_handler = error_handler
#         self.context = context

#         self.ws_task: Optional[asyncio.Task] = None
#         self.is_connected: bool = False        
#         self.max_reconnect_attempts: int = 51
#         self.reconnect_attempts: int = 0
#         self.ws_shutdown_event: asyncio.Event = asyncio.Event()
#         self.WEBSOCKET_URL: str = ws_url
#         self.last_symbol_progress = 0

#     async def handle_ws_message(self, message: str) -> None:
#         try:
#             msg = json.loads(message).get("data")
#             if not msg or msg.get("e") != "kline":
#                 return

#             symbol = msg["s"]
#             kline = msg["k"]
#             self.context.ws_price_data[symbol] = {
#                 "close": float(kline["c"]),
#             }
#         except Exception as e:
#             self.error_handler.debug_error_notes(f"[WS Handle] Error: {e}, Traceback: {traceback.format_exc()}")

#     async def keepalive_ping(self, websocket):
#         """Отправляет ping и ожидает pong, чтобы гарантировать живое соединение."""
#         while not self.ws_shutdown_event.is_set():
#             try:
#                 pong_waiter = await websocket.ping()
#                 await asyncio.wait_for(pong_waiter, timeout=10)  # ждем pong максимум 5с
#                 await asyncio.sleep(15)  # интервал между пингами
#             except asyncio.TimeoutError:
#                 # self.error_handler.debug_error_notes("[Ping] Pong не получен в течение 5 секунд — разрыв соединения")
#                 break
#             except Exception as e:
#                 self.error_handler.debug_error_notes(f"[Ping] Error: {e}")
#                 break

#     async def connect_and_handle(self, symbols: List[str]) -> None:
#         if not symbols:
#             self.error_handler.debug_error_notes("Empty symbols list provided")
#             return

#         streams = [f"{symbol.lower()}@kline_1m" for symbol in symbols]
#         url = f"{self.WEBSOCKET_URL}stream?streams={'/'.join(streams)}"

#         while self.reconnect_attempts < self.max_reconnect_attempts:
#             if self.ws_shutdown_event.is_set():
#                 break

#             try:
#                 async with websockets.connect(
#                     url,
#                     ping_interval=None,
#                     ping_timeout=None,
#                     close_timeout=5,
#                     max_queue=100
#                 ) as websocket:
#                     self.is_connected = True
#                     self.reconnect_attempts = 0
#                     ping_task = asyncio.create_task(self.keepalive_ping(websocket))

#                     try:
#                         async for message in websocket:
#                             if self.ws_shutdown_event.is_set():
#                                 await websocket.close(code=1000, reason="Shutdown")
#                                 break
#                             await self.handle_ws_message(message)
#                     finally:
#                         ping_task.cancel()
#                         with contextlib.suppress(asyncio.CancelledError):
#                             await ping_task

#             except (ConnectionClosedError, ConnectionClosedOK) as e:
#                 self.error_handler.debug_error_notes(
#                     f"[WS Closed] Connection closed: {e}, attempt {self.reconnect_attempts + 1}/{self.max_reconnect_attempts}"
#                 )
#             except TimeoutError as e:
#                 self.error_handler.debug_error_notes(
#                     f"[WS Timeout] Не удалось подключиться: {e}, попытка {self.reconnect_attempts + 1}/{self.max_reconnect_attempts}"
#                 )                
#             except Exception as e:
#                 self.error_handler.debug_error_notes(f"[WS Error] {e}, Traceback: {traceback.format_exc()}")

#             self.reconnect_attempts += 1
#             backoff = min(2 * self.reconnect_attempts, 10)
#             await asyncio.sleep(backoff)

#         self.is_connected = False
#         self.error_handler.debug_error_notes("Max reconnect attempts reached, WebSocket stopped")

#     async def connect_to_websocket(self, symbols: List[str]) -> None:
#         try:
#             await self.stop_ws_process()
#             self.ws_shutdown_event.clear()
#             self.reconnect_attempts = 0
#             self.ws_task = asyncio.create_task(self.connect_and_handle(symbols))
#         except Exception as e:
#             self.error_handler.debug_error_notes(f"[WS Connect] Failed to start WebSocket: {e}, Traceback: {traceback.format_exc()}")
#             return
        
#     async def restart_ws(self):
#         """Перезапускает вебсокет всегда, независимо от количества символов."""
#         try:
#             await self.stop_ws_process()
#             await self.connect_to_websocket(list(self.context.fetch_symbols))
#             self.error_handler.debug_info_notes("[WS] Вебсокет перезапущен")
#         except Exception as e:
#             self.error_handler.debug_error_notes(f"[WS Restart] Ошибка при перезапуске: {e}")

#     async def stop_ws_process(self) -> None:
#         self.ws_shutdown_event.set()
#         if self.ws_task:
#             self.ws_task.cancel()
#             try:
#                 await asyncio.wait_for(self.ws_task, timeout=5.0)
#             except (asyncio.TimeoutError, asyncio.CancelledError):
#                 self.error_handler.debug_info_notes("WebSocket task cancelled or timed out")
#             finally:
#                 self.ws_task = None
#                 self.is_connected = False
#                 self.error_handler.debug_info_notes("WebSocket process stopped")

#     async def sync_ws_streams(self, active_symbols: list) -> None: 
#         """Управляет состоянием WS в зависимости от списка активных символов."""
#         new_symbols_set = set(active_symbols)

#         # если изменился именно набор символов (а не только количество)
#         if new_symbols_set != getattr(self, "last_symbols_set", set()):
#             self.last_symbols_set = new_symbols_set
#             if new_symbols_set:  # есть активные символы
#                 await self.connect_to_websocket(list(new_symbols_set))
#             else:  # символов нет
#                 await self.stop_ws_process()

#     async def reset_existing_prices(self, symbols: Iterable[str]) -> None:
#         async with self.context.ws_async_lock:
#             # self.context.ws_price_data.update({s: {"close": None} for s in symbols if s in self.context.ws_price_data})
#             self.context.ws_price_data.update({s: {"close": None} for s in symbols})



# [Nik][volf_stoch][ALGOUSDT][SHORT]: Invalid input parameters in size_calc Time: 2025-09-24 20:03:08
# Nik_volf_stoch_TRXUSDT_SHORT[Unexpected Error] Failed to update positions for volf_stoch: unsupported operand type(s) for *: 'NoneType' and 'float' Time: 2025-09-24 20:11:25
# Nik_volf_stoch_TRXUSDT_SHORT[Unexpected Error] Failed to update positions for volf_stoch: unsupported operand type(s) for *: 'NoneType' and 'float' Time: 2025-09-24 20:11:27
# Nik_volf_stoch_TRXUSDT_SHORT[Unexpected Error] Failed to update positions for volf_stoch: unsupported operand type(s) for *: 'NoneType' and 'float' Time: 2025-09-24 20:11:28
# Nik_volf_stoch_TRXUSDT_SHORT[Unexpected Error] Failed to update positions for volf_stoch: unsupported operand type(s) for *: 'NoneType' and 'float' Time: 2025-09-24 20:11:30
# Nik_volf_stoch_TRXUSDT_SHORT[Unexpected Error] Failed to update positions for volf_stoch: unsupported operand type(s) for *: 'NoneType' and 'float' Time: 2025-09-24 20:11:32
# Nik_volf_stoch_TRXUSDT_SHORT[Unexpected Error] Failed to update positions for volf_stoch: unsupported operand type(s) for *: 'NoneType' and 'float' Time: 2025-09-24 20:11:33
# Nik_volf_stoch_TRXUSDT_SHORT[Unexpected Error] Failed to update positions for volf_stoch: unsupported operand type(s) for *: 'NoneType' and 'float' Time: 2025-09-24 20:11:35
# Nik_volf_stoch_TRXUSDT_SHORT[Unexpected Error] Failed to update positions for volf_stoch: unsupported operand type(s) for *: 'NoneType' and 'float' Time: 2025-09-24 20:11:37




        # while True:
        #     cur_price = await get_cur_price(
        #         session=self.publuc_connector.session,
        #         # ws_price_data=self.context.ws_price_data,
        #         ws_price_data={},
        #         symbol="BTCUSDT",
        #         get_hot_price=self.binance_public.get_hot_price
        #     )
        #     print(cur_price)
        #     await asyncio.sleep(3.25)







# import aiohttp
# import asyncio
# import inspect

# class BINANCE_FUTURES_API:
#     def __init__(self, proxy_url=None, error_handler=None):
#         self.proxy_url = proxy_url
#         self.error_handler = error_handler
#         self.price_url = "https://fapi.binance.com/fapi/v1/ticker/price"

#     async def get_hot_price(self, session: aiohttp.ClientSession, symbol: str) -> float | None:
#         """Возвращает текущую (горячую) цену по символу с Binance Futures"""
#         params = {'symbol': symbol.upper()}
#         try:
#             async with session.get(self.price_url, params=params, proxy=self.proxy_url) as response:
#                 if response.status != 200:
#                     self.error_handler.debug_info_notes(
#                         f"Failed to fetch price for {symbol}: {response.status}"
#                     )
#                     return None
#                 data = await response.json()
#                 return float(data.get("price", 0.0))
#         except Exception as ex:
#             self.error_handler.debug_info_notes(
#                 f"{ex} in {inspect.currentframe().f_code.co_name} at line {inspect.currentframe().f_lineno}"
#             )
#             return None


# def my_error_handler():
#     raise


# async def foo():

#     api = BINANCE_FUTURES_API(proxy_url=None, error_handler=my_error_handler)

#     async with aiohttp.ClientSession() as session:
#         price = await api.get_hot_price(session, "BTCUSDT")
#         print(f"[BTCUSDT] Горячая цена: {price}")


# asyncio.run(foo())











# import asyncio
# import aiohttp
# from typing import Callable, List
# from b_context import BotContext
# from c_log import ErrorHandler
# from c_utils import PositionUtils
# from c_validators import OrderValidator
# from d_bapi import BinancePrivateApi

# class RiskSet:
#     def __init__(
#         self,
#         context: BotContext,
#         error_handler: ErrorHandler,
#         validate: OrderValidator
#     ):
#         error_handler.wrap_foreign_methods(self)
#         self.error_handler = error_handler
#         self.context = context
#         self.validate = validate

#     async def _cancel_risk_order(
#         self,
#         session,
#         user_name: str,
#         strategy_name: str,
#         symbol: str,
#         position_side: str,
#         cancel_order_by_id: Callable,
#         suffix: str
#     ) -> bool:
#         debug_label = f"[{user_name}][{strategy_name}][{symbol}][{position_side}]"
#         pos_data = self.context.position_vars[user_name][strategy_name][symbol][position_side]
#         order_id = pos_data.get(f"{suffix}_order_id")
#         if not order_id:
#             self.error_handler.trades_info_notes(
#                 f"[INFO]{debug_label}[{suffix.upper()}]: отсутствует ID ордера.", False
#             )
#             return False
#         response = await cancel_order_by_id(
#             session=session,
#             strategy_name=strategy_name,
#             symbol=symbol,
#             order_id=order_id,
#             suffix=suffix
#         )
#         if self.validate.validate_cancel_risk_response(response, suffix, debug_label):
#             pos_data[f"{suffix}_order_id"] = None
#             return True
#         return False

#     async def _place_risk_order(
#         self,
#         session,
#         user_name: str,
#         strategy_name: str,
#         symbol: str,
#         position_side: str,
#         suffix: str,
#         place_risk_order: Callable,
#         offset: float = None,
#         activation_percent: float = None,
#         is_move_tp: bool = False
#     ):
#         debug_label = f"[{user_name}][{strategy_name}][{symbol}][{position_side}]"
#         user_risk_cfg = self.context.total_settings[user_name]["symbols_risk"]
#         key = symbol if symbol in user_risk_cfg else "ANY_COINS"
#         dinamic_condition_pct = (
#             self.context.dinamik_risk_data
#             .get(user_name, {})
#             .get(symbol, {})
#             .get(suffix)
#         )
#         condition_pct = (
#             dinamic_condition_pct if dinamic_condition_pct is not None else user_risk_cfg.get(key, {}).get(suffix.lower())
#         )
#         if not condition_pct:
#             self.error_handler.debug_info_notes(f"{debug_label}: Не задан {suffix.upper()} процент.")
#             return
#         is_long = position_side == "LONG"
#         sign = 1 if is_long else -1
#         pos_data = self.context.position_vars[user_name][strategy_name][symbol][position_side]
#         avg_price = pos_data.get("avg_price")
#         qty = pos_data.get("comul_qty")
#         price_precision = self.context.position_vars[user_name][strategy_name][symbol].get("price_precision", 2)
#         order_type = user_risk_cfg.get(key, {}).get(f"tp_order_type")
#         try:
#             if suffix.lower() == "sl" and offset:
#                 target_price = round(avg_price * (1 + sign * offset / 100), price_precision)
#             elif suffix.lower() == "tp" and is_move_tp:
#                 shift_pct = activation_percent + condition_pct
#                 target_price = round(avg_price * (1 + sign * shift_pct / 100), price_precision)
#             else:
#                 shift_pct = condition_pct if suffix == "tp" else -abs(condition_pct)
#                 target_price = round(avg_price * (1 + sign * shift_pct / 100), price_precision)
#         except Exception as e:
#             print(f"{debug_label} ❌ Error calculating target_price: {e}")
#             return
#         side = "SELL" if is_long else "BUY"
#         try:
#             response = await place_risk_order(
#                 session=session,
#                 strategy_name=strategy_name,
#                 symbol=symbol,
#                 qty=qty,
#                 side=side,
#                 position_side=position_side,
#                 target_price=target_price,
#                 suffix=suffix,
#                 order_type=order_type
#             )
#         except Exception as e:
#             print(f"{debug_label} ❌ Error placing order: {e}")
#             return
#         validated = self.validate.validate_risk_response(response, suffix.upper(), debug_label)
#         if validated:
#             success, order_id = validated
#             if success:
#                 pos_data[f"{suffix.lower()}_order_id"] = order_id
#                 print(f"{debug_label} ✅ Order placed: {suffix.lower()}_order_id = {order_id}")
#                 return True
#         return False

#     async def cancel_all_risk_orders(
#         self,
#         session,
#         user_name: str,
#         strategy_name: str,
#         symbol: str,
#         position_side: str,
#         risk_suffix_list: List,  # ['tp', 'sl']
#         cancel_order_by_id: Callable,
#     ):
#         """ Отменяет оба ордера (SL и TP) параллельно. """
#         return await asyncio.gather(*[
#             self._cancel_risk_order(
#                 session, user_name, strategy_name, symbol, position_side, cancel_order_by_id, suffix
#             ) for suffix in risk_suffix_list
#         ])

#     async def place_all_risk_orders(
#         self,
#         session,
#         user_name: str,
#         strategy_name: str,
#         symbol: str,
#         position_side: str,
#         risk_suffix_list: List,  # ['tp', 'sl']
#         place_risk_order: Callable,
#         offset: float = None,
#         activation_percent: float = None,
#         is_move_tp: bool = False,
#     ):
#         """ Размещает оба ордера (SL и TP) параллельно. """
#         return await asyncio.gather(*[
#             self._place_risk_order(
#                 session, user_name, strategy_name, symbol, position_side, suffix,
#                 place_risk_order, offset, activation_percent, is_move_tp
#             ) for suffix in risk_suffix_list
#         ])

#     async def replace_sl(
#         self,
#         session: aiohttp.ClientSession,
#         user_name: str,
#         strategy_name: str,
#         symbol: str,
#         position_side: str,
#         is_move_tp: bool,
#         offset: float,
#         activation_percent: float,
#         cancel_order_by_id: Callable,
#         place_risk_order: Callable,
#         debug_label: str = ""
#     ) -> None:
#         try:
#             await self.cancel_all_risk_orders(
#                 session, user_name, strategy_name, symbol, position_side, ["tp", "sl"], cancel_order_by_id
#             )
#             self.error_handler.debug_info_notes(f"Cancelled SL/TP for {debug_label}")
#             risk_suffics_list = ['sl']
#             if is_move_tp:
#                 risk_suffics_list.append('tp')
#             await self.place_all_risk_orders(
#                 session, user_name, strategy_name, symbol, position_side, risk_suffics_list,
#                 place_risk_order, offset, activation_percent, is_move_tp
#             )
#         except aiohttp.ClientError as e:
#             self.error_handler.debug_error_notes(f"[HTTP Error] Failed to replace SL/TP for {debug_label}: {e}")
#             raise
#         except Exception as e:
#             self.error_handler.debug_error_notes(f"[Unexpected Error] Failed to replace SL/TP for {debug_label}: {e}")
#             raise

# class HandleOrders:
#     def __init__(
#         self,
#         context: BotContext,
#         error_handler: ErrorHandler,
#         pos_utils: PositionUtils,
#         risk_set: RiskSet,
#         get_hot_price: Callable,
#         get_cur_price: Callable
#     ):
#         error_handler.wrap_foreign_methods(self)
#         self.context = context
#         self.error_handler = error_handler
#         self.pos_utils = pos_utils
#         self.get_hot_price = get_hot_price
#         self.get_cur_price = get_cur_price
#         self.risk_set = risk_set
#         self.last_debug_label = {}

#     async def set_hedge_mode_for_all_users(self, all_users: List, enable_hedge: bool = True):
#         tasks = []
#         for user_name in all_users:
#             try:
#                 user_context = self.context.user_contexts[user_name]
#                 session = user_context["connector"].session
#                 binance_client: BinancePrivateApi = user_context["binance_client"]
#                 task = binance_client.set_hedge_mode(
#                     session=session, true_hedg=enable_hedge
#                 )
#                 tasks.append(task)
#             except Exception as e:
#                 self.error_handler.debug_error_notes(
#                     f"[HEDGE_MODE ERROR][{user_name}] → {e}", is_print=True
#                 )
#         await asyncio.gather(*tasks)

#     async def compose_trade_instruction(self, task_list: list[dict]):
#         from collections import defaultdict

#         async def make_trailing_task(task):
#             strategy_settings = self.context.strategy_notes[task["strategy_name"]][task["position_side"]]
#             is_move_tp = strategy_settings.get("exit_conditions", {}).get("trailing_sl", {}).get("is_move_tp", False)
#             await self.risk_set.replace_sl(
#                 task["client_session"],
#                 task["user_name"],
#                 task["strategy_name"],
#                 task["symbol"],
#                 task["position_side"],
#                 is_move_tp,
#                 task["position_data"].get("offset"),
#                 task["position_data"].get("activation_percent"),
#                 task["binance_client"].cancel_order_by_id,
#                 task["binance_client"].place_risk_order,
#                 task["debug_label"]
#             )

#         async def make_trade_task(task, side, qty):
#             try:
#                 user_name = task["user_name"]
#                 symbol = task["symbol"]
#                 strategy_name = task["strategy_name"]
#                 position_side = task["position_side"]
#                 debug_label = task["debug_label"]
#                 client_session = task["client_session"]
#                 binance_client: BinancePrivateApi = task["binance_client"]
#                 symbols_risk = self.context.total_settings[user_name]["symbols_risk"]
#                 symbol_risk_key = symbol if symbol in symbols_risk else "ANY_COINS"
#                 action = task["status"]
#                 position_data = task["position_data"]
#                 leverage = symbols_risk.get(symbol_risk_key, {}).get("leverage", 1)
#                 margin_type = symbols_risk.get(symbol_risk_key, {}).get("margin_type", "CROSSED")
#                 last_known_label = self.last_debug_label \
#                     .setdefault(user_name, {}) \
#                     .setdefault(symbol, {}) \
#                     .setdefault(position_side, None)
#                 pos = self.context.position_vars.get(user_name, {}) \
#                     .get(strategy_name, {}) \
#                     .get(symbol, {}) \
#                     .get(position_side)
#                 in_position = pos and pos.get("in_position")
#                 if action == "is_closing":
#                     if not in_position:
#                         return
#                 elif action == "is_opening":
#                     if in_position:
#                         return
#                 if debug_label != last_known_label:
#                     await binance_client.set_margin_type(client_session, strategy_name, symbol, margin_type)
#                     await binance_client.set_leverage(client_session, strategy_name, symbol, leverage)
#                     self.last_debug_label[user_name][symbol][position_side] = debug_label
#                 last_avg_price = pos.get("avg_price", None) if pos else None
#                 market_order_result = await binance_client.make_order(
#                     session=client_session,
#                     strategy_name=strategy_name,
#                     symbol=symbol,
#                     qty=qty,
#                     side=side,
#                     position_side=position_side,
#                     market_type="MARKET"
#                 )
#                 success, validated = self.risk_set.validate.validate_market_response(
#                     market_order_result[0], debug_label
#                 )
#                 if not success and action == "is_opening":
#                     self.error_handler.debug_info_notes(
#                         f"[INFO][{debug_label}] не удалось нормально открыть позицию.", is_print=True
#                     )
#                     return
#                 if action in {"is_avg", "is_closing"}:
#                     position_data["trailing_sl_progress_counter"] = 0
#                 for attempt in range(3):
#                     cancelled = await self.risk_set.cancel_all_risk_orders(
#                         session=client_session,
#                         user_name=user_name,
#                         strategy_name=strategy_name,
#                         symbol=symbol,
#                         position_side=position_side,
#                         risk_suffix_list=['tp', 'sl'],
#                         cancel_order_by_id=binance_client.cancel_order_by_id
#                     )
#                     if all(cancelled):
#                         break
#                     await asyncio.sleep(0.15)
#                 else:
#                     self.error_handler.debug_error_notes(f"[INFO][{debug_label}] не удалось отменить риск ордера после 3-х попыток ")
#                 if action == "is_closing":
#                     return
#                 if action in {"is_opening", "is_avg"}:
#                     for attempt in range(120):
#                         pos_data = self.context.position_vars.get(user_name, {}) \
#                             .get(strategy_name, {}) \
#                             .get(symbol, {}) \
#                             .get(position_side, {})
#                         avg_price = pos_data.get("avg_price")
#                         in_position = pos_data.get("in_position")
#                         if in_position and avg_price != last_avg_price and avg_price is not None:
#                             self.error_handler.debug_info_notes(
#                                 f"[READY][{debug_label}] pos_data обновлены на попытке {attempt+1}: "
#                                 f"avg_price={avg_price}, in_position={in_position}"
#                             )
#                             break
#                         await asyncio.sleep(0.15)
#                     else:
#                         self.error_handler.debug_error_notes(
#                             f"[TIMEOUT][{debug_label}] не удалось дождаться avg_price/in_position "
#                             f"(avg_price={avg_price}, in_position={in_position})"
#                         )
#                 for attempt in range(3):
#                     placed = await self.risk_set.place_all_risk_orders(
#                         session=client_session,
#                         user_name=user_name,
#                         strategy_name=strategy_name,
#                         symbol=symbol,
#                         position_side=position_side,
#                         risk_suffix_list=['tp', 'sl'],
#                         place_risk_order=binance_client.place_risk_order
#                     )
#                     if all(placed):
#                         break
#                     await asyncio.sleep(0.15)
#                 else:
#                     self.error_handler.debug_error_notes(f"[CRITICAL][{debug_label}] не удалось установить риск ордера после 3-х попыток.")
#             except Exception as e:
#                 self.error_handler.debug_error_notes(
#                     f"[Order Error] {task['debug_label']} → {e}", is_print=True
#                 )

#         grouped_tasks = defaultdict(list)
#         for task in task_list:
#             key = (task["user_name"], task["symbol"])
#             grouped_tasks[key].append(task)

#         for key, group in grouped_tasks.items():
#             sub_tasks = []
#             for task in group:
#                 try:
#                     action = task["status"]
#                     position_side = task["position_side"]
#                     debug_label = task["debug_label"]
#                     if action == "is_trailing":
#                         sub_tasks.append(make_trailing_task(task))
#                         continue
#                     if action == "is_closing":
#                         side = "SELL" if position_side == "LONG" else "BUY"
#                         qty = task["position_data"].get("comul_qty", 0.0)
#                     elif action in ["is_opening", "is_avg"]:
#                         side = "BUY" if position_side == "LONG" else "SELL"
#                         symbols_risk = self.context.total_settings[task["user_name"]]["symbols_risk"]
#                         symbol_risk_key = task["symbol"] if task["symbol"] in symbols_risk else "ANY_COINS"
#                         leverage = symbols_risk.get(symbol_risk_key, {}).get("leverage", 1)
#                         cur_price = None
#                         for _ in range(5):
#                             cur_price = await self.get_cur_price(
#                                 session=task["client_session"],
#                                 ws_price_data=self.context.ws_price_data,
#                                 symbol=task["symbol"],
#                                 get_hot_price=self.get_hot_price
#                             )
#                             if cur_price:
#                                 break
#                             await asyncio.sleep(0.25)
#                         if not cur_price:
#                             self.error_handler.debug_error_notes(
#                                 f"[CRITICAL][{debug_label}] не удалось получить цену при выставлении ордера (is_opening, is_avg)."
#                             )
#                             continue
#                         pos_martin = (
#                             self.context.position_vars
#                             .setdefault(task["user_name"], {})
#                             .setdefault(task["strategy_name"], {})
#                             .setdefault(task["symbol"], {})
#                             .setdefault("martin", {})
#                             .setdefault(position_side, {})
#                         )
#                         base_margin = symbols_risk.get(symbol_risk_key, {}).get("margin_size", 0.0)
#                         margin_size = pos_martin.get("cur_margin_size")
#                         if margin_size is None:
#                             margin_size = base_margin
#                         print(f"{debug_label}: total margin: {margin_size} usdt")
#                         qty = self.pos_utils.size_calc(
#                             margin_size=margin_size,
#                             entry_price=cur_price,
#                             leverage=leverage,
#                             volume_rate=task["position_data"].get("process_volume"),
#                             precision=task["qty_precision"],
#                             dubug_label=debug_label
#                         )
#                     else:
#                         self.error_handler.debug_info_notes(f"{debug_label} Неизвестный маркер ордера. ")
#                         continue
#                     if not qty or qty <= 0:
#                         self.error_handler.debug_info_notes(f"{debug_label} Нулевой размер позиции — пропуск")
#                         continue
#                     sub_tasks.append(make_trade_task(task, side, qty))
#                 except Exception as e:
#                     self.error_handler.debug_error_notes(
#                         f"[compose_trade_instruction] Ошибка при подготовке задачи: {task}\n→ {e}", is_print=True
#                     )
#             if sub_tasks:
#                 await asyncio.gather(*sub_tasks)




        # unique_key = f"{user_name}_{strategy_name}_{symbol}_{position_side}_is_tp"
        # if self.context.anti_double_close.get(unique_key, False):
        #     return None

        # self.context.anti_double_close[unique_key] = True


                            # if all(cancelled):
                            #     break
                        #     await asyncio.sleep(0.15)
                        # else:
                        #     self.error_handler.debug_error_notes(f"[INFO][{debug_label}] не удалось отменить риск ордера после 3-х попыток ")