from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telebot import types

markup_your_score = types.InlineKeyboardMarkup(row_width=2)
item1 = types.InlineKeyboardButton("Твой результат🍾", callback_data='your_score')
markup_your_score.add(item1)

markup_lead = types.InlineKeyboardMarkup(row_width=2)
item1 = types.InlineKeyboardButton("Таблица лидеров🤸", callback_data='lead')
markup_lead.add(item1)

keyboard_duels = InlineKeyboardMarkup(row_width=3)
keyboard_duels.add(
            InlineKeyboardButton("🗿", callback_data="stone"),
            InlineKeyboardButton("✂️", callback_data="scissors"),
            InlineKeyboardButton("💷", callback_data="paper"),)

keyboard_a = InlineKeyboardMarkup(row_width=3)
keyboard_a.add(
            InlineKeyboardButton("yes", callback_data="accept1"),
            InlineKeyboardButton("no", callback_data="decline1"))

kakaska = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
kakaska.add(KeyboardButton('1'), ('2'), ('3'), ('4'))

duels_markup = types.InlineKeyboardMarkup(row_width=3)
rock_d = types.InlineKeyboardButton("🗿", callback_data='🗿')
paper_d = types.InlineKeyboardButton("💵", callback_data='💵')
sicors_d = types.InlineKeyboardButton("✂️", callback_data='✂️')
exit_d = sicors = types.InlineKeyboardButton("выход❌", callback_data='❌')
duels_markup.add(rock_d, sicors_d, paper_d)
duels_markup.add(exit_d)

Who_GPT_markup = types.InlineKeyboardMarkup(row_width=1)
DPXR = types.InlineKeyboardButton("ДПХР👔", callback_data='DPXR')
clown = types.InlineKeyboardButton("Нехороший!🤡", callback_data='clown')
Who_GPT_markup.add(clown, DPXR)

markup_game = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
rock = KeyboardButton("🗿")
sis = KeyboardButton("✂️")
paper = KeyboardButton("💵")
score = KeyboardButton("счёт📄")
exit = KeyboardButton("выход❌")
markup_game.add(paper, sis, rock)
markup_game.add(exit, score)

markup_event = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
markup_event.add(KeyboardButton('да'), ('ДА!'), ('нет'))

markup_GPT = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
markup_GPT.add(KeyboardButton('продолжи🥺'), ('ВЫХОД❌'), ('привет!'))

markup_my = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
rps = KeyboardButton("/game_rps")
cha = KeyboardButton("/my_chanel")
help = KeyboardButton("/help")
infobot = KeyboardButton("/info_about_bot")
ys = KeyboardButton("/your_score")
markup_my.add(help, cha, rps)
markup_my.add(infobot, ys)

# x = "🤕"
