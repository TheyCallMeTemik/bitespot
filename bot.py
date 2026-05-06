import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import stripe

# Stripe Secret Key (тестовый или реальный)
stripe.api_key = "sk_test_51TU1tk1DqzENdtT5xi0Ip0DTNUYdPJVguw6gNgkObtkOJxCS7cC12GxZsvC639NE28s4jJ80hzoZpTSxNvhhuaKG00gQGXyxbb"

TOKEN = "7828344943:AAFEvi8vIkcDFzmwtihn_HbzcZ1M8SN7esQ"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Главное меню
menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🍔 Найти дешёвую еду рядом")],
        [KeyboardButton(text="🔥 Сегодняшние акции")],
        [KeyboardButton(text="📍 Выбрать район")],
        [KeyboardButton(text="💼 Реклама для кафе")],
        [KeyboardButton(text="💳 Оплатить акцию")]
    ],
    resize_keyboard=True
)

# Меню выбора района с кнопкой возврата
districts_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Бостандыкский")],
        [KeyboardButton(text="Алмалинский")],
        [KeyboardButton(text="🔙 Главное меню")]
    ],
    resize_keyboard=True
)

# Данные кафе и ресторанов
places = [
    {"name": "MENDAL", "offer": "Бизнес-ланч — 3990 тг (Суп дня, котлеты, куриный шашлык, люля-кебаб, макароны, рис, чай, компот, баклава)", "district": "Бостандыкский", "promo": True, "daily": False},
    {"name": "Чачапури Абылайхан", "offer": "Скидка 10% на все позиции в течение 1 недели", "district": "Алмалинский", "promo": True, "daily": True},
    {"name": "Nuala", "offer": "Безлимитный формат на праздник 39 990 тг", "district": "Бостандыкский", "promo": True, "daily": False},
    {"name": "Wok Wok", "offer": "Скидка 15% на весь счет в день рождения", "district": "Алмалинский", "promo": False, "daily": False},
    {"name": "PerekysCity", "offer": "При покупке от 3500 тг дарим рожок с мороженым", "district": "Бостандыкский", "promo": False, "daily": True}
]

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    text = (
        "Привет! 👋 Я **BiteSpot** 🍔 — бот для поиска дешёвой еды рядом с университетом.\n\n"
        "Я помогу найти лучшие акции и предложения в кафе.\n"
        "Выберите нужную кнопку меню."
    )
    await message.answer(text, reply_markup=menu)

@dp.message(lambda message: message.text == "🍔 Найти дешёвую еду рядом")
async def cheap_food_handler(message: types.Message):
    sorted_places = sorted(places, key=lambda x: x["promo"], reverse=True)
    text = "🍔 Дешёвая еда рядом:\n\n"
    for i, place in enumerate(sorted_places, start=1):
        prefix = "🔥 Продвигаемое\n" if place["promo"] else ""
        text += f"{i}. {prefix}{place['name']} — {place['offer']}\nРайон: {place['district']}\n\n"
    await message.answer(text)

@dp.message(lambda message: message.text == "🔥 Сегодняшние акции")
async def daily_deals_handler(message: types.Message):
    deals = [place for place in places if place["daily"]]
    if not deals:
        await message.answer("Сегодня нет специальных акций. Загляните позже!")
        return
    text = "🔥 Сегодняшние акции:\n\n"
    for i, place in enumerate(deals, start=1):
        prefix = "⭐ Реклама\n" if place["promo"] else ""
        text += f"{i}. {prefix}{place['name']} — {place['offer']}\nРайон: {place['district']}\n\n"
    await message.answer(text)

@dp.message(lambda message: message.text == "📍 Выбрать район")
async def districts_handler(message: types.Message):
    text = "📍 В каком районе ищем еду?\n\nВыберите район:"
    await message.answer(text, reply_markup=districts_menu)

@dp.message(lambda message: message.text == "Бостандыкский")
async def bo_stan_handler(message: types.Message):
    filtered = [p for p in places if p["district"] == "Бостандыкский"]
    if not filtered:
        await message.answer("В Бостандыкском районе пока нет предложений.", reply_markup=districts_menu)
        return
    text = "🏙 Предложения в Бостандыкском районе:\n\n"
    for i, p in enumerate(filtered, 1):
        text += f"{i}. {p['name']} — {p['offer']}\n"
    await message.answer(text, reply_markup=districts_menu)

@dp.message(lambda message: message.text == "Алмалинский")
async def almaly_handler(message: types.Message):
    filtered = [p for p in places if p["district"] == "Алмалинский"]
    if not filtered:
        await message.answer("В Алмалинском районе пока нет предложений.", reply_markup=districts_menu)
        return
    text = "🏙 Предложения в Алмалинском районе:\n\n"
    for i, p in enumerate(filtered, 1):
        text += f"{i}. {p['name']} — {p['offer']}\n"
    await message.answer(text, reply_markup=districts_menu)

@dp.message(lambda message: message.text == "🔙 Главное меню")
async def back_to_menu(message: types.Message):
    await message.answer("Вы вернулись в главное меню.", reply_markup=menu)

@dp.message(lambda message: message.text == "💼 Реклама для кафе")
async def cafe_handler(message: types.Message):
    text = (
        "💼 Мы помогаем кафе привлекать студентов через бот!\n\n"
        "1. Размещение акций — 3000 тг/неделя\n"
        "2. Продвижение в топ — 5000 тг/неделя\n"
        "3. Рекламное место — 7000 тг\n\n"
        "Для оплаты нажмите кнопку «💳 Оплатить акцию» в главном меню."
    )
    await message.answer(text)

@dp.message(lambda message: message.text == "💳 Оплатить акцию")
async def payment_handler(message: types.Message):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': 'Размещение акции для кафе',
                        },
                        'unit_amount': 5000,  # 50.00 USD
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url='https://bitespot.space/payment/success',
            cancel_url='https://bitespot.space/payment/failed',
        )
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="💳 Перейти к оплате", url=session.url)]
        ])
        
        await message.answer(
            "Оплатите размещение акции. После успешной оплаты вы вернётесь на наш сайт.",
            reply_markup=keyboard
        )
    except Exception as e:
        await message.answer("❌ Произошла ошибка. Попробуйте позже.")
        print(f"Stripe error: {e}")

@dp.message()
async def unknown_message(message: types.Message):
    await message.answer("Пожалуйста, используйте кнопки меню. Нажмите /start для перезапуска.", reply_markup=menu)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
