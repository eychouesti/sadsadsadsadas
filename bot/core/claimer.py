import asyncio
import time
from datetime import datetime
from urllib.parse import unquote

import aiohttp
from aiohttp_proxy import ProxyConnector
from better_proxy import Proxy
from pyrogram import Client
from pyrogram.errors import Unauthorized, UserDeactivated, AuthKeyUnregistered
from pyrogram.raw.functions.messages import RequestWebView
from pyrogram.types import Message
from pyrogram.filters import command, private

from ..config import settings

# Loglama için bir fonksiyon
def log(message):
    print(f"{datetime.now()} - {message}")

class WigwamClaimer:
    def __init__(self, client: Client):
        self.client = client
        self.session_name = client.name
        self.is_authorized = False

    async def get_tg_web_data(self) -> str:
        try:
            if not self.client.is_connected:
                await self.client.connect()

            web_view = await self.client.invoke(RequestWebView(
                peer=await self.client.resolve_peer('drumtap_bot'),
                bot=await self.client.resolve_peer('drumtap_bot'),
                platform='android',
                from_bot_menu=False,
                url='https://drum.wigwam.app'  # Wigwam web uygulaması URL'si
            ))

            auth_url = web_view.url
            tg_web_data = unquote(
                string=auth_url.split('tgWebAppData=', maxsplit=1)[1].split('&tgWebAppVersion', maxsplit=1)[0])

            return tg_web_data

        except Exception as error:
            log(f"{self.session_name} | Telegram web verileri alınamadı: {error}")
            await asyncio.sleep(delay=3)

    async def get_drum_game_data(self, user_id) -> dict:
        try:
            headers = {"Authorization": f"Bearer {settings.API_TOKEN}"}  # Eğer API token gerekiyorsa
            response = requests.post(f"{settings.API_BASE_URL}/getUserInfo", json={"devAuthData": user_id, "authData": await self.get_tg_web_data(), "platform": "web", "data": {}}, headers=headers)
            response.raise_for_status()

            response_json = response.json()
            drum_game_data = response_json['data']
            return drum_game_data
        except Exception as error:
            log(f"{self.session_name} | Kullanıcı bilgileri alınamadı: {error}")
            await asyncio.sleep(delay=3)

    async def tap_drum(self, user_id) -> bool:
        try:
            headers = {"Authorization": f"Bearer {settings.API_TOKEN}"}
            response = requests.post(f"{settings.API_BASE_URL}/tapDrum", json={"userId": user_id}, headers=headers)
            response.raise_for_status()

            log(f"{self.session_name} | Tap işlemi başarılı: {response.json()}")
            return True
        except Exception as error:
            log(f"{self.session_name} | Tap işlemi başarısız: {error}")
            await asyncio.sleep(delay=3)
            return False

    async def claim_farm_reward(self, user_id) -> bool:
        try:
            headers = {"Authorization": f"Bearer {settings.API_TOKEN}"}
            response = requests.post(f"{settings.API_BASE_URL}/claimFarm", headers=headers)
            response.raise_for_status()

            response_json = await response.json()
            claimed_balance = response_json['data']['claimedBalance']

            log(f"{self.session_name} | Çiftlik ödülü başarıyla toplandı: {claimed_balance} DRUM")
            return True
        except Exception as error:
            log(f"{self.session_name} | Çiftlik ödülü toplama başarısız: {error}")
            await asyncio.sleep(delay=3)
            return False

    async def run(self, message) -> None:
        self.user_id = message.from_user.id
        proxy_connector = ProxyConnector().from_url(settings.PROXY_URL) if settings.USE_PROXY else None
        async with aiohttp.ClientSession(connector=proxy_connector) as http_client:
            while True:
                user_info = await self.get_drum_game_data(self.user_id)

                if user_info["availableTaps"] > 0:
                    await self.tap_drum(self.user_id)
                else:
                    remaining_time = user_info["currentTapWindowFinishIn"] / 1000
                    log(f"{self.session_name} | Tap hakkı yok. Kalan süre: {remaining_time} saniye")
                    time.sleep(remaining_time)

                await asyncio.sleep(settings.TAP_INTERVAL)
                await self.claim_farm_reward(self.user_id)
                await asyncio.sleep(settings.CLAIM_FARM_INTERVAL)
