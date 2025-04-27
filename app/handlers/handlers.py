from datetime import datetime

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from app.keyboards import keyboards
from app.database import get_session
from app.services.payments.heleket_api import create_invoice
from app.crud.user_service import get_user_by_telegram_id, create_user
from app.crud.vpn_key_service import get_vpn_key_by_user_id
from app.crud.order_service import create_order, update_order_info


router = Router()


class VPNStates(StatesGroup):
    select_server = State()
    select_tariff = State()
    test = State()

@router.message(CommandStart())
async def start(message: Message):
    async for session in get_session():
        user = await get_user_by_telegram_id(session, str(message.from_user.id))
        if not user:
            await create_user(session, str(message.from_user.id), message.from_user.username)

    await message.answer(text="""Главное меню""", reply_markup=keyboards.main_kb)


@router.callback_query(F.data == "buy_key")
async def show_servers(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    async for session in get_session():
        user = await get_user_by_telegram_id(session, str(callback.from_user.id))
        vpn_key = await get_vpn_key_by_user_id(session, user.id)
        if vpn_key:
            server_region = vpn_key.server.region
            print(f"server_region: {server_region}")
            await state.update_data(region=server_region)
            await state.set_state(VPNStates.select_tariff)
            await callback.message.answer("Выбери тариф:", reply_markup=keyboards.price_kb)
            await state.set_state(VPNStates.select_tariff)
        else:
            # нужно билдть клаву т.е показывать только те регионы которые is_active
            await callback.message.answer("Выбери регион сервера:", reply_markup=keyboards.regions_kb)
            await state.set_state(VPNStates.select_server)


@router.callback_query(F.data.startswith("region:"))
async def handle_region(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = callback.data.split(":")[1]
    await state.update_data(region=data)
    await callback.message.answer("Выбери тариф:", reply_markup=keyboards.price_kb)
    await state.set_state(VPNStates.select_tariff)

@router.callback_query(VPNStates.select_tariff, F.data.startswith("tariff:"))
async def form_price(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    tariff_type = callback.data.split(':')[1]
    data = await state.get_data()
    region = data.get("region")
    await state.clear()
    
    price = None
    month_count = None
    if tariff_type == "1":
        price = "2.20"
        month_count = 1
    elif tariff_type == "2":
        price = "4.40"
        month_count = 3
    elif tariff_type == "3":
        price = "6.60"
        month_count = 6
    elif tariff_type == "4":
        price = "10"
        month_count = 12

    async for session in get_session():
        user = await get_user_by_telegram_id(session, str(callback.from_user.id))
        order = await create_order(session, user.id, price, "USDT", month_count, region)
        invoice = await create_invoice(order.id, price)

        kb = keyboards.create_invoice_keyboard(invoice['result']['url'])
        await update_order_info(session, order.id, invoice['result']['uuid'])
        await callback.message.answer(text="""❗️ При оплате криптой учитывайте, что выдача доступа происходит в течении 5 минут ПОСЛЕ ПОДТВЕРЖДЕНИЯ ОПЛАТЫ.\nЕсли возникли вопросы с оплатой ты всегда можешь написать нам.""",
                                      reply_markup=kb)


@router.callback_query(F.data == "my_key")
async def show_all_config(callback: CallbackQuery):
    await callback.answer()
    async for session in get_session():
        user = await get_user_by_telegram_id(session, str(callback.from_user.id))
        vpn_key = await get_vpn_key_by_user_id(session, user.id)
        if vpn_key:
            date = vpn_key.subscription.expires_at
            formatted_date = datetime.strftime(date, "%Y.%m.%d %H:%M")
            await callback.message.answer(f"Ключ работает до: {formatted_date}\nКлюч:\n`{vpn_key.full_key_data}`", parse_mode="Markdown")
        else:
            await callback.message.answer(f"У вас нет VPN-ключа",
                                          parse_mode="Markdown")


@router.callback_query(F.data == "supp_contacts")
async def support_contacts(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer("Телеграм: `@xtwdgnuuqp`\nПочта: `darhanuva@gmail.com`", parse_mode="Markdown")
