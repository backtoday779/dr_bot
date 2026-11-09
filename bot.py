import asyncio
from datetime import datetime
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, FSInputFile, InputMediaPhoto
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

# ====== НАСТРОЙКИ ======
BOT_TOKEN = "9273998414:AAGRQnIAlP-UDzihzm8Pq0ObB5eohOumcTs" # ВСТАВЬ СВОЙ ТОКЕН, ЕСЛИ ИЗМЕНИЛ
ADMIN_ID = 464080782
PHOTO_PATH = "invite.jpg"
PHOTO_MESTO1 = "mesto1.jpg"
PHOTO_MESTO2 = "mesto2.jpg"

REMINDER_TIME = datetime(2026, 11, 19, 12, 0) 

# ТЕКСТЫ
TEXT_START = "" # ТУТ ПУСТО, ТЕКСТА НА АФИШЕ НЕ БУДЕТ

TEXT_MESTO = (
    "🎉 Приглашаю на мой День Рождения! 🎉\n\n"
    "📅 Когда: 21.11.2026 (суббота)\n"
    "📍 Где: Чайковичи, СО Рассвет 428\n\n"
    "Дорогой друг! Буду очень рад видеть тебя на моем празднике.\n"
    "Я не мог быть постоянно рядом. Но я никого не забыл. И вот мне исполняется 25 лет. Для меня - это подводящая круглая дата.\n\n"
    "Я арендовал отапливаемую беседку: Русская изба.\n"
    "Хочу коллективно отдохнуть в этот день, но в тоже время и дать жару, как раньше."
)

TEXT_DECLINE = (
    "Очень жаль! Я не забыл нашу дружбу! "
    "Всё же буду рад тебя видеть! 🥺"
)

TEXT_THINK = (
    "Хорошо! *Необходимо дать ответ не позже 14.11.2026*\n\n"
    "Напиши, пожалуйста, свое ФИО, чтобы я знал, кого ждать (если передумаешь):"
)

TEXT_BONUS = "Скоро тут будет инфа. 👀"
# ================================================

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

user_steps = {} 
user_info = {}
reminder_sent = False

# --- КЛАВИАТУРЫ ---
def start_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text="О, как!", callback_data="start_details")
    return kb.as_markup()

def details_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text="1) Газ!", callback_data="yes_come")
    kb.button(text="2) Думаю", callback_data="think_come")
    kb.button(text="3) У меня не получится:(", callback_data="no_come")
    kb.adjust(1)
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
    kb.button(text="🏋🏻 Другое / Не пью", callback_data="mydrink_custom")
    kb.adjust(2, 2, 2)
    return kb.as_markup()

def friend_drinks_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text="🏄🏿 Пиво", callback_data="frienddrink:Пиво")
    kb.button(text="🍷 Вино", callback_data="frienddrink:Вино")
    kb.button(text="🧞‍♂️ Водка", callback_data="frienddrink:Водка")
    kb.button(text="🧗🏻 Самогон", callback_data="frienddrink:Самогон")
    kb.button(text="🥤 Виски", callback_data="frienddrink:Виски")
    kb.button(text="🏋🏻 Другое / Не пью", callback_data="frienddrink_custom")
    kb.adjust(2, 2, 2)
    return kb.as_markup()

def final_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text="👀 А может тебе интересно?", callback_data="bonus_info")
    return kb.as_markup()

# --- ФОНОВАЯ РАССЫЛКА ---
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
                        await bot.send_photo(chat_id=user_id, photo=photo, caption="Привет! Напоминаю, что завтра мой День Рождения! 🥳\n📍 Чайковичи, СО Рассвет 428 (Русская изба)\n🕐 В 13:00\n\nЖду тебя! 🎉")
                        await asyncio.sleep(0.1)
                    except Exception:
                        pass
        await asyncio.sleep(60)

# --- ХЕНДЛЕРЫ ---

@dp.message(Command("start"))
async def cmd_start(message: Message):
    user_steps[message.from_user.id] = None
    user_info[message.from_user.id] = {}
    photo = FSInputFile(PHOTO_PATH)
    # Отправляем только фото и кнопку, без текста
    await message.answer_photo(photo=photo, reply_markup=start_kb())

@dp.callback_query(F.data == "start_details")
async def on_start_details(callback: CallbackQuery):
    # Отправляем 2 фото места (альбомом) с полным текстом
    media = [
        InputMediaPhoto(media=FSInputFile(PHOTO_MESTO1)),
        InputMediaPhoto(media=FSInputFile(PHOTO_MESTO2), caption=TEXT_MESTO)
    ]
    await callback.message.answer_media_group(media=media)
    
    # Следом вопрос с кнопками
    await callback.message.answer("Ты со мной?", reply_markup=details_kb())
    await callback.answer()

@dp.callback_query(F.data == "yes_come")
async def on_yes_come(callback: CallbackQuery):
    user_steps[callback.from_user.id] = "wait_fio"
    await callback.message.answer("Супер! Напиши, пожалуйста, свое ФИО (полностью):")
    await callback.answer()

@dp.callback_query(F.data == "think_come")
async def on_think_come(callback: CallbackQuery):
    user_steps[callback.from_user.id] = "wait_fio"
    await callback.message.answer(TEXT_THINK, parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data == "no_come")
async def on_no_come(callback: CallbackQuery):
    await callback.message.answer(TEXT_DECLINE)
    await callback.answer()
    user = callback.from_user
    await bot.send_message(ADMIN_ID, f"❌ *{user.full_name}* (@{user.username or '—'}) не придёт.", parse_mode="Markdown")

# --- ОБРАБОТКА ТЕКСТА ---
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
        await message.answer("Супер! Всё записал, буду ждать тебя! 🎉", reply_markup=final_kb())
        await message.answer("На всякий случай напомню тебе 19.11.2026 🎂")
        
        info = user_info.get(user_id, {})
        admin_msg = f"✅ Придёт: *{info.get('fio', '—')}* (@{message.from_user.username or '—'})\n"
        admin_msg += f"🕐 Время: *{info.get('arrival_time', '13:00')}*\n"
        if info.get("plus_one") and info.get("plus_one") != "yes":
            admin_msg += f"👫 С ним/ней: *{info['plus_one']}*\n"
            admin_msg += f"🍹 Напиток гостя: *{info.get('my_drink')}*\n"
            admin_msg += f"🍹 Напиток спутника: *{info.get('friend_drink')}*\n"
        else:
            admin_msg += f"🍹 Напиток: *{info.get('my_drink')}*\n"
        admin_msg += f"💬 Пожелания: *{message.text}*"
        await bot.send_message(ADMIN_ID, admin_msg, parse_mode="Markdown")
        user_steps[user_id] = "done"

# --- ВРЕМЯ И НАПИТКИ ---
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
    my_drink = callback.data.split(":", 1)[1]
    user_info[user_id]["my_drink"] = my_drink
    
    user_steps[user_id] = "wait_plus_name" 
    await callback.message.answer(f"Записал, ты пьёшь: *{my_drink}* 🥂\n\nНапиши имя твоего спутника (текстом, если один — напиши «Один»):", parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data.startswith("frienddrink:"))
async def on_friend_drink(callback: CallbackQuery):
    user_id = callback.from_user.id
    friend_drink = callback.data.split(":", 1)[1]
    user_info[user_id]["friend_drink"] = friend_drink
    user_steps[user_id] = "preferences"
    await callback.message.answer(f"Записал! Твой спутник пьёт: *{friend_drink}* 🥂\n\nОтлично! У тебя есть какие-то предпочтения?\nНапример: Баня, караоке, горячий шашлык 👇", parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data == "bonus_info")
async def on_bonus_info(callback: CallbackQuery):
    await callback.message.answer(TEXT_BONUS)
    await callback.answer()

# --- АДМИН-ПАНЕЛЬ ---
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
            if a.get('plus_one') and a.get('plus_one') != "yes" and a.get('plus_one').lower() != "один":
                lines.append(f"✅ {fio} (в {time}) + {a['plus_one']} — {a.get('my_drink')} / {a.get('friend_drink')} (Пожелания: {pref})")
            else:
                lines.append(f"✅ {fio} (в {time}) — {a.get('my_drink')} (Пожелания: {pref})")
    await message.answer("\n".join(lines), parse_mode="Markdown")

async def main():
    asyncio.create_task(reminder_loop())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())