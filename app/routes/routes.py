from datetime import datetime

from aiogram import Bot
from aiohttp.web_request import Request
from aiohttp.web_response import json_response
from dateutil.relativedelta import relativedelta

from app import utils
from app.database import get_session
from app.models.order import OrderStatus

from app.crud.order_service import get_order_by_id
from app.crud.vpn_key_service import create_vpn_key, get_vpn_key_by_user_id
from app.crud.subscription_service import create_subscription, update_vpn_expire_time
from app.crud.user_service import get_user_by_user_id
from app.crud.server_service import select_server_by_region, select_server_by_id

from py3xui import AsyncApi, Client


async def heleket_order_handler(request: Request):
    data = await request.json()
    print(f"Data: {data}")
    bot: Bot = request.app["bot"]

    order_id = data.get("order_id")
    status = data.get("status")


    async for session in get_session():
        # здесь должна быть проверка, если уже существует ключ, то добавляем к нему время
        # может быть такое что heleket сам по себе отправляет данные и нужно проверить
        # хотя просто нужно сверить статус который с БД пришел и который с heleket и все
        # получается я с БД беру ордер, беру подписку, если нет создаю ее если есть нужно продлить

        order = await get_order_by_id(session, int(order_id))
        user = await get_user_by_user_id(session, order.user_id)

        # Проверка статуса платежа с БД, если уже оплачено то делаем ретерн, если нет то дальше
        if order.status in [OrderStatus.PAID, OrderStatus.PAID_OVER]:
            return json_response({"message": "Already paid"})
        # добавить проверку статуса cancel
        
        if status in ["paid", "paid_over"]:
            order.status = OrderStatus.PAID
            order.paid_at = datetime.now()
            month_count = order.month_count
            region = order.server_region
            
            vpn_key = await get_vpn_key_by_user_id(session, user.id)
            if vpn_key:
                await prolong_key(session, bot, user, vpn_key, month_count)
                return json_response({"message": "Key created"})
            else:
                await create_new_key(session, order, bot, month_count, region)
                return json_response({"message": "Key created"})


async def create_new_key(session, order, bot: Bot, months, region):
    server = await select_server_by_region(session, region)
    print(f"Server: {server}")
    username = server.panel_username
    password = server.panel_password
    server_port = server.panel_port
    server_webpath = server.panel_webpath
    server_ip = server.server_ip
    
    print(f"Username: {username}, Password: {password}")
    print(f"Server IP: {server_ip}, Port: {server_port}, Webpath: {server_webpath}")
    
    api = AsyncApi(host=f"https://{server_ip}:{server_port}/{server_webpath}", username=username, password=password, use_tls_verify=False)
    await api.login()
    
    now = datetime.now().replace(tzinfo=None)
    expires_at = now + relativedelta(months=months)
    timestamp = int(expires_at.timestamp() * 1000)
    settings = utils.create_settings_for_new_key()
    
    new_client = Client(id=settings[0], email=settings[1], enable=True, flow="xtls-rprx-vision", expiryTime=timestamp)
    inbound_id = 1

    await api.client.add(inbound_id, [new_client])
    new_client = await api.client.get_by_email(settings[1])
    
    connection_str = await generate_connection_string(api, settings[0], settings[1], server_ip)

    if new_client:
        vpn_key = await create_vpn_key(session, order.user_id, connection_str, settings[0], settings[1], server.id)
        await create_subscription(session, vpn_key.id, expires_at)
        user = await get_user_by_user_id(session, order.user_id)
        await bot.send_message(user.telegram_id, f"✅ Оплата прошла. Ваш VPN:\n`{vpn_key.full_key_data}`", parse_mode="Markdown")


async def prolong_key(session, bot, user, vpn_key, months):
    server_id = vpn_key.server_id
    server = await select_server_by_id(session, server_id)
    username = server.panel_username
    password = server.panel_password
    server_port = server.panel_port
    server_webpath = server.panel_webpath
    server_ip = server.server_ip
    
    api = AsyncApi(host=f"https://{server_ip}:{server_port}/{server_webpath}", username=username, password=password, use_tls_verify=False)
    await api.login()

    vpn_date = vpn_key.subscription.expires_at
    expires_at = vpn_date + relativedelta(months=months)
    timestamp = int(expires_at.timestamp() * 1000)
    
    client = await api.client.get_by_email(vpn_key.key_email)
    print(client)
    client.expiry_time = timestamp
    
    await api.client.update(vpn_key.key_uuid, client)

    await update_vpn_expire_time(session, vpn_key.id, expires_at)
    await bot.send_message(user.telegram_id, f"✅ Оплата прошла. Ваш ключ продлен до {expires_at}")


async def generate_connection_string(api, user_uuid: str, user_email: int, server_ip: str):
    inbounds = await api.inbound.get_list()
    inbound = inbounds[0]
    
    public_key = inbound.stream_settings.reality_settings.get("settings").get("publicKey")
    website_name = inbound.stream_settings.reality_settings.get("serverNames")[0]
    short_id = inbound.stream_settings.reality_settings.get("shortIds")[0]

    connection_string = (
        f"vless://{user_uuid}@{server_ip}:444"
        f"?type=tcp&security=reality&pbk={public_key}&fp=chrome&sni={website_name}"
        f"&sid={short_id}&spx=%2F&flow=xtls-rprx-vision#VLESS_REALITY-{user_email}"
    )

    return connection_string
