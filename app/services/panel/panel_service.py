import os
import aiohttp

from dotenv import load_dotenv

load_dotenv()

class PanelAPI:
    def __init__(self):
        self._session = None  # Инициализируем сессию как None

    async def __aenter__(self):
        """Асинхронный контекстный менеджер для входа в класс."""
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Асинхронный контекстный менеджер для выхода из класса."""
        await self.stop()

    async def start(self):
        """Инициализация сессии."""
        if self._session is None or self._session.closed:
            jar = aiohttp.CookieJar(unsafe=True)
            self._session = aiohttp.ClientSession(cookie_jar=jar)

    async def stop(self):
        """Закрытие сессии."""
        if self._session and not self._session.closed:
            await self._session.close()
            self._session = None

    async def login(self):
        """Выполнение логина."""
        if not self._session or self._session.closed:
            raise RuntimeError("Сессия не инициализирована. Вызовите start() сначала.")

        data = {
            "username": os.getenv("PANEL_USER"),
            "password": os.getenv("PANEL_PASS")
        }

        async with self._session.post("https://57.129.67.153:65000/vpn-panel/login", data=data, ssl=False) as response:
            content = await response.read()
            return response.status, content

    async def add_client(self, client_settings, key_uuid, key_sub_id):
        """Добавление нового клиента."""
        if not self._session or self._session.closed:
            raise RuntimeError("Сессия не инициализирована. Вызовите start() сначала.")

        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0'
        }
        async with self._session.post("https://57.129.67.153:65000/vpn-panel/panel/api/inbounds/addClient",
                                    headers=headers, json=client_settings, ssl=False) as response:
            content = await response.text()

            if content == """{"success":true,"msg":"Client(s) added Successfully","obj":null}""":
                proxy_cred = f"vless://{key_uuid}@57.129.67.153:433?type=tcp&security=reality&pbk=N0RqXw2DN2m9iSyS9q4feMEInH11gs4tH9KaA-2u11I&fp=chrome&sni=yahoo.com&sid=aa199bc1b9a4c5&spx=%2F&flow=xtls-rprx-vision#VLESS-REALITY-{key_sub_id}"
                return proxy_cred
            return False

    async def update_key(self, client_settings, key_uuid):
        if not self._session or self._session.closed:
            raise RuntimeError("Сессия не инициализирована. Вызовите start() сначала.")

        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0'
        }

        async with self._session.post(f"https://57.129.67.153:65000/vpn-panel/panel/inbound/updateClient/{key_uuid}",
                                      headers=headers, json=client_settings, ssl=False) as response:
            content = await response.text()
            if content == """{"success":true,"msg":"Client updated Successfully","obj":null}""":
                return True
            return False
