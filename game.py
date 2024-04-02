from telebot import TeleBot
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

token = "токен_сюда"
bot = TeleBot(token=token)

user_data = {
    "юзернейм1_телеграма": 11111111,  # Юзернейм телеграма: id пользователя
    "юзернейм2_телеграма": 22222222,  # Юзернейм телеграма: id пользователя
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
def challenge_to_duel(message: Message):
    players = list(user_data.keys())

    bot.send_message(
        message.chat.id,
        f"Напишите имя оппонента, которому хотите бросить вызов: {players}"
    )
    bot.register_next_step_handler(message, choose_rival)


def choose_rival(message: Message):
    rival = message.text
    if rival in user_data:
        game_data["player_1"]["username"] = message.from_user.username

        bot.send_message(
            message.chat.id,
            f"Мы отправили ваш вызов сопернику {rival}. Ждём его ответ..."
        )

        keyboard = InlineKeyboardMarkup(row_width=2)
        keyboard.add(
            InlineKeyboardButton("Да", callback_data="accept"),
            InlineKeyboardButton("Нет", callback_data="decline"),
        )

        bot.send_message(
            user_data[rival],
            f"Вам бросил вызов {message.from_user.username}. Принять?",
            reply_markup=keyboard
        )
    else:
        bot.send_message(
            message.chat.id,
            "Такого пользователя не существует:("
        )


@bot.callback_query_handler(func=lambda callback: callback.data in ["accept", "decline"])
def accept_challenge(callback: CallbackQuery):
    bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.id,
        text=callback.message.text,
        reply_markup=None,
    )

    if callback.data == "decline":
        bot.send_message(
            user_data[game_data["player_1"]["username"]],
            "Оппонент не принял ваш вызов:("
        )
        bot.send_message(
            callback.message.chat.id,
            "Трус!"
        )
        game_data["player_1"]["username"] = ""

    else:
        game_data["player_2"]["username"] = callback.from_user.username

        keyboard = InlineKeyboardMarkup(row_width=3)
        keyboard.add(
            InlineKeyboardButton("Камень", callback_data="stone"),
            InlineKeyboardButton("Ножницы", callback_data="scissors"),
            InlineKeyboardButton("Бумага", callback_data="paper"),
        )

        bot.send_message(
            user_data[game_data["player_1"]["username"]],
            "Противник принял вызов! Начинаем!",
            reply_markup=keyboard,
        )
        bot.send_message(
            callback.message.chat.id,
            "Начинаем!",
            reply_markup=keyboard,
        )


@bot.callback_query_handler(func=lambda callback: callback.data in ["stone", "scissors", "paper"])
def choice_weapon(callback: CallbackQuery):
    bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.id,
        text=callback.message.text,
        reply_markup=None,
    )
    for _, player_data in game_data.items():
        if player_data["username"] == callback.from_user.username:
            player_data["choice"] = callback.data

    if game_data["player_1"]["choice"] and game_data["player_2"]["choice"]:
        who_win()


def who_win():
    choice_player_1 = game_data["player_1"]["choice"]
    choice_player_2 = game_data["player_2"]["choice"]

    if choice_player_1 == choice_player_2:
        game_data["player_1"]["choice"] = ""
        game_data["player_2"]["choice"] = ""

        keyboard = InlineKeyboardMarkup(row_width=3)
        keyboard.add(
            InlineKeyboardButton("Камень", callback_data="stone"),
            InlineKeyboardButton("Ножницы", callback_data="scissors"),
            InlineKeyboardButton("Бумага", callback_data="paper"),
        )

        bot.send_message(
            user_data[game_data["player_1"]["username"]],
            "Пока ничья.. Продолжаем!",
            reply_markup=keyboard,
        )
        bot.send_message(
            user_data[game_data["player_2"]["username"]],
            "Пока ничья.. Продолжаем!",
            reply_markup=keyboard,
        )

    elif ((choice_player_1 == "stone" and choice_player_2 == "scissors")
          or (choice_player_1 == "scissors" and choice_player_2 == "paper")
          or (choice_player_1 == "paper" and choice_player_2 == "stone")):
        bot.send_message(
            user_data[game_data["player_1"]["username"]],
            "Поздравляем! Вы победили!",
        )
        bot.send_message(
            user_data[game_data["player_2"]["username"]],
            "К сожалению, вы проиграли:(",
        )

    else:
        bot.send_message(
            user_data[game_data["player_1"]["username"]],
            "К сожалению, вы проиграли:(",
        )
        bot.send_message(
            user_data[game_data["player_2"]["username"]],
            "Поздравляем! Вы победили!",
        )


bot.polling()
