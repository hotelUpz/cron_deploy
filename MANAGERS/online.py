import asyncio
import aiohttp
import json
from typing import *
from b_context import BotContext
from c_log import ErrorHandler
import contextlib
import traceback


MAX_RECONNECT = 99999999999999

class NetworkManager:
    def __init__(self, error_handler: ErrorHandler, proxy_url: str=None, user_label: str=None):
        error_handler.wrap_foreign_methods(self)
        self.error_handler = error_handler

        self.session: Optional[aiohttp.ClientSession] = None
        self.proxy_url = proxy_url
        self.user_label = user_label

    async def initialize_session(self):
        if not self.session or self.session.closed:
            self.session = aiohttp.ClientSession()

    async def _check_session_connection(self, session):
        try:
            async with session.get("https://api.binance.com/api/v3/ping", proxy=self.proxy_url) as response:
                return response.status == 200
        except aiohttp.ClientError:
            return False

    async def validate_session(self) -> tuple[bool, bool]:
        """
        Проверяет сессию. Если была замена или пересоздание — возвращает (True, True).
        Если всё в порядке — (True, False).
        Если не удалось восстановить — (False, True).
        """
        was_reconnected = False

        for attempt in range(1, MAX_RECONNECT + 1):
            if self.session and not self.session.closed:
                if await self._check_session_connection(self.session):
                    return True, was_reconnected  # Успешно, даже если reconnected = False

                try:
                    await self.session.close()
                except Exception as e:
                    self.error_handler.debug_error_notes(f"{self.user_label}: Ошибка при закрытии сессии: {e}. ")

            await asyncio.sleep((attempt * 1.6) + 1)
            self.error_handler.debug_error_notes(f"🔁 {self.user_label}: Попытка восстановить сессию ({attempt}/{MAX_RECONNECT})...")
            await self.initialize_session()
            was_reconnected = True  # Сессия пересоздана

        self.error_handler.debug_error_notes(f"❌ {self.user_label}: Не удалось восстановить сессию после нескольких попыток.", True)
        return False, was_reconnected
    
    async def shutdown_session(self):
        """Закрытие aiohttp-сессии при остановке."""
        if self.session and not self.session.closed:
            try:
                await self.session.close()
            except Exception as e:
                self.error_handler.debug_error_notes(f"{self.user_label}: ошибка при закрытии сессии в shutdown_session(): {e}. ")
# # python -m MANAGERS.networks


class WebSocketManager:
    """Менеджер WebSocket для получения последних сделок (hot price) с Binance Futures."""

    def __init__(
        self,
        context: BotContext,
        error_handler: ErrorHandler,
        proxy_url: Optional[str] = None,
        ws_url: str = "wss://fstream.binance.com/"
    ):
        error_handler.wrap_foreign_methods(self)
        self.error_handler = error_handler
        self.context = context

        # --- состояние ---
        self.session: Optional[aiohttp.ClientSession] = None
        self.websocket: Optional[aiohttp.ClientWebSocketResponse] = None
        self.ws_task: Optional[asyncio.Task] = None
        self.is_connected: bool = False

        # --- параметры ---
        self.max_reconnect_attempts: int = 50
        self.reconnect_attempts: int = 0
        self.ws_shutdown_event: asyncio.Event = asyncio.Event()
        self.WEBSOCKET_URL: str = ws_url

        # --- прокси ---
        self.proxy_url: Optional[str] = proxy_url
        self.proxy_auth: Optional[aiohttp.BasicAuth] = None

    # ============================================================
    #  Обработка входящих сообщений
    # ============================================================
    async def handle_ws_message(self, message: str) -> None:
        try:
            payload = json.loads(message)
            data = payload.get("data")
            if not data:
                return

            symbol = data.get("s")
            price = float(data.get("p", 0.0))
            if not symbol or price <= 0:
                return

            # обновляем горячую цену в контексте
            self.context.ws_price_data[symbol] = {"close": price}

        except Exception as e:
            self.error_handler.debug_error_notes(
                f"[WS Handle] Error: {e}\n{traceback.format_exc()}"
            )

    # ============================================================
    #  Ping keepalive
    # ============================================================
    async def keepalive_ping(self) -> None:
        """Отправляет ping каждые 15 секунд."""
        while not self.ws_shutdown_event.is_set() and self.websocket:
            try:
                await self.websocket.ping()
                await asyncio.sleep(15)
            except Exception as e:
                self.error_handler.debug_error_notes(f"[Ping] Ошибка: {e}")
                break

    # ============================================================
    #  Подключение и основной цикл
    # ============================================================
    async def connect_and_handle(self, symbols: List[str]) -> None:
        if not symbols:
            self.error_handler.debug_error_notes("[WS] Пустой список символов")
            return

        # --- формируем trade-стримы ---
        streams = [f"{symbol.lower()}@trade" for symbol in symbols]
        ws_url = f"{self.WEBSOCKET_URL}stream?streams={'/'.join(streams)}"

        if not self.session:
            self.session = aiohttp.ClientSession()

        while self.reconnect_attempts < self.max_reconnect_attempts:
            if self.ws_shutdown_event.is_set():
                break

            try:
                # --- создаем websocket ---
                self.websocket = await self.session.ws_connect(
                    ws_url,
                    proxy=self.proxy_url,
                    proxy_auth=self.proxy_auth,
                    autoping=False
                )

                self.is_connected = True
                self.reconnect_attempts = 0
                self.error_handler.debug_info_notes(f"[WS] Connected: {ws_url}")

                # --- запускаем ping ---
                ping_task = asyncio.create_task(self.keepalive_ping())

                # --- читаем поток ---
                async for msg in self.websocket:
                    if self.ws_shutdown_event.is_set():
                        await self.websocket.close(code=1000, message=b"Shutdown")
                        break

                    if msg.type == aiohttp.WSMsgType.TEXT:
                        await self.handle_ws_message(msg.data)
                    elif msg.type in (aiohttp.WSMsgType.CLOSED, aiohttp.WSMsgType.ERROR):
                        break

                ping_task.cancel()
                with contextlib.suppress(asyncio.CancelledError):
                    await ping_task

            except Exception as e:
                self.error_handler.debug_error_notes(
                    f"[WS Error] {e}\n{traceback.format_exc()}"
                )
                self.reconnect_attempts += 1
                backoff = min(2 * self.reconnect_attempts, 10)
                await asyncio.sleep(backoff)

        self.is_connected = False
        self.error_handler.debug_error_notes("[WS] Достигнут лимит переподключений")

    # ============================================================
    #  Управление WS
    # ============================================================
    async def connect_to_websocket(self, symbols: List[str]) -> None:
        try:
            await self.stop_ws_process()
            self.ws_shutdown_event.clear()
            self.reconnect_attempts = 0
            self.ws_task = asyncio.create_task(self.connect_and_handle(symbols))
        except Exception as e:
            self.error_handler.debug_error_notes(f"[WS Connect] Failed: {e}")

    async def restart_ws(self):
        """Принудительный перезапуск."""
        try:
            await self.stop_ws_process()
            await self.connect_to_websocket(list(self.context.fetch_symbols))
            self.error_handler.debug_info_notes("[WS] Перезапущен")
        except Exception as e:
            self.error_handler.debug_error_notes(f"[WS Restart] Ошибка: {e}")

    async def stop_ws_process(self) -> None:
        """Останавливает текущий процесс WS."""
        self.ws_shutdown_event.set()

        if self.ws_task:
            self.ws_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await asyncio.wait_for(self.ws_task, timeout=5)
            self.ws_task = None
            self.is_connected = False

        if self.websocket:
            await self.websocket.close()
            self.websocket = None

        if self.session and not self.session.closed:
            await self.session.close()

        # self.error_handler.debug_info_notes("[WS] Процесс остановлен")

    async def sync_ws_streams(self, active_symbols: list) -> None:
        """Синхронизирует активные символы (перезапускает при изменении списка)."""
        new_symbols_set = set(active_symbols)
        if new_symbols_set != getattr(self, "last_symbols_set", set()):
            self.last_symbols_set = new_symbols_set
            if new_symbols_set:
                await self.connect_to_websocket(list(new_symbols_set))
            else:
                await self.stop_ws_process()
