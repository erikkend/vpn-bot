from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton


def create_invoice_keyboard(invoice_url):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Оплатить счет", url=invoice_url)]
    ])

    return markup


main_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="✏️Купить/Продлить ключ", callback_data='buy_key')],
    [InlineKeyboardButton(text="🔑Мой ключ", callback_data='my_key')],
    [InlineKeyboardButton(text="Контакты поддержки", callback_data="supp_contacts")]
])

price_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🥉 1 мес - 200 ₽", callback_data="tariff:1")],
    [InlineKeyboardButton(text="🥈 3 мес - 550 ₽", callback_data="tariff:2")],
    [InlineKeyboardButton(text="🥇 6 мес - 1000 ₽", callback_data="tariff:3")],
    [InlineKeyboardButton(text="🎖 12 мес - 1900 ₽", callback_data="tariff:4")],
])

regions_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🇩🇪 Германия', callback_data='region:GE'), InlineKeyboardButton(text='🇫🇷 Франция', callback_data='region:FR')],
    [InlineKeyboardButton(text='🇳🇱 Нидерланды', callback_data='region:NE'), InlineKeyboardButton(text='🇱🇻 Австрия', callback_data='region:AV')],
])
