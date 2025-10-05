
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


