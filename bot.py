import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = "7828344943:AAFEvi8vIkcDFzmwtihn_HbzcZ1M8SN7esQ"

bot = Bot(token=TOKEN)
dp = Dispatcher()

menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🍔 Дешево рядом")],
        [KeyboardButton(text="🔥 Сегодняшние акции")],
        [KeyboardButton(text="📍 Районы")],
        [KeyboardButton(text="💼 Для кафе")]
    ],
    resize_keyboard=True
)

places = [
    {
        "name": "Student Food",
        "offer": "Бургер 1200 тг",
        "district": "Бостандыкский",
        "promo": False,
        "daily": False
    },
    {
        "name": "Doner Hub",
        "offer": "Донер 900 тг",
        "district": "Алмалинский",
        "promo": False,
        "daily": False
    },
    {
        "name": "Pizza Time",
        "offer": "2 куска пиццы за 1000 тг",
        "district": "Бостандыкский",
        "promo": True,
        "daily": True
    },
    {
        "name": "Burger Lab",
        "offer": "Бургер -30%",
        "district": "Ауэзовский",
        "promo": True,
        "daily": True
    },
    {
        "name": "Fast Pasta",
        "offer": "Паста 1100 тг",
        "district": "Алмалинский",
        "promo": False,
        "daily": False
    },
    {
        "name": "Sushi Box",
        "offer": "Сет 2500 тг",
        "district": "Бостандыкский",
        "promo": False,
        "daily": True
    }
]


@dp.message(Command("start"))
async def start_handler(message: types.Message):
    text = (
        "Привет! Я BiteSpot 🍔\n\n"
        "Помогаю студентам находить дешёвую еду рядом и актуальные акции.\n"
        "Выбери нужный раздел:"
    )
    await message.answer(text, reply_markup=menu)


@dp.message(lambda message: message.text == "🍔 Дешево рядом")
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

    text = "🔥 Сегодняшние акции:\n\n"
    for i, place in enumerate(deals, start=1):
        prefix = "⭐ Реклама\n" if place["promo"] else ""
        text += f"{i}. {prefix}{place['name']} — {place['offer']}\nРайон: {place['district']}\n\n"

    await message.answer(text)


@dp.message(lambda message: message.text == "📍 Районы")
async def districts_handler(message: types.Message):
    text = (
        "📍 Районы:\n\n"
        "• Бостандыкский\n"
        "• Алмалинский\n"
        "• Ауэзовский\n\n"
        "В MVP это демонстрационный список районов."
    )
    await message.answer(text)


@dp.message(lambda message: message.text == "💼 Для кафе")
async def cafe_handler(message: types.Message):
    text = (
        "💼 Размещение для кафе:\n\n"
        "• Размещение акции — 3000 тг / неделя\n"
        "• Продвижение в топе — 5000 тг / неделя\n"
        "• Рекламное место — 7000 тг / неделя\n\n"
        "Для сотрудничества: @hotboynonetvoi"
    )
    await message.answer(text)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())