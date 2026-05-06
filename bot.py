import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import stripe

# Тестовый Secret Key для Stripe
stripe.api_key = "sk_test_51TU1tk1DqzENdtT5xi0Ip0DTNUYdPJVguw6gNgkObtkOJxCS7cC12GxZsvC639NE28s4jJ80hzoZpTSxNvhhuaKG00gQGXyxbb"  # <-- Вставь свой Secret Key

TOKEN = "7828344943:AAFEvi8vIkcDFzmwtihn_HbzcZ1M8SN7esQ"  # Токен от BotFather для вашего бота

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Кнопки
menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🍔 Найти дешёвую еду рядом")],
        [KeyboardButton(text="🔥 Сегодняшние акции")],
        [KeyboardButton(text="📍 Выбрать район")],
        [KeyboardButton(text="💼 Реклама для кафе")]
    ],
    resize_keyboard=True
)

# Районы для выбора
districts_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Бостандыкский")],
        [KeyboardButton(text="Алмалинский")]
    ],
    resize_keyboard=True
)

# Реальные кафе и рестораны рядом с КБТУ
places = [
    {"name": "MENDAL", "offer": "Бизнес-ланч — 3990 тг (Суп дня, котлеты, куриный шашлык, люля-кебаб, макароны, рис, чай, компот, баклава)", "district": "Бостандыкский", "promo": True, "daily": False},
    {"name": "Чачапури Абылайхан", "offer": "Скидка 10% на все позиции в течение 1 недели", "district": "Алмалинский", "promo": True, "daily": True},
    {"name": "Nuala", "offer": "Безлимитный формат на праздник 39 990 тг", "district": "Бостандыкский", "promo": True, "daily": False},
    {"name": "Wok Wok", "offer": "Скидка 15% на весь счет в день рождения", "district": "Алмалинский", "promo": False, "daily": False},
    {"name": "PerekysCity", "offer": "При покупке от 3500 тг дарим рожок с мороженым", "district": "Бостандыкский", "promo": False, "daily": True}
]

# Основная логика бота
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    text = (
        "Привет! 👋 Я **BiteSpot** 🍔 — бот для поиска дешёвой еды рядом с университетом. Я помогу найти лучшие акции и предложения в кафе!\n\n"
        "Вот что я могу:\n\n"
        "• **Найти дешёвые предложения рядом** – покажу вам все дешёвые кафе и рестораны рядом с вами!\n"
        "• **Посмотреть акции на сегодня** – выберите этот пункт, чтобы увидеть актуальные скидки и предложения!\n"
        "• **Выбрать район** – если вы хотите, чтобы я показывал предложения только в определённом районе.\n\n"
        "Просто выбери нужную кнопку, и я покажу лучшие предложения! 😄"
    )
    await message.answer(text, reply_markup=menu)

# Обработка кнопки "Дешево рядом"
@dp.message(lambda message: message.text == "🍔 Найти дешёвую еду рядом")
async def cheap_food_handler(message: types.Message):
    sorted_places = sorted(places, key=lambda x: x["promo"], reverse=True)

    text = "🍔 Дешёвая еда рядом:\n\n"
    for i, place in enumerate(sorted_places, start=1):
        prefix = "🔥 Продвигаемое\n" if place["promo"] else ""
        text = f"{i}. {prefix}{place['name']} — {place['offer']}\nРайон: {place['district']}\n\n"
        await message.answer(text)

# Обработка кнопки "Сегодняшние акции"
@dp.message(lambda message: message.text == "🔥 Сегодняшние акции")
async def daily_deals_handler(message: types.Message):
    deals = [place for place in places if place["daily"]]

    text = "🔥 Сегодняшние акции:\n\n"
    for i, place in enumerate(deals, start=1):
        prefix = "⭐ Реклама\n" if place["promo"] else ""
        text += f"{i}. {prefix}{place['name']} — {place['offer']}\nРайон: {place['district']}\n\n"

    await message.answer(text)

# Обработка кнопки "Выбрать район"
@dp.message(lambda message: message.text == "📍 Выбрать район")
async def districts_handler(message: types.Message):
    text = (
        "📍 В каких районах ищем еду?\n\n"
        "Выберите район, чтобы найти кафе с лучшими предложениями рядом!"
    )
    await message.answer(text, reply_markup=districts_menu)

# Обработка кнопки "Реклама для кафе"
@dp.message(lambda message: message.text == "💼 Реклама для кафе")
async def cafe_handler(message: types.Message):
    text = (
        "💼 Мы помогаем кафе привлекать студентов через бот! Вот как это работает:\n\n"
        "1. Размещение ваших акций — всего **3000 тг** за неделю\n"
        "2. Продвижение в топ — **5000 тг** за неделю\n"
        "3. Рекламное место — **7000 тг**\n\n"
        "Напишите нам, и мы разместим ваши предложения прямо в боте!"
    )
    await message.answer(text)

# Интеграция с Stripe для приема оплаты
@dp.message(lambda message: message.text == "💳 Оплатить акцию")
async def payment_handler(message: types.Message):
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'Размещение акции для кафе',
                    },
                    'unit_amount': 5000,  # Пример суммы для размещения акции
                },
                'quantity': 1,
            },
        ],
        mode='payment',
        success_url='https://ваш_сайт.com/success',
        cancel_url='https://ваш_сайт.com/cancel',
    )

    # Отправка ссылки для оплаты
    await message.answer(f"Пожалуйста, оплатите за размещение акции: {session.url}")

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
