import asyncio
from datetime import datetime
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

# ====== НАСТРОЙКИ ======
BOT_TOKEN = "9273998414:AAGRQnIAlP-UDzihzm8Pq0ObB5eohOumcTs"
ADMIN_ID = 464080782
PHOTO_PATH = "invite.jpg"

REMINDER_TIME = datetime(2026, 11, 19, 12, 0) 

INVITE_TEXT = (
    "🎉 Приглашаю на мой День Рождения! 🎉\n\n"
    "Дорогой друг! Буду очень рад видеть тебя на моем празднике.\n\n"
    "Я не мог быть постоянно рядом. Но я никого не забыл. И вот мне исполняется 25 лет. Для меня - это подводящая круглая дата. \n\n"
    "📅 Когда: 21.11.2026 (суббота)\n"
    "📍 Где: СО Рассвет, 428\n\n"
    "Я арендовал отапливаемую беседку: Русская изба. \n\n"
    "Хочу коллективно отдохнуть в этот день, но в тоже время и дать жару. \n\n"
    "Подтверди, пожалуйста, придёшь ли ты 👇"
)

DECLINE_TEXT = (
    "Очень жаль! Я не забыл нашу дружбу! "
    "Всё же буду рад тебя видеть! 🥺"
)
# ================================================

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

user_steps = {} 
user_info = {}
reminder_sent = False

def start_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text="✅ Приду один", callback_data="come")
    kb.button(text="👫 Приду не один", callback_data="come_plus")
    kb.button(text="❌ Не приду", callback_data="decline")
    kb.adjust(2, 1)
    return kb.as_markup()

def time_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text="✅ Успеваю к 13:00", callback_data="time_yes")
    kb.button(text="⏰ Буду позже", callback_data="time_no")
    kb.adjust(1)
    return kb.as_markup()

def my_drinks_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text="🏄🏿 Пиво", callback_data="mydrink:Пиво")
    kb.button(text="🍷 Вино", callback_data="mydrink:Вино")
    kb.button(text="🧞‍♂️ Водка", callback_data="mydrink:Водка")
    kb.button(text="🧗🏻 Самогон", callback_data="mydrink:Самогон")
    kb.button(text="🥤 Виски", callback_data="mydrink:Виски")
    kb.button(text="🏋🏻 Другое / Не пью", callback_data="mydrink_custom") # Изменили на mydrink_custom для надежности
    kb.adjust(2, 2, 2)
    return kb.as_markup()

def friend_drinks_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text="🏄🏿 Пиво", callback_data="frienddrink:Пиво")
    kb.button(text="🍷 Вино", callback_data="frienddrink:Вино")
    kb.button(text="🧞‍♂️ Водка", callback_data="frienddrink:Водка")
    kb.button(text="🧗🏻 Самогон", callback_data="frienddrink:Самогон")
    kb.button(text="🥤 Виски", callback_data="frienddrink:Виски")
    kb.button(text="🏋🏻 Другое / Не пью", callback_data="frienddrink_custom") # Изменили на frienddrink_custom
    kb.adjust(2, 2, 2)
    return kb.as_markup()

async def reminder_loop():
    global reminder_sent
    while True:
        now = datetime.now()
        if now >= REMINDER_TIME and not reminder_sent:
            print("Отправляю напоминания...")
            reminder_sent = True
            photo = FSInputFile(PHOTO_PATH)
            
            for user_id, info in user_info.items():
                if info.get("preferences"):
                    try:
                        await bot.send_photo(
                            chat_id=user_id,
                            photo=photo,
                            caption=(
                                "Привет! Напоминаю, что завтра мой День Рождения! 🥳\n\n"
                                "📍 Место: СО Рассвет, 428 (Беседка: Русская изба)\n"
                                "🕐 Встречаемся в 13:00\n\n"
                                "Жду тебя, ничего не забудь! 🎉"
                            )
                        )
                        await asyncio.sleep(0.1)
                    except Exception as e:
                        print(f"Не смог отправить сообщение {user_id}: {e}")
        await asyncio.sleep(60)

@dp.message(Command("start"))
async def cmd_start(message: Message):
    user_steps[message.from_user.id] = None
    user_info[message.from_user.id] = {}
    photo = FSInputFile(PHOTO_PATH)
    await message.answer_photo(photo=photo, caption=INVITE_TEXT, reply_markup=start_kb())

@dp.callback_query(F.data == "decline")
async def on_decline(callback: CallbackQuery):
    user_steps[callback.from_user.id] = None
    await callback.message.answer(DECLINE_TEXT)
    await callback.answer()
    user = callback.from_user
    await bot.send_message(ADMIN_ID, f"❌ *{user.full_name}* (@{user.username or '—'}) не придёт.", parse_mode="Markdown")

@dp.callback_query(F.data == "come")
async def on_come(callback: CallbackQuery):
    user_steps[callback.from_user.id] = "wait_fio"
    user_info[callback.from_user.id] = {"plus_one": None}
    await callback.message.answer("Отлично! 🎉 Напиши, пожалуйста, свое ФИО (полностью):")
    await callback.answer()

@dp.callback_query(F.data == "come_plus")
async def on_come_plus(callback: CallbackQuery):
    user_steps[callback.from_user.id] = "wait_fio"
    user_info[callback.from_user.id] = {"plus_one": "yes"}
    await callback.message.answer("Отлично! 🎉 Напиши, пожалуйста, свое ФИО (полностью):")
    await callback.answer()

@dp.callback_query(F.data == "time_yes")
async def on_time_yes(callback: CallbackQuery):
    user_steps[callback.from_user.id] = "my_drink"
    user_info[callback.from_user.id]["arrival_time"] = "13:00"
    await callback.message.answer("Супер, записал! А что пьёшь ты? 👇", reply_markup=my_drinks_kb())
    await callback.answer()

@dp.callback_query(F.data == "time_no")
async def on_time_no(callback: CallbackQuery):
    user_steps[callback.from_user.id] = "wait_custom_time"
    await callback.message.answer("Понял! Во сколько ты будешь? (напиши время текстом, например: 14:30)")
    await callback.answer()

# --- ОБРАБОТЧИКИ ТЕКСТА ---
@dp.message(F.text & ~F.text.startswith("/"))
async def handle_text(message: Message):
    user_id = message.from_user.id
    step = user_steps.get(user_id)
    
    if step == "wait_fio":
        user_info[user_id]["fio"] = message.text
        user_steps[user_id] = "wait_time"
        await message.answer(f"Записал! *{message.text}*.\n\n🕐 Время встречи в 13:00.\nУспеваешь к этому времени?", parse_mode="Markdown", reply_markup=time_kb())
    
    elif step == "wait_custom_time":
        user_info[user_id]["arrival_time"] = message.text
        user_steps[user_id] = "my_drink"
        await message.answer(f"Записал, будешь в *{message.text}*! А что пьёшь ты? 👇", parse_mode="Markdown", reply_markup=my_drinks_kb())

    elif step == "wait_custom_my_drink":
        user_info[user_id]["my_drink"] = message.text
        if user_info[user_id].get("plus_one") == "yes":
            user_steps[user_id] = "wait_plus_name"
            await message.answer(f"Записал, ты будешь пить: *{message.text}*.\n\nНапиши имя твоего спутника (текстом):", parse_mode="Markdown")
        else:
            user_steps[user_id] = "preferences"
            await message.answer(f"Записал! Ты пьёшь: *{message.text}* 🥂\n\nОтлично! У тебя есть какие-то предпочтения?\nНапример: Баня, караоке, горячий шашлык 👇", parse_mode="Markdown")

    elif step == "wait_plus_name":
        user_info[user_id]["plus_one"] = message.text
        user_steps[user_id] = "friend_drink"
        await message.answer(f"Записал! Твой спутник: *{message.text}*.\nА что он(а) пьёт? 👇", parse_mode="Markdown", reply_markup=friend_drinks_kb())

    elif step == "wait_custom_friend_drink":
        user_info[user_id]["friend_drink"] = message.text
        user_steps[user_id] = "preferences"
        await message.answer(f"Записал! Твой спутник пьёт: *{message.text}* 🥂\n\nОтлично! У тебя есть какие-то предпочтения?\nНапример: Баня, караоке, горячий шашлык 👇", parse_mode="Markdown")
    
    elif step == "preferences":
        user_info[user_id]["preferences"] = message.text
        await message.answer("Супер! Всё записал, буду ждать тебя! 🎉")
        await message.answer("На всякий случай напомню тебе 19.11.2026 🎂")
        
        info = user_info.get(user_id, {})
        admin_msg = f"✅ Придёт: *{info.get('fio', '—')}* (@{message.from_user.username or '—'})\n"
        admin_msg += f"🕐 Время: *{info.get('arrival_time', '13:00')}*\n"
        
        if info.get("plus_one") and info.get("plus_one") != "yes":
            admin_msg += f"👫 С ним/ней: *{info['plus_one']}*\n"
            admin_msg += f"🍹 Его/её напиток: *{info.get('my_drink')}*\n"
            admin_msg += f"🍹 Напиток спутника: *{info.get('friend_drink')}*\n"
        else:
            admin_msg += f"🍹 Напиток: *{info.get('my_drink')}*\n"
            
        admin_msg += f"💬 Пожелания: *{message.text}*"
        await bot.send_message(ADMIN_ID, admin_msg, parse_mode="Markdown")
        user_steps[user_id] = "done"

# --- КНОПКИ НАПИТКОВ ---
@dp.callback_query(F.data == "mydrink_custom")
async def on_my_drink_custom(callback: CallbackQuery):
    user_steps[callback.from_user.id] = "wait_custom_my_drink"
    await callback.message.answer("Напиши, пожалуйста, что ты будешь пить (или напиши «Не пью»):")
    await callback.answer()

@dp.callback_query(F.data == "frienddrink_custom")
async def on_friend_drink_custom(callback: CallbackQuery):
    user_steps[callback.from_user.id] = "wait_custom_friend_drink"
    await callback.message.answer("Напиши, пожалуйста, что будет пить твой спутник:")
    await callback.answer()

@dp.callback_query(F.data.startswith("mydrink:"))
async def on_my_drink(callback: CallbackQuery):
    user_id = callback.from_user.id
    if user_steps.get(user_id) != "my_drink":
        await callback.answer("Сначала ответь на предыдущий вопрос!", show_alert=True)
        return
    
    my_drink = callback.data.split(":", 1)[1]
    user_info[user_id]["my_drink"] = my_drink
    
    if user_info[user_id].get("plus_one") == "yes":
        user_steps[user_id] = "wait_plus_name"
        await callback.message.answer(f"Записал, ты пьёшь: *{my_drink}* 🥂\n\nНапиши имя твоего спутника (текстом):", parse_mode="Markdown")
    else:
        user_steps[user_id] = "preferences"
        await callback.message.answer(f"Записал! Ты пьёшь: *{my_drink}* 🥂\n\nОтлично! У тебя есть какие-то предпочтения?\nНапример: Баня, караоке, горячий шашлык 👇", parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data.startswith("frienddrink:"))
async def on_friend_drink(callback: CallbackQuery):
    user_id = callback.from_user.id
    friend_drink = callback.data.split(":", 1)[1]
    user_info[user_id]["friend_drink"] = friend_drink
    user_steps[user_id] = "preferences"
    
    await callback.message.answer(f"Записал! Твой спутник пьёт: *{friend_drink}* 🥂\n\nОтлично! У тебя есть какие-то предпочтения?\nНапример: Баня, караоке, горячий шашлык 👇", parse_mode="Markdown")
    await callback.answer()

@dp.message(Command("list"))
async def cmd_list(message: Message):
    if message.from_user.id != ADMIN_ID: return
    if not user_info: return await message.answer("Пока никто не ответил.")
    lines = ["📋 *Ответы гостей:*\n"]
    for uid, a in user_info.items():
        if a.get("preferences"):
            pref = a.get('preferences', '—')
            fio = a.get('fio', '—')
            time = a.get('arrival_time', '13:00')
            if a.get('plus_one') and a.get('plus_one') != "yes":
                lines.append(f"✅ {fio} (в {time}) + {a['plus_one']} — {a.get('my_drink')} / {a.get('friend_drink')} (Пожелания: {pref})")
            else:
                lines.append(f"✅ {fio} (в {time}) — {a.get('my_drink')} (Пожелания: {pref})")
    await message.answer("\n".join(lines), parse_mode="Markdown")

async def main():
    asyncio.create_task(reminder_loop())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())