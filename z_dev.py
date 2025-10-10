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
#         # print(f"\n📌 START placing {suffix.upper()} order for [{user_name}][{strategy_name}][{symbol}][{position_side}]")
#         debug_label = f"[{user_name}][{strategy_name}][{symbol}][{position_side}]"

#         user_risk_cfg = self.context.total_settings[user_name]["symbols_risk"]
#         key = symbol if symbol in user_risk_cfg else "ANY_COINS"

#         dinamic_condition_pct = (
#             self.context.dinamik_risk_data
#                 .get(user_name, {})
#                 .get(symbol, {})
#                 .get(suffix)
#         )

#         condition_pct = (
#             dinamic_condition_pct
#             if dinamic_condition_pct is not None
#             else user_risk_cfg.get(key, {}).get(suffix.lower())
#         )

#         # print(f"{debug_label} → condition_pct ({suffix}): {condition_pct}")
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

#         # print(f"{debug_label} → avg_price: {avg_price}, qty: {qty}, precision: {price_precision}, sign: {sign}")

#         try:
#             if suffix.lower() == "sl" and offset:
#                 target_price = round(avg_price * (1 + sign * offset / 100), price_precision)
#                 # print(f"{debug_label} → SL offset: {offset}, target_price: {target_price}")

#             elif suffix.lower() == "tp" and is_move_tp:
#                 shift_pct = activation_percent + condition_pct
#                 target_price = round(avg_price * (1 + sign * shift_pct / 100), price_precision)
#                 # print(f"{debug_label} → TP shift (activation + condition): {shift_pct}, target_price: {target_price}")

#             else:
#                 # === Вычисления ===
#                 shift_pct = condition_pct if suffix == "tp" else -abs(condition_pct)
#                 target_price = round(avg_price * (1 + sign * shift_pct / 100), price_precision)

#         except Exception as e:
#             print(f"{debug_label} ❌ Error calculating target_price: {e}")
#             return

#         side = "SELL" if is_long else "BUY"
#         # print(f"{debug_label} → placing order: side={side}, qty={qty}, price={target_price}, suffix={suffix}")

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
#         # print(f"{debug_label} → validation result: {validated}")
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
#         risk_suffix_list: List, # ['tp', 'sl']
#         cancel_order_by_id: Callable,
#     ):
#         """
#         Отменяет оба ордера (SL и TP) параллельно.
#         """
#         return await asyncio.gather(*[
#             self._cancel_risk_order(
#                 session,
#                 user_name,
#                 strategy_name,
#                 symbol,
#                 position_side,
#                 cancel_order_by_id,
#                 suffix
#             )
#             for suffix in risk_suffix_list
#         ])

#     async def place_all_risk_orders(
#         self,
#         session,
#         user_name: str,
#         strategy_name: str,
#         symbol: str,
#         position_side: str,
#         risk_suffix_list: List, # ['tp', 'sl']
#         place_risk_order: Callable,
#         offset: float = None,
#         activation_percent: float = None,
#         is_move_tp: bool = False,
#     ):
#         """
#         Размещает оба ордера (SL и TP) параллельно.
#         """
#         return await asyncio.gather(*[
#             self._place_risk_order(
#                 session,
#                 user_name,
#                 strategy_name,
#                 symbol,
#                 position_side,
#                 suffix,
#                 place_risk_order,
#                 offset,
#                 activation_percent,
#                 is_move_tp
#             )
#             for suffix in risk_suffix_list
#         ])

#     # ////////
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
#             # 🚫 Отменяем TP и SL
#             await self.cancel_all_risk_orders(
#                     session,
#                     user_name,
#                     strategy_name,
#                     symbol,
#                     position_side,
#                     ["tp", "sl"],
#                     cancel_order_by_id
#                 )
#             self.error_handler.debug_info_notes(f"Cancelled SL/TP for {debug_label}")

#             risk_suffics_list = ['sl']
#             if is_move_tp:
#                 risk_suffics_list.append('tp')

#             await self.place_all_risk_orders(
#                 session,
#                 user_name,
#                 strategy_name,
#                 symbol,
#                 position_side,
#                 risk_suffics_list,
#                 place_risk_order,
#                 offset,
#                 activation_percent,
#                 is_move_tp
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
#         # self.sync_pos_all_users = sync_pos_all_users
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
#                     session=session,
#                     true_hedg=enable_hedge
#                 )
#                 tasks.append(task)

#             except Exception as e:
#                 self.error_handler.debug_error_notes(
#                     f"[HEDGE_MODE ERROR][{user_name}] → {e}", is_print=True
#                 )

#         await asyncio.gather(*tasks)

#     async def compose_trade_instruction(self, task_list: list[dict]):
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

#                 # Проставим плечо и тип маржи, если debug_label новый
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

#                 last_avg_price = pos_data.get("avg_price", None)

#                 # Основной запрос на маркет-ордер
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
#                         f"[INFO][{debug_label}] не удалось нормально открыть позицию.",
#                         is_print=True
#                     )
#                     return

#                 if action in {"is_avg", "is_closing"}:
#                     position_data["trailing_sl_progress_counter"] = 0

#                     for attempt in range(3):  # максимум 3 попытки
#                         if await self.risk_set.cancel_all_risk_orders(
#                             session=client_session,
#                             user_name=user_name,
#                             strategy_name=strategy_name,
#                             symbol=symbol,
#                             position_side=position_side,
#                             risk_suffix_list=['tp', 'sl'],
#                             cancel_order_by_id=binance_client.cancel_order_by_id
#                         ):
#                             break
#                         await asyncio.sleep(0.15)
#                     else:
#                         # цикл не прервался — не дождались обновления
#                         self.error_handler.debug_error_notes(f"[INFO][{debug_label}] не удалось отменить риск ордера после 3-х попыток ")
#                     if action == "is_closing":
#                         return
                
#                 if action in {"is_opening", "is_avg"}:
#                     # ждем, пока контекст обновит in_position и avg_price
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
#                         # цикл не прервался — не дождались обновления
#                         self.error_handler.debug_error_notes(
#                             f"[TIMEOUT][{debug_label}] не удалось дождаться avg_price/in_position "
#                             f"(avg_price={avg_price}, in_position={in_position})"
#                         )

#                     for attempt in range(3):  # максимум 3 попытки
#                         if await self.risk_set.place_all_risk_orders(
#                             session=client_session,
#                             user_name=user_name,
#                             strategy_name=strategy_name,
#                             symbol=symbol,
#                             position_side=position_side,
#                             risk_suffix_list=['tp', 'sl'],
#                             place_risk_order=binance_client.place_risk_order
#                         ):
#                             break
#                         await asyncio.sleep(0.15)
#                     else:
#                         # цикл не прервался — не дождались обновления
#                         self.error_handler.debug_error_notes(f"[CRITICAL][{debug_label}] не удалось установить риск ордера после 3-х попыток.")

#             except Exception as e:
#                 self.error_handler.debug_error_notes(
#                     f"[Order Error] {task['debug_label']} → {e}",
#                     is_print=True
#                 )

#         tasks = []

#         for task in task_list:
#             try:
#                 action = task["status"]
#                 user_name = task["user_name"]
#                 strategy_name = task["strategy_name"]
#                 symbol = task["symbol"]
#                 position_side = task["position_side"]
#                 debug_label = task["debug_label"]

#                 if action == "is_trailing":
#                     tasks.append(make_trailing_task(task))
#                     continue

#                 if action == "is_closing":
#                     side = "SELL" if position_side == "LONG" else "BUY"
#                     qty = task["position_data"].get("comul_qty", 0.0)

#                 elif action in ["is_opening", "is_avg"]:
#                     side = "BUY" if position_side == "LONG" else "SELL"
#                     symbols_risk = self.context.total_settings[task["user_name"]]["symbols_risk"]
#                     symbol_risk_key = task["symbol"] if task["symbol"] in symbols_risk else "ANY_COINS"
#                     leverage = symbols_risk.get(symbol_risk_key, {}).get("leverage", 1)

#                     for _ in range(5):  # 1 + 3 попытки
#                         cur_price = await self.get_cur_price(
#                             session=task["client_session"],
#                             ws_price_data=self.context.ws_price_data,
#                             symbol=task["symbol"],
#                             get_hot_price=self.get_hot_price
#                         )
#                         if cur_price:
#                             break
#                         await asyncio.sleep(0.25)
#                     else:
#                         # цикл не прервался — не дождались обновления
#                         self.error_handler.debug_error_notes(
#                             f"[CRITICAL][{debug_label}] не удалось установить получить цену при выставлении ордера (is_opening, is_avg)."
#                         )
#                         continue

#                     pos_martin = (
#                         self.context.position_vars
#                             .setdefault(user_name, {})
#                             .setdefault(strategy_name, {})
#                             .setdefault(symbol, {})
#                             .setdefault("martin", {})
#                             .setdefault(position_side, {})
#                     )

#                     base_margin = symbols_risk.get(symbol_risk_key, {}).get("margin_size", 0.0)
#                     margin_size = pos_martin.get("cur_margin_size")
#                     if margin_size is None:
#                         margin_size = base_margin               

#                     print(f"{debug_label}: total margin: {margin_size} usdt")
#                     qty = self.pos_utils.size_calc(
#                         margin_size=margin_size,
#                         entry_price=cur_price,
#                         leverage=leverage,
#                         volume_rate=task["position_data"].get("process_volume"),
#                         precision=task["qty_precision"],
#                         dubug_label=debug_label
#                     )
#                 else:
#                     self.error_handler.debug_info_notes(f"{debug_label} Неизвестный маркер ордера. ")
#                     continue

#                 if not qty or qty <= 0:
#                     self.error_handler.debug_info_notes(f"{debug_label} Нулевой размер позиции — пропуск")
#                     continue

#                 tasks.append(make_trade_task(task, side, qty))

#             except Exception as e:
#                 self.error_handler.debug_error_notes(
#                     f"[compose_trade_instruction] Ошибка при подготовке задачи: {task}\n→ {e}",
#                     is_print=True
#                 )

#         return await asyncio.gather(*tasks)

