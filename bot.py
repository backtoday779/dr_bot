import asyncio
from datetime import datetime
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, FSInputFile, InputMediaPhoto
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

# ====== НАСТРОЙКИ ======
BOT_TOKEN = "9273998414:AAGRQnIAlP-UDzihzm8Pq0ObB5eohOumcTs"
ADMIN_ID = 464080782
PHOTO_PATH = "invite.jpg"
PHOTO_MESTO1 = "mesto1.jpg"
PHOTO_MESTO2 = "mesto2.jpg"

REMINDER_TIME = datetime(2026, 11, 18, 12, 0) 

# ====== ТЕКСТЫ ======
TEXT_LYRICS = (
    "💽 *press2p - snowfall*\n\n"
    "Я бы опять поднял пластмассовый стакан\n"
    "Прошёлся по всем именам, даже тем, кого запамятовал\n"
    "*По тем, чьи лица годы не видал*\n"
    "*Я скучал, хранил, любил и ждал*"
)

TEXT_MESTO = (
    "📅 Когда: 21.11.2026 (суббота)\n"
    "📍 Где: Чайковичи, СО Рассвет 428\n\n"
    "Я арендовал отапливаемую беседку: Русская изба.\n"
    "Хочу коллективно отдохнуть в этот день, но в тоже время и дать жару, как раньше.\n\n"
    "Дорогой друг! Буду очень рад видеть тебя на моем празднике.\n\n"
    "Я не мог быть постоянно рядом.\n"
    "Но я никого не забыл.\n\n"
    "И вот мне исполняется 25 лет.\n" 
    "Для меня - это подводящая круглая дата."
)

TEXT_FINAL_INFO = (
    "📅 Когда: 21.11.2026 (суббота)\n"
    "🏠 Беседка: Русская изба.\n"
    "📍 Где: Чайковичи, СО Рассвет 428\n"
    "🕐 Время встречи: 13:00"
)

TEXT_DECLINE = "Очень жаль! Я не забыл нашу дружбу! Всё же буду рад тебя видеть! 🥺"

# 🔥 НОВЫЙ ТЕКСТ, КОТОРЫЙ ПРИДЕТ В КОНЦЕ
TEXT_FINAL_BONUS = (
    "На День Рождение жду с хорошим настроением!\n"
    "Но если будет плохое, не беда, исправим! \n"
    "Стиль одежды не трактую. \n"
    "Сам буду в деловом.\n\n"
    "*Любая творческая инициатива приветствуется! \n"
    "Дай знать если есть идея: __словом «Идея»__ в личку._\n"
    "*Свяжу с ответственным лицом!*\n\n"
    "Решил крепко заморочиться.\n"
    "Детали - это важно. \n"
    "Сделал акцент на каждой мелочи (от кода до визуала).\n"
    "Бота написал на 90% своими силами. \n\n"
    "Спасибо, что листаешь до конца! \n"
    "До встречи, друг! 🤍"
)

TEXT_REMINDER = "Привет! Напоминаю, что послезавтра, 21 ноября, мой День Рождения! 🥳\n📍 Место: Чайковичи, СО Рассвет 428 (Беседка: Русская изба)\n🕐 Встречаемся в 13:00\n\nЖду тебя, ничего не забудь! 🎉"

# ================================================

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

user_steps = {} 
user_info = {}
bot_messages = {} 
reminder_sent = False

# --- КЛАВИАТУРЫ ---
def start_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text="О, как!", callback_data="start_details")
    return kb.as_markup()

def details_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text="Газ!", callback_data="yes_come")
    kb.button(text="Думаю", callback_data="think_come")
    kb.button(text="У меня не получится:(", callback_data="no_come")
    kb.adjust(1)
    return kb.as_markup()

def alone_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text="Один", callback_data="alone_yes")
    kb.button(text="Не один", callback_data="alone_no")
    kb.adjust(2)
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
    kb.button(text="🥂 Шампанское", callback_data="mydrink:Шампанское")
    kb.button(text="🍷 Вино", callback_data="mydrink:Вино")
    kb.button(text="🧞‍♂️ Водка", callback_data="mydrink:Водка")
    kb.button(text="🧗🏻 Самогон", callback_data="mydrink:Самогон")
    kb.button(text="🥤 Виски", callback_data="mydrink:Виски")
    kb.button(text="🏋🏻 Другое / Не пью", callback_data="mydrink_custom")
    kb.adjust(2, 2, 2, 1)
    return kb.as_markup()

def friend_drinks_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text="🏄🏿 Пиво", callback_data="frienddrink:Пиво")
    kb.button(text="🥂 Шампанское", callback_data="frienddrink:Шампанское")
    kb.button(text="🍷 Вино", callback_data="frienddrink:Вино")
    kb.button(text="🧞‍♂️ Водка", callback_data="frienddrink:Водка")
    kb.button(text="🧗🏻 Самогон", callback_data="frienddrink:Самогон")
    kb.button(text="🥤 Виски", callback_data="frienddrink:Виски")
    kb.button(text="🏋🏻 Другое / Не пью", callback_data="frienddrink_custom")
    kb.adjust(2, 2, 2, 1)
    return kb.as_markup()

def restart_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text="🔄 Начать заново", callback_data="restart")
    return kb.as_markup()

# --- УТИЛИТА ДЛЯ УДАЛЕНИЯ МУСОРА ---
async def delete_prev_messages(chat_id):
    if chat_id in bot_messages:
        for msg in bot_messages[chat_id]:
            try:
                await bot.delete_message(chat_id, msg.message_id)
            except Exception:
                pass
        bot_messages[chat_id] = []
    else:
        bot_messages[chat_id] = []

async def send_bot_message(chat_id, text, reply_markup=None, parse_mode=None):
    msg = await bot.send_message(chat_id, text, reply_markup=reply_markup, parse_mode=parse_mode)
    if chat_id not in bot_messages:
        bot_messages[chat_id] = []
    bot_messages[chat_id].append(msg)
    return msg

# --- ФОНОВАЯ РАССЫЛКА ---
async def reminder_loop():
    global reminder_sent
    while True:
        now = datetime.now()
        if now >= REMINDER_TIME and not reminder_sent:
            reminder_sent = True
            photo = FSInputFile(PHOTO_PATH)
            for user_id, info in user_info.items():
                if info.get("preferences"):
                    try:
                        await bot.send_photo(chat_id=user_id, photo=photo, caption=TEXT_REMINDER)
                        await asyncio.sleep(0.1)
                    except Exception:
                        pass
        await asyncio.sleep(60)

# --- ХЕНДЛЕРЫ ---

@dp.message(Command("start"))
async def cmd_start(message: Message):
    user_steps[message.from_user.id] = None
    user_info[message.from_user.id] = {}
    await delete_prev_messages(message.from_user.id)
    
    photo = FSInputFile(PHOTO_PATH)
    msg_photo = await message.answer_photo(photo=photo)
    if message.from_user.id not in bot_messages:
        bot_messages[message.from_user.id] = []
    bot_messages[message.from_user.id].append(msg_photo)
    
    await send_bot_message(
        message.from_user.id, 
        TEXT_LYRICS, 
        reply_markup=start_kb(), 
        parse_mode="Markdown"
    )

@dp.callback_query(F.data == "start_details")
async def on_start_details(callback: CallbackQuery):
    await delete_prev_messages(callback.from_user.id)
    
    media = [
        InputMediaPhoto(media=FSInputFile(PHOTO_MESTO1)),
        InputMediaPhoto(media=FSInputFile(PHOTO_MESTO2))
    ]
    msg_album = await callback.message.answer_media_group(media=media)
    
    if callback.from_user.id not in bot_messages:
        bot_messages[callback.from_user.id] = []
    for m in msg_album:
        bot_messages[callback.from_user.id].append(m)

    await send_bot_message(callback.from_user.id, TEXT_MESTO, reply_markup=details_kb())
    await callback.answer()

# --- ВЕТКА "ГАЗ" ---
@dp.callback_query(F.data == "yes_come")
async def on_yes_come(callback: CallbackQuery):
    await delete_prev_messages(callback.from_user.id)
    user_info[callback.from_user.id] = {"fio": ""} 
    await send_bot_message(callback.from_user.id, "Ты будешь один или с кем-то?", reply_markup=alone_kb())
    await callback.answer()

@dp.callback_query(F.data == "alone_yes")
async def on_alone_yes(callback: CallbackQuery):
    await delete_prev_messages(callback.from_user.id)
    user_info[callback.from_user.id]["plus_one"] = None
    user_steps[callback.from_user.id] = "wait_fio"
    await send_bot_message(callback.from_user.id, "Супер! Напиши, пожалуйста, свое ФИО (полностью):")
    await callback.answer()

@dp.callback_query(F.data == "alone_no")
async def on_alone_no(callback: CallbackQuery):
    await delete_prev_messages(callback.from_user.id)
    user_info[callback.from_user.id]["plus_one"] = "yes"
    user_steps[callback.from_user.id] = "wait_fio"
    await send_bot_message(callback.from_user.id, "Супер! Напиши, пожалуйста, свое ФИО (полностью):")
    await callback.answer()

# --- ВЕТКА "ДУМАЮ" ---
@dp.callback_query(F.data == "think_come")
async def on_think_come(callback: CallbackQuery):
    await delete_prev_messages(callback.from_user.id) 
    user_steps[callback.from_user.id] = "wait_fio_think"
    await send_bot_message(callback.from_user.id, "Напиши, пожалуйста, свое ФИО:")
    await callback.answer()

# --- ВЕТКА "НЕ ПРИДУ" ---
@dp.callback_query(F.data == "no_come")
async def on_no_come(callback: CallbackQuery):
    await delete_prev_messages(callback.from_user.id) 
    await send_bot_message(callback.from_user.id, TEXT_DECLINE, reply_markup=restart_kb())
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
        await delete_prev_messages(user_id)
        await send_bot_message(user_id, "🕐 Время встречи в 13:00.\nУспеваешь к этому времени?", reply_markup=time_kb())

    elif step == "wait_fio_think":
        user_info[user_id]["fio"] = message.text
        user_steps[user_id] = "wait_date_think"
        await delete_prev_messages(user_id)
        await send_bot_message(user_id, "Когда дашь ответ? (напиши дату текстом).\nИнформацию нужно предоставить до 15.11.2026.")

    elif step == "wait_date_think":
        user_info[user_id]["think_date"] = message.text
        user_steps[user_id] = None
        await delete_prev_messages(user_id)
        await send_bot_message(user_id, "Скорее возвращайся с обратной связью! 👋", reply_markup=restart_kb())
        
        info = user_info[user_id]
        await bot.send_message(ADMIN_ID, f"🤔 *{info['fio']}* думает и даст ответ *{info['think_date']}*", parse_mode="Markdown")

    elif step == "wait_custom_time":
        user_info[user_id]["arrival_time"] = message.text
        user_steps[user_id] = "my_drink"
        await delete_prev_messages(user_id)
        await send_bot_message(user_id, "А что пьёшь ты? 👇", reply_markup=my_drinks_kb())

    elif step == "wait_custom_my_drink":
        user_info[user_id]["my_drink"] = message.text
        await delete_prev_messages(user_id)
        if user_info[user_id].get("plus_one") == "yes":
            user_steps[user_id] = "wait_plus_name"
            await send_bot_message(user_id, "Напиши имя твоего спутника (текстом):")
        else:
            user_steps[user_id] = "preferences"
            await send_bot_message(user_id, "Отлично! У тебя есть какие-то предпочтения?\nНапример: Баня, караоке, горячий шашлык 👇")

    elif step == "wait_plus_name":
        user_info[user_id]["plus_one_name"] = message.text
        user_steps[user_id] = "friend_drink"
        await delete_prev_messages(user_id)
        await send_bot_message(user_id, "А что он(а) пьёт? 👇", reply_markup=friend_drinks_kb())

    elif step == "wait_custom_friend_drink":
        user_info[user_id]["friend_drink"] = message.text
        user_steps[user_id] = "preferences"
        await delete_prev_messages(user_id)
        await send_bot_message(user_id, "Отлично! У тебя есть какие-то предпочтения?\nНапример: Баня, караоке, горячий шашлык 👇")
    
    elif step == "preferences":
        user_info[user_id]["preferences"] = message.text
        
        # 1. Удаляем всё
        await delete_prev_messages(user_id)
        
        # 2. Присылаем заново афишу
        photo = FSInputFile(PHOTO_PATH)
        msg_photo = await message.answer_photo(photo=photo)
        bot_messages[user_id].append(msg_photo)
        
        # 3. Присылаем текст с датой/местом/временем
        await send_bot_message(user_id, TEXT_FINAL_INFO)
        
        # 4. Присылаем финальный красивый текст (без кнопки)
        await send_bot_message(user_id, TEXT_FINAL_BONUS, parse_mode="Markdown")
        
        # Отправляем инфу тебе
        info = user_info.get(user_id, {})
        admin_msg = f"✅ Придёт: *{info.get('fio', '—')}* (@{message.from_user.username or '—'})\n"
        admin_msg += f"🕐 Время: *{info.get('arrival_time', '13:00')}*\n"
        if info.get("plus_one") == "yes":
            admin_msg += f"👫 С ним/ней: *{info.get('plus_one_name')}*\n"
            admin_msg += f"🍹 Твой напиток: *{info.get('my_drink')}*\n"
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
    await delete_prev_messages(callback.from_user.id)
    await send_bot_message(callback.from_user.id, "А что пьёшь ты? 👇", reply_markup=my_drinks_kb())
    await callback.answer()

@dp.callback_query(F.data == "time_no")
async def on_time_no(callback: CallbackQuery):
    user_steps[callback.from_user.id] = "wait_custom_time"
    await delete_prev_messages(callback.from_user.id)
    await send_bot_message(callback.from_user.id, "Понял! Во сколько ты будешь? (напиши время текстом, например: 14:30)")
    await callback.answer()

@dp.callback_query(F.data == "mydrink_custom")
async def on_my_drink_custom(callback: CallbackQuery):
    user_steps[callback.from_user.id] = "wait_custom_my_drink"
    await delete_prev_messages(callback.from_user.id)
    await send_bot_message(callback.from_user.id, "Напиши, пожалуйста, что ты будешь пить (или напиши «Не пью»):")
    await callback.answer()

@dp.callback_query(F.data == "frienddrink_custom")
async def on_friend_drink_custom(callback: CallbackQuery):
    user_steps[callback.from_user.id] = "wait_custom_friend_drink"
    await delete_prev_messages(callback.from_user.id)
    await send_bot_message(callback.from_user.id, "Напиши, пожалуйста, что будет пить твой спутник:")
    await callback.answer()

@dp.callback_query(F.data.startswith("mydrink:"))
async def on_my_drink(callback: CallbackQuery):
    user_id = callback.from_user.id
    my_drink = callback.data.split(":", 1)[1]
    user_info[user_id]["my_drink"] = my_drink
    await delete_prev_messages(user_id)
    
    if user_info[user_id].get("plus_one") == "yes":
        user_steps[user_id] = "wait_plus_name"
        await send_bot_message(user_id, "Напиши имя твоего спутника (текстом):")
    else:
        user_steps[user_id] = "preferences"
        await send_bot_message(user_id, "Отлично! У тебя есть какие-то предпочтения?\nНапример: Баня, караоке, горячий шашлык 👇")
    await callback.answer()

@dp.callback_query(F.data.startswith("frienddrink:"))
async def on_friend_drink(callback: CallbackQuery):
    user_id = callback.from_user.id
    friend_drink = callback.data.split(":", 1)[1]
    user_info[user_id]["friend_drink"] = friend_drink
    user_steps[user_id] = "preferences"
    await delete_prev_messages(user_id)
    await send_bot_message(user_id, "Отлично! У тебя есть какие-то предпочтения?\nНапример: Баня, караоке, горячий шашлык 👇")
    await callback.answer()

@dp.callback_query(F.data == "restart")
async def on_restart(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_steps[user_id] = None
    user_info[user_id] = {}
    
    await delete_prev_messages(user_id) 
    
    photo = FSInputFile(PHOTO_PATH)
    msg_photo = await callback.message.answer_photo(photo=photo)
    if user_id not in bot_messages:
        bot_messages[user_id] = []
    bot_messages[user_id].append(msg_photo)
    
    await send_bot_message(user_id, TEXT_LYRICS, reply_markup=start_kb(), parse_mode="Markdown")
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
            if a.get('plus_one') == "yes":
                lines.append(f"✅ {fio} (в {time}) + {a.get('plus_one_name')} — {a.get('my_drink')} / {a.get('friend_drink')} (Пожелания: {pref})")
            else:
                lines.append(f"✅ {fio} (в {time}) — {a.get('my_drink')} (Пожелания: {pref})")
    await message.answer("\n".join(lines), parse_mode="Markdown")

async def main():
    asyncio.create_task(reminder_loop())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())