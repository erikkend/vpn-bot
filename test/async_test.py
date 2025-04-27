import aiohttp
import json
from aiohttp import ClientSession


class PanelAPI:
    def __init__(self):
        self._session = None

    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.stop()

    async def start(self):
        if self._session is None or self._session.closed:
            # Явно указываем, что мы хотим сохранять куки
            jar = aiohttp.CookieJar(unsafe=True)  # unsafe=True позволяет сохранять куки без проверки домена
            self._session = aiohttp.ClientSession(cookie_jar=jar)

    async def stop(self):
        if self._session and not self._session.closed:
            await self._session.close()
            self._session = None

    async def login(self):
        if not self._session or self._session.closed:
            raise RuntimeError("Сессия не инициализирована. Вызовите start() сначала.")

        data = {
            "username": "Admin977",
            "password": "R9Ppg4Rv8M"
        }

        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0'  # Добавляем User-Agent, если сервер его требует
        }

        async with self._session.post("http://57.129.67.153:2053/login", json=data, headers=headers) as response:
            print(f"Login status: {response.status}")
            text = await response.text()
            print(f"Login response: {text}")

            # Получаем и выводим куки после запроса
            cookies = self._session.cookie_jar.filter_cookies("http://57.129.67.153:2053")
            print("Cookies после логина:", dict(cookies))

            if response.status >= 400:
                raise Exception(f"Ошибка при логине: {text}")

            return response.status, text

    async def add_client(self, client_settings):
        if not self._session or self._session.closed:
            raise RuntimeError("Сессия не инициализирована. Вызовите start() сначала.")

        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0'
        }

        async with self._session.post(
                "http://57.129.67.153:2053/panel/api/inbounds/addClient",
                json=client_settings,
                headers=headers
        ) as response:
            print(f"Add client status: {response.status}")
            text = await response.text()
            print(f"Add client response: {text}")

            # Получаем и выводим куки после запроса
            cookies = self._session.cookie_jar.filter_cookies("http://57.129.67.153:2053")
            print("Cookies после добавления клиента:", dict(cookies))

            if response.status >= 400:
                raise Exception(f"Ошибка при добавлении клиента: {text}")

            return response.status, text

    def get_cookies(self):
        """Метод для получения текущих куков сессии."""
        if not self._session or self._session.closed:
            raise RuntimeError("Сессия не инициализирована или закрыта.")

        cookies = self._session.cookie_jar.filter_cookies("http://57.129.67.153:2053")
        return dict(cookies)

    async def test(self):
        client_settings = {"order_id": "13",
                           "status": "paid"
        }

        async with self._session.post(
                "https://stablevpn.shop/demo-post/",
                json=client_settings
        ) as response:
            text = await response.text()
            print(f"Test:\n{text}")

            return response.status, text


# Пример использования
async def main():
    async with PanelAPI() as api:
        await api.test()

if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
    
    
#     ZCblGO0Jii
# Password: Xu9EVV4914
# Port: 14349
# WebBasePath: XuizpbVnN9dPdBA
# Access URL: http://57.129.67.153:14349/XuizpbVnN9dPdBA