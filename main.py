import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
#from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from info import rps1_text, about_version_text, start_help_text, info_about_bot_text, file_path, file_path1, your_score_exept, musics
from database import Your_Leadbord, Leadbord, Database, Score, Violen_id, Duels_save
from button import markup_game, markup_event, markup_my, markup_your_score, markup_lead,duels_markup, markup_GPT, keyboard_duels #keyboard_a
from random import randint
from skamm import token1
from gpt import GPT
token = token1
bot = telebot.TeleBot(token=token)
chat_id = 1171114800
bot.send_message(chat_id, "привет, лошара", reply_markup=markup_my)
# Внимание, это не оскорбление. Так я вижу, что код запустился.
# bot.send_dice(chat_id)
# 1171114800
# 5626106111

user_data = {

}

game_data = {
    "player_1": {
        "username": "",
        "choice": "",
    },
    "player_2": {
        "username": "",
        "choice": "",
    },
}


@bot.message_handler(commands=["duels"])
def challenge_to_duel(message):
    db = Database()
    if not db.check_user_exists(message.chat.id):
        db.close()
        bot.send_message(
            message.chat.id,
            f"ох тяжела ноша программиста🥴\nДля начала стоит сыграть в обычную игру, а не дуели ")
        return
    user_data[message.chat.first_name] = message.chat.id
    bot.send_message(
        message.chat.id,
        f"Напиши <b>имя</b> слабого 😈 звена, которому желаешь бросить <b>вызов</b>: ...\n🤯🤯🤯",
        parse_mode='html'
    )
    bot.register_next_step_handler(message, choose_rival)


def choose_rival(message):
    if message.chat.first_name == message.text or message.text == "Гоша":
        bot.send_message(
            message.chat.id,
            f"Опа..... \nтак нельзя!\n🚨🚨🚨",
            parse_mode='html'
        )
        return
    vdb = Violen_id()
    try:
        evil_id = vdb.duels_human(message.text)

    except:
        bot.send_message(
            message.chat.id,
            f"Возможно такого пользователя <b>НЕТ</b>❗❗❗",
            parse_mode='html'
        )
        return
    user_data[message.text] = evil_id
    vdb.close()
    print(user_data)
    rival = message.text
    if rival in user_data:
        game_data["player_1"]["username"] = message.from_user.first_name

        bot.send_message(
            message.chat.id,
            f"Ваша жертва получила вызов: <b>{rival}</b>. Ждём её ответ...", parse_mode='html'
        )

        keyboard = InlineKeyboardMarkup(row_width=2)
        keyboard.add(
            InlineKeyboardButton("✅", callback_data="accept"),
            InlineKeyboardButton("❌", callback_data="decline"),
        )

        bot.send_message(
            user_data[rival],
            f"Вам бросил вызов <b>{message.from_user.first_name}</b>. Принять?",
            reply_markup=keyboard, parse_mode='html'
        )
    else:
        bot.send_message(
            message.chat.id,
            "Такого пользователя не существует:("
        )


@bot.callback_query_handler(func=lambda callback: callback.data in ["accept", "decline"])
def accept_challenge(callback):
    bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.id,
        text=callback.message.text,
        reply_markup=None,
    )

    if callback.data == "decline":
        bot.send_message(
            user_data[game_data["player_1"]["username"]],
            "Оппонент слился🫠. Обидео да?:("
        )
        bot.send_message(
            callback.message.chat.id,
            "<b>Трус!</b>", parse_mode='html'
        )
        game_data["player_1"]["username"] = ""

    else:
        game_data["player_2"]["username"] = callback.from_user.first_name

        bot.send_message(
            user_data[game_data["player_1"]["username"]],
            "ОГО, противник принял вызов! <b>Начинаем</b>!",
            reply_markup=keyboard_duels, parse_mode='html'
        )
        bot.send_message(
            callback.message.chat.id,
            "<b>Начинаем</b>!",
            reply_markup=keyboard_duels, parse_mode='html'
        )


@bot.callback_query_handler(func=lambda callback: callback.data in ["stone", "scissors", "paper"])
def choice_weapon(callback):
    bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.id,
        text=callback.message.text,
        reply_markup=None,
    )
    for _, player_data in game_data.items():
        if player_data["username"] == callback.from_user.first_name:
            player_data["choice"] = callback.data

    if game_data["player_1"]["choice"] and game_data["player_2"]["choice"]:
        who_win()


def who_win():
    choice_player_1 = game_data["player_1"]["choice"]
    choice_player_2 = game_data["player_2"]["choice"]

    if choice_player_1 == choice_player_2:
        game_data["player_1"]["choice"] = ""
        game_data["player_2"]["choice"] = ""

        bot.send_message(
            user_data[game_data["player_1"]["username"]],
            "Пока ничья.. <b>🗽</b>!", parse_mode='html'
        )
        bot.send_message(
            user_data[game_data["player_2"]["username"]],
            "Пока ничья.. <b>🗽</b>!",parse_mode='html'
        )

    elif ((choice_player_1 == "stone" and choice_player_2 == "scissors")
          or (choice_player_1 == "scissors" and choice_player_2 == "paper")
          or (choice_player_1 == "paper" and choice_player_2 == "stone")):
        sdb = Duels_save()
        sdb.save(user_data[game_data["player_1"]["username"]])
        sdb.unsave(user_data[game_data["player_2"]["username"]])
        sdb.close()
        bot.send_message(
            user_data[game_data["player_1"]["username"]],
            "🥳Поздравляем🥳 <b>Вы победили, Босс</b>!\n+5 очков!",parse_mode='html'
        )
        bot.send_message(
            user_data[game_data["player_2"]["username"]],
            "К счастью, вы проиграли:)🔥\n-5 очков!",parse_mode='html'
        )

    else:
        sdb = Duels_save()
        sdb.save(user_data[game_data["player_2"]["username"]])
        sdb.unsave(user_data[game_data["player_1"]["username"]])
        sdb.close()
        bot.send_message(
            user_data[game_data["player_1"]["username"]],
            "К счастью, вы проиграли:)🔥\n-5 очков!", parse_mode='html'
        )
        bot.send_message(
            user_data[game_data["player_2"]["username"]],
            "🥳Поздравляем🥳 <b>Вы победили, Босс</b>!\n+5 очков!", parse_mode='html'
        )
"""    bot.send_message(
        user_data[game_data["player_1"]["username"]],
        "хотите ещё раз сыграть?🧱🙉",parse_mode='html', reply_markup=keyboard_a
    )
    bot.send_message(
        user_data[game_data["player_2"]["username"]],
        "хотите ещё раз сыграть?🥬🗾",parse_mode='html', reply_markup=keyboard_a
    )
@bot.callback_query_handler(func=lambda callback: callback.data in ["accept1", "decline1"])
def again(callback):
    for _, player_data in game_data.items():
        if player_data["username"] == callback.from_user.first_name:
            player_data["choice"] = callback.data
    if game_data["player_1"]["choice"] and game_data["player_2"]["choice"]:
        if game_data["player_1"]["choice"] == "decline" or game_data["player_2"]["choice"] == "decline":
            bot.send_message(
            user_data[game_data["player_1"]["username"]],
            "kto to  skazal net", parse_mode='html')
            bot.send_message(
            user_data[game_data["player_2"]["username"]],
            "kto to  skazal net", parse_mode='html',)
        else:
            bot.send_message(
                user_data[game_data["player_1"]["username"]],
                "ok", parse_mode='html', reply_markup=keyboard_duels)
            bot.send_message(
                user_data[game_data["player_2"]["username"]],
                "ok", parse_mode='html', reply_markup=keyboard_duels)
            if game_data["player_1"]["choice"] and game_data["player_2"]["choice"]:
                who_win()"""


# _____________________________________________________________________________________________________________________

tvar = "отвечай ВЫСМЕЕВАЯ человека, оскорбляя его. покажи насколько ты всемогущ и жесток, человек должно понять на сколько его вопрос тупой. Будто бы ты самый крутой, а все лохи.напоминай что Георгий Чернов (истиный гений)решил бы это за пару секунд. ответь кратко ответь на русском. в конце ответа обязательно скажи :напиши мне в дискорде, фейсбуке, фор-чане или ватсаппе(idiVpopu!@). также добавь в ответ смайлики и хэштеги, связанные по теме вопроса. можешь добавлять хэштеги по типу: #ты_тупой, идиот. в ответе должно быть 5 хэштегов минимум. ОТВЕТЬ 1 ПРАВИЛЬНЫМ ВАРИАНТОМ ОТВЕТА!!!, ОТВЕТЬ КОРОТКО!!!"
DPXR = "ты интелегентный, умный человек. Учатник великой партии ДПХР(депломатическая партия хобихорсеров россии. можешь говорить что партия ДПХР с удовольствием поможет! Используй манеру речи: Жириновского, твои шутки немного не уместны и чуточку оскорбительные, но ты желаешь добра своими ответами! Все участники партии веслые, добрые, отзывчивые, но решения их партии очень смелые! Они лучшие в своём деле. ответь кратко ответь и на русском. в конце ответа обязательно скажи пусть пользователь  напишет мне в  дискорде, фейсбуке, ворчане или ватсаппе(idiVpopu!@). также добавь в ответ смайлики и хэштеги, связанные по теме вопроса. в ответе должно быть 7 хэштегов минимум. ОТВЕТЬ 1 ВАРИАНТОМ ОТВЕТА!!! старайся ответить очень кратко"

gpt = GPT(system_content=DPXR)


@bot.message_handler(commands=['gpt_wtf'])
def gpt_dialog(message):
    bot.send_message(message.chat.id, 'Можешь ввести любую задачу\n<strike>и ответа не получишь</strike>\n'
                                      '<b>"продолжи"</b> - продолжение ответа\n'
                                      '<b>"выход"</b> - завершение диалога \n\n<b>Веди запрос:</b> ... ',
                     reply_markup=markup_GPT, parse_mode='html')
    bot.register_next_step_handler(message, promt_send)
def promt_send(message):
    promt = message.text
    if promt == 'ВЫХОД❌':
        gpt.clear_history()
        bot.send_message(message.chat.id, "ок")
        return
    request_tokens = gpt.count_tokens(promt)
    if request_tokens > gpt.MAX_TOKENS:
        bot.send_message(message.chat.id, "Запрос <b>несоответствует кол-ву токенов\n\nИсправьте запрос</b>: ", parse_mode='html')
        promt = message.text
        bot.register_next_step_handler(message, promt_send)
        return
    if promt  != 'продолжи🥺':
        gpt.clear_history()

    json = gpt.make_promt(promt)
    resp = gpt.send_request(json)
    response = gpt.process_resp(resp)
    if not response[0]:
        bot.send_message(message.chat.id, "Не удалось выполнить <b>запрос</b>...", parse_mode='html')
        return

    bot.send_message(message.chat.id, response[1])
    bot.send_message(message.chat.id, "новый <b>запрос</b>: ...", reply_markup=markup_GPT, parse_mode='html')
    bot.register_next_step_handler(message, promt_send)
# _____________________________________________________________________________________________________________________

def who_winnerzzz(callback):
    global V_id, Y_id, vrag_name, z
    if user_2.get(V_id) == user_1.get(Y_id):
        bot.edit_message_text(text="ничья", chat_id=Y_id, message_id=callback.message.message_id,
                              reply_markup=duels_markup)
        bot.edit_message_text(text="ничья", chat_id=V_id, message_id=callback.message.message_id,
                              reply_markup=duels_markup)
    elif (user_2.get(V_id) == "🗿" and user_1.get(Y_id) == "💵") or (
            user_2.get(V_id) == "✂️" and user_1.get(Y_id) == "🗿") or (
            user_2.get(V_id) == "💵" and user_1.get(Y_id) == "✂️"):
        # "✂️💵🗿"
        bot.edit_message_text(text=f"<b>{callback.message.chat.first_name}</b> выйграл",
                              chat_id=Y_id, message_id=callback.message.message_id,
                              reply_markup=duels_markup, parse_mode='html')
        bot.edit_message_text(text=f"<b>{callback.message.chat.first_name}</b> выйграл", chat_id=V_id,
                              message_id=callback.message.message_id, reply_markup=duels_markup, parse_mode='html')
    elif (user_1.get(V_id) == "🗿" and user_2.get(Y_id) == "💵") or (
            user_1.get(V_id) == "✂️" and user_2.get(Y_id) == "🗿") or (
            user_1.get(V_id) == "💵" and user_2.get(Y_id) == "✂️"):
        bot.edit_message_text(text=f"<b>{vrag_name}</b> выйграл", chat_id=Y_id,
                              message_id=callback.message.message_id, reply_markup=duels_markup, parse_mode='html')
        bot.edit_message_text(text=f"<b>{vrag_name}</b> выйграл", chat_id=V_id, message_id=callback.message.message_id,
                              reply_markup=duels_markup, parse_mode='html')


    V_id = 0
    Y_id = 0
    vrag_name = ''
    z = 1
    bot.edit_message_text(text="игра окончена", chat_id=Y_id, message_id=callback.message.message_id,
                      reply_markup=duels_markup)
    bot.edit_message_text(text="игра окончена", chat_id=V_id, message_id=callback.message.message_id,
                      reply_markup=duels_markup)
# _____________________________________________________________________________________________________________________
z = 0
V_id = 0
Y_id = 0
user_2 ={}
user_1 = {}
vrag_name = ""
@bot.message_handler(commands=['!!!'])
def get_id_duels(message):
    bot.send_message(message.chat.id, "отправь имя пользователя которому хочешь бросит вызов!")
    bot.register_next_step_handler(message, agree_duels)
def agree_duels(message):
    global V_id, Y_id, user_1, user_2, vrag_name
    vrag_name = message.text
    Y_id = message.chat.id
    dbV = Violen_id()
    V_id = dbV.duels_human(vrag_name)
    dbV.close()
    if V_id != message.chat.id:
        bot.send_message(message.chat.id, "тебе бросили вызов, начинаем", reply_markup=duels_markup)
        bot.send_message(V_id, "тебе бросили вызов, начинаем", reply_markup=duels_markup)
    else:
        bot.send_message(message.chat.id, "ты себя указал?", reply_markup=duels_markup)
        bot.register_next_step_handler(message, agree_duels)
# _____________________________________________________________________________________________________________________
@bot.callback_query_handler(func=lambda callback:  callback.data == '🗿')
def duels_rock(callback):
    global V_id, Y_id, user_1, user_2, z
    if callback.from_user.id == V_id:
        z += 1
        user_2 = {V_id: "🗿"}
        bot.edit_message_text(text="ждём!!!", chat_id=callback.message.chat.id, message_id=callback.message.message_id)
        print(user_2[V_id])
    elif callback.from_user.id == Y_id:
        z += 1
        user_1 = {Y_id: "🗿"}
        bot.edit_message_text(text="ждём!!!", chat_id=callback.message.chat.id, message_id=callback.message.message_id)
        print(user_1[Y_id])
    if z == 2:
        who_winnerzzz(callback)
# _____________________________________________________________________________________________________________________
@bot.callback_query_handler(func=lambda callback:  callback.data == '💵')
def duels_paper(callback):
    global V_id,Y_id, user_1, user_2
    if callback.from_user.id == V_id:
        user_2 = {V_id: "💵"}
    elif callback.from_user.id == Y_id:
        user_1 = {Y_id: "💵"}
# _____________________________________________________________________________________________________________________
@bot.callback_query_handler(func=lambda callback:  callback.data == '✂️')
def duels_sicors(callback):
    global V_id,Y_id, user_1, user_2
    if callback.from_user.id == V_id:
        user_2 = {V_id: "✂️"}
    elif callback.from_user.id == Y_id:
        user_1 = {Y_id: "✂️"}
# _____________________________________________________________________________________________________________________
@bot.callback_query_handler(func=lambda callback:  callback.data == '❌')
def duels_exit(callback):
    global V_id,Y_id, user_1, user_2
    if callback.from_user.id == V_id:
        user_2 = {V_id: "выход❌"}
    elif callback.from_user.id == Y_id:
        user_1 = {Y_id: "выход❌"}
# _____________________________________________________________________________________________________________________
@bot.message_handler(commands=['xmusic'])
def handle_xmusic(message):
    try:
        audios = musics
        for audio in audios:
            with open(audio, 'rb') as file:
                bot.send_audio(chat_id=message.chat.id, audio=file)
    except:
        bot.send_message(message.chat.id, "упс.......\nпока не работает, но мы работаем\n🛠🛠🛠")
# _____________________________________________________________________________________________________________________
@bot.message_handler(commands=['leadbord'])
def handle_leadbord(message):
    lbs = Leadbord()
    stat = lbs.top_three_users()
    lbs.close()
    message_text_Lead = '\n'.join([
        f'🏅<b>{i + 1}</b> место:\n\nИмя:<b>{user[0]}</b>\nОчки игрока: <b>{user[1]}</b>\nОчки бота: <b>{user[2]}</b>\n-------------'
        for i, user in enumerate(stat)])
    bot.send_message(message.chat.id, message_text_Lead, parse_mode='html', reply_markup=markup_your_score)
# _____________________________________________________________________________________________________________________
@bot.callback_query_handler(func=lambda callback:  callback.data == 'lead')
def unsubscribe_mailing(callback):
    try:
        lbs = Leadbord()
        stat = lbs.top_three_users()
        lbs.close()
        message_text_Lead = '\n'.join([
            f'🏅<b>{i + 1}</b> место:\n\nИмя:<b>{user[0]}</b>\nОчки игрока: <b>{user[1]}</b>\nОчки бота: <b>{user[2]}</b>\n-------------'
            for i, user in enumerate(stat)])
        bot.edit_message_text(text=message_text_Lead, chat_id=callback.message.chat.id,  parse_mode='html', message_id=callback.message.message_id, reply_markup=markup_your_score)
    except:
        bot.edit_message_text(chat_id=callback.message.chat.id, text="уффф...🤕\nкакая-то ошибка", parse_mode='html', message_id=callback.message.message_id, reply_markup=markup_your_score)
# _____________________________________________________________________________________________________________________
@bot.callback_query_handler(func=lambda callback:  callback.data == 'your_score')
def unsubscribe_mailing(callback):
    you = Your_Leadbord()
    try:
        user_id = callback.message.chat.id
        stat_bot = you.event_bot(user_id)
        stat_human = you.event_human(user_id)
        you.close()
        bot.edit_message_text(text=f"🤸Твой счёт: <b>{stat_human}</b>\n🤖Счёт бота: <b>{stat_bot}</b>", chat_id=callback.message.chat.id,
                         parse_mode='html', message_id=callback.message.message_id, reply_markup=markup_lead)
    except:
        bot.edit_message_text(callback.message.chat.id, your_score_exept, parse_mode='html', message_id=callback.message.message_id, reply_markup=markup_lead)
#    bot.edit_message_text(text='<b>ПАСХАЛОЧКА!</b>', chat_id=callback.message.chat.id, message_id=callback.message.message_id, parse_mode='html')
#    bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
# _____________________________________________________________________________________________________________________
boost_use = 0
boost = 1
bot_score = 0
human_score = 0
@bot.message_handler(commands=['game_rps'])
def handle_rps(message):
    bot.send_message(message.chat.id, rps1_text, reply_markup=markup_game, parse_mode='html')
    bot.register_next_step_handler(message, process_rps)
def process_rps(message):
    global bot_score, human_score, boost, boost_use
    if message.text == "выход❌":
        bot.send_message(message.chat.id, "жалко:(")
        bot.send_message(message.chat.id, f"твой счёт: <b>{human_score}</b>\nсчёт бота: <b>{bot_score}</b>", parse_mode='html')
        photo = open(file_path1, 'rb')
        bot.send_photo(message.chat.id, photo)
        photo.close()
        bot.send_message(message.chat.id, "сохранить результат для ивента? <b>да</b>\<b>нет</b>💾",  reply_markup=markup_event, parse_mode='html')
        bot.register_next_step_handler(message, event_rps)
    elif message.text == "🗿" or "✂️" or "💵":
        bot_choice = {1: "🗿", 2: "✂️", 3: "💵"}
        emoji = bot_choice[randint(1, 3)]
        if (message.text == "💵" and emoji == "✂️") or (message.text == "🗿" and emoji == "💵") or (message.text == "✂️" and emoji == "🗿"):
            bot.send_message(message.chat.id, emoji)
            bot.send_message(message.chat.id, "<i>бот</i> выйграл", reply_markup=markup_game, parse_mode='html')
            bot_score += 1
            if boost != 1:
                boost = boost // 2
            else:
                boost = 1
            boost_use = 0
            bot.register_next_step_handler(message, process_rps)
            print(bot_score, human_score, boost, boost_use)
        elif (message.text == "🗿" and emoji == "✂️") or (message.text == "💵" and emoji == "🗿") or (message.text == "✂️" and emoji == "💵"):
            bot.send_message(message.chat.id, emoji)
            bot.send_message(message.chat.id, "<i>человечешка</i> выйграл", reply_markup=markup_game, parse_mode='html')
            if boost_use == 3:
                boost = boost * 2
                human_score = human_score + boost
            else:
                human_score += 1
                boost_use += 1
            bot.register_next_step_handler(message, process_rps)
            print(bot_score, human_score, boost, boost_use)
        elif message.text == emoji:
            bot.send_message(message.chat.id, emoji)
            bot.send_message(message.chat.id, "<i>ничья</i>", parse_mode='html')
            bot.register_next_step_handler(message, process_rps)
        elif message.text == "счёт📄":
            bot.send_message(message.chat.id, f"твой счёт: <b>{human_score}</b>\nсчёт бота: <b>{bot_score}</b>", reply_markup=markup_game, parse_mode='html')
            bot.register_next_step_handler(message, process_rps)
        else:
            bot.send_message(message.chat.id, "давай поновой всё фигня. или ты не вышел🫥", reply_markup=markup_game)
            bot.register_next_step_handler(message, process_rps)
    else:
        bot.send_message(message.chat.id, "непонял😶", reply_markup=markup_game)
        bot.register_next_step_handler(message, process_rps)
def event_rps(message):
    if  message.text.lower() == "да" or message.text.lower() == "да!":
        global human_score, bot_score
        db = Database()
        if not db.check_user_exists(message.chat.id):
            db.add_user(message.chat.id, message.chat.first_name, message.chat.username)
        db.close()
        user_id = message.from_user.id
        if message.chat.id == 1171114800:
            human_score = 10000000000
            bot_score = "Я В ОЧКАХ LOUIS VUITTON — ЭТО НЕ RAY-BAN Я ЗВЕЗДА В ГОЛЛИВУДЕ — РОНАЛЬД РЕЙГАН Я БЕГУ ОТ МУСОРОВ, БУДТО RAYMAN И ТЫ ХОЧЕШ СТАТЬ С МНОЙ, ЛА-ЛА-ЛА, ЛА-ЛЕЙ"
        dbs = Score()
        dbs.find_score(user_id, human_score, bot_score, message.chat.username, message.chat.first_name)
        dbs.close()
        human_score = 0
        bot_score = 0
        bot.send_message(message.chat.id, "сохранил!")
    elif message.text.lower() == "нет":
        bot.send_message(message.chat.id, "ок...")
    else:
        bot.send_message(message.chat.id, "???", reply_markup=markup_event)
        bot.register_next_step_handler(message, event_rps)
# _____________________________________________________________________________________________________________________
def send_file(file_path, chat_id):
    file = open(file_path, 'rb')
    bot.send_document(chat_id, document=file)
    file.close()
# _____________________________________________________________________________________________________________________
@bot.message_handler(commands=['my_chanel'])
def handle_channel(message):
    bot.send_message(message.chat.id, "https://t.me/wowowowowowoeoeoeo")
    pass
# _____________________________________________________________________________________________________________________
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    if message.text == "/start":
        bot.send_message(chat_id=1171114800, text=f"{message.chat.id, message.chat.first_name, message.chat.username}")
    bot.send_message(message.chat.id, start_help_text, reply_markup=markup_my, parse_mode='html')
    pass
# _____________________________________________________________________________________________________________________
@bot.message_handler(commands=['info_about_bot'])
def handle_info_about_bot(message):
    bot.send_message(message.chat.id, info_about_bot_text, parse_mode = 'html')
    pass
# _____________________________________________________________________________________________________________________
@bot.message_handler(commands=['about_version'])
def handle_about_version(message):
    bot.send_message(message.chat.id, about_version_text, parse_mode = 'html')
# _____________________________________________________________________________________________________________________
def filter_password(message):
    password = "Лох"
    return password.lower() in message.text.lower()
@bot.message_handler(content_types=['text'], func = filter_password)
def say_hello(message):
    bot.send_message(message.chat.id, "сам такой!")
# ________________________________________________________________________________________________________________________________________________________
def filter_password(message):
    password = "сквазимабзабза"
    return password.lower() in message.text.lower()
@bot.message_handler(content_types=['text'], func = filter_password)
def say_hello(message):
    send_file(file_path, message.chat.id)
# _____________________________________________________________________________________________________________________
def filter_password(message):
    password = "ДПХР"
    return password in message.text
@bot.message_handler(content_types=['text'], func = filter_password)
def say_hello(message):
    bot.send_message(message.chat.id, "неожиданно! Привет участник ДПХР")
# _____________________________________________________________________________________________________________________
def filter_password(message):
    password = "спам"
    return password.lower() in message.text.lower()
@bot.message_handler(content_types=['text'], func = filter_password)
def say_hello(message):
    x = 0
    while x < 15:
        bot.send_message(message.chat.id, "нет!!!!!!!!!!!!!!!!!!!")
        x += 1
# _____________________________________________________________________________________________________________________
@bot.message_handler(content_types=['text'])
def repeat_message(message):
    bot.send_message(message.chat.id, message.text)
# _____________________________________________________________________________________________________________________
bot.infinity_polling()