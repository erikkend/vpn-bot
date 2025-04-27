import os
import json
import hashlib
import base64

from aiohttp import ClientSession
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("HELEKET_API")
MERCHANT_UUID = os.getenv("HELEKET_UUID")

def generate_headers(data):
    sign = hashlib.md5(
        base64.b64encode(data.encode("ascii")) + API_KEY.encode("ascii")
    ).hexdigest()

    return {"merchant": MERCHANT_UUID, "sign": sign, "content-type": "application/json"}

async def create_invoice(order_id: int, amount: str):
    async with ClientSession() as session:
        json_str = json.dumps({
            "amount": amount,
            "order_id": str(order_id),
            "currency": "USDT",
            "lifetime": 300,
            "url_callback" : "https://dear-genuine-scorpion.ngrok-free.app/demo-post/"
        })
        response = await session.post(
            "https://api.heleket.com/v1/payment",
            data=json_str,
            headers=generate_headers(json_str)
        )
        return await response.json()


async def get_invoice(invoice_uuid):
    async with ClientSession() as session:
        json_str = json.dumps({"uuid": invoice_uuid})
        response = await session.post(
            "https://api.heleket.com/v1/payment/info",
            data=json_str,
            headers=generate_headers(json_str)
        )
        return await response.json()
