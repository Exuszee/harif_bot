#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This is a testing environment for Customer suport of Harif Sport betting Platform.

import logging
import os
import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from datetime import datetime, timedelta, timezone
import time
from flask import Flask, request
import tabulate
import emoji
import pandas as pd
import pyshorteners
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
import telegram
from telebot import types
import lang_dict
from eng_class import English_bot
from amh_class import Amharic_bot
import formatter
import db_schema
from telegram import *
# import eng_class
# import amh_class
# import config
# import dbworker


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Telegram token
TOKEN = "Your_Telegram_Bot_TOKEN"
# Init bot
bot = telebot.TeleBot(TOKEN)  # , threaded=False)


# Init Flask Server (For cloud deployment)
server = Flask(__name__)

# eng_class = English_bot(bot)
# amh_class = Amharic_bot(bot)


@bot.message_handler(commands=['start'])
def cmd_start(message):
    eng_class = English_bot(bot)
    amh_class = Amharic_bot(bot)

    print(message)
    chat_id = message.chat.id
    user_id = message.from_user.id
    print(chat_id, user_id)
    unix_ts = int(message.date)  # unix timestamp
    time_stamp = formatter.unix_to_date(unix_ts)
    print(time_stamp)
    print("Bot Started by {}... ".format(
        message.from_user.first_name))
    session_expiry = formatter.set_session_expiry(time_stamp)
    print(session_expiry)

    # Welcome Fetching Database
    bot.send_photo(
        message.chat.id, 'https://scontent.fadd1-1.fna.fbcdn.net/v/t1.6435-9/cp0/e15/q65/p320x320/86465367_128063475399041_7206321894184714240_n.jpg?_nc_cat=103&ccb=1-5&_nc_sid=110474&_nc_ohc=iM1U0YIYy3MAX9Jt1WK&_nc_ht=scontent.fadd1-1.fna&oh=41d1ee59bbdb359af294055bbb175873&oe=617C10C4')
    bot.send_message(
        message.chat.id,
        formatter.format_me("Welcome to Harif Sport Betting...\nእንኳን ወደ አሪፍ ቤቲንግ በደህና መጡ! ..."), parse_mode='HTML')
    bot.send_message(message.chat.id, formatter.format_me(
        "Fetching Your Personal Dashboard, Please wait for a few seconds ... \n"), parse_mode='HTML')
    # Init Language classes
    # init DB
    user_db = db_schema.User_db_update()
    db_check = db_schema.User_db_checker()
    # eng_class = English_bot(bot, message)
    # amh_class = Amharic_bot(bot, message)

    # GET database stat from chat_id
    result, chat_lang, is_loggedin, is_registered, phone, password, last_login, login_expiry = db_check.get_user(
        chat_id)
    print(result, chat_lang, is_loggedin, is_registered,
          phone, password, last_login, login_expiry)
    if result == "Pass":
        if chat_lang == "english":
            if str(is_registered) == "1":
                if str(is_loggedin) == "1":
                    if time_stamp < login_expiry:
                        eng_class.dashboard(message)
                    elif time_stamp >= login_expiry:
                        eng_class.welcome_back_login(message)
                elif str(is_loggedin) == "0":
                    eng_class.welcome_back_login(message)
            elif str(is_registered) == "0":
                eng_class.welcome_reg(message)
        elif chat_lang == "amharic":
            if str(is_registered) == "1":
                if str(is_loggedin) == "1":
                    if time_stamp < login_expiry:
                        amh_class.dashboard(message)
                    elif time_stamp >= login_expiry:
                        amh_class.welcome_back_login(message)
                elif str(is_loggedin) == "0":
                    amh_class.welcome_login(message)
            elif str(is_registered) == "0":
                amh_class.welcome_reg(message)
        elif chat_lang == "None":
            user_db.update_db(str(message.chat.id), 'None', "0", 'None', str(
                message.from_user.id), '0', '0', "None", time_stamp, session_expiry)
            bot.send_message(
                message.chat.id,
                formatter.format_me("Please Choose Your Language\nእባክዎን ቋንቋ ይምረጡ\n"), parse_mode='HTML',
                reply_markup=in_lang_keyboard())

    elif result == "Fail":
        user_db.update_db(str(message.chat.id), 'None', "0", 'None', str(
            message.from_user.id), '0', '0', "None", time_stamp, session_expiry)
        bot.send_message(
            message.chat.id,
            formatter.format_me("Please Choose Your Language\nእባክዎን ቋንቋ ይምረጡ\n"), parse_mode='HTML',
            reply_markup=in_lang_keyboard())
    # return reply


# Reset and language selection bot handler
@bot.message_handler(commands=['reset', 'language'])
def reset(message):
    print("reset Clicked")
    chat_id = message.chat.id
    bot.send_message(
        message.chat.id,
        formatter.format_me("Harif Bot Restarting ... "), parse_mode='HTML')
    bot.send_photo(
        message.chat.id, 'https://scontent.fadd1-1.fna.fbcdn.net/v/t1.6435-9/cp0/e15/q65/p320x320/86465367_128063475399041_7206321894184714240_n.jpg?_nc_cat=103&ccb=1-5&_nc_sid=110474&_nc_ohc=iM1U0YIYy3MAX9Jt1WK&_nc_ht=scontent.fadd1-1.fna&oh=41d1ee59bbdb359af294055bbb175873&oe=617C10C4')
    bot.send_message(
        message.chat.id,
        formatter.format_me("Welcome to Harif Sport Betting...\n > Please Choose Your Language\nእንኳን ወደ አሪፍ ቤቲንግ በደህና መጡ! ... \n > እባክዎን ቋንቋ ይምረጡ\n\n"), parse_mode='HTML',
        reply_markup=in_lang_keyboard())

    print("Start Pressed by {}... ".format(
        message.from_user.first_name))


@bot.message_handler(content_types=['contact'])
def contact_handler(message):
    eng_class = English_bot(bot)
    amh_class = Amharic_bot(bot)

    print("Contact_handler working!")
    print(message.contact.phone_number)
    phone = message.contact.phone_number
    user_id = message.from_user.id
    chat_id = message.chat.id
    print(user_id, chat_id)
    db_check = db_schema.User_db_checker()
    chat_lang = db_check.check_lang(chat_id)
    print(chat_lang)
    if chat_lang == 'english':
        eng_class.remove_keyboard_no_message(message)
        eng_class.register_en_pass(message, user_id, phone)
    elif chat_lang == 'amharic':
        amh_class.remove_keyboard_no_message(message)
        amh_class.register_am_pass(message, user_id, phone)


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    eng_class = English_bot(bot)
    amh_class = Amharic_bot(bot)

    chat_id = call.message.chat.id
    user_id = call.message.from_user.id

    # time stamp
    unix_ts = int(call.message.date)  # unix timestamp
    time_stamp = formatter.unix_to_date(unix_ts)
    session_expiry = formatter.set_session_expiry(time_stamp)
    db_check = db_schema.User_db_checker()
    user_db = db_schema.User_db_update()
    result, chat_lang, is_loggedin, is_registered, phone, password, last_login, login_expiry = db_check.get_user(
        call.message.chat.id)

    # Lang Selection
    if call.data == 'english':
        # user_db = db_schema.User_db_update()
        # result, chat_lang, is_loggedin, is_registered, phone, password, last_login, login_expiry = user_db.get_user(
        #     call.message.chat.id)

        user_db.update_db(str(chat_id), 'english', "0", 'None', str(
            user_id), '0', '0', "None", last_login, login_expiry)
        eng_class.welcome_reg(call.message)

    if call.data == 'amharic':
        # user_db = db_schema.User_db_update()
        # result, chat_lang, is_loggedin, is_registered, phone, password, last_login, login_expiry = user_db.get_user(
        #     call.message.chat.id)

        user_db.update_db(str(chat_id), 'anharic', "0", 'None', str(
            user_id), '0', '0', "None", last_login, login_expiry)
        amh_class.welcome_reg(call.message)

    # Lang Class Specifics
    # ENglish Class
    if call.data == 'e_register':
        eng_class.register_en_phone(call.message)

    if call.data == 'e_login':
        eng_class.login_en(call.message)

    if call.data == 'e_support':
        eng_class.support_en(call.message)

    if call.data == 'e_main_menu':
        # user_db = db_schema.User_db_update()
        # result, chat_lang, is_loggedin, is_registered, phone, password, last_login, login_expiry = user_db.get_user(
        #     call.message.chat.id)

        if str(is_registered) == "1":
            if str(is_loggedin) == "1":
                if time_stamp < login_expiry:
                    eng_class.dashboard(call.message)
                elif time_stamp >= login_expiry:
                    eng_class.welcome_back_login(
                        call.message)  # session expired login
            elif str(is_loggedin) == "0":
                eng_class.welcome_back_login(call.message)
        elif str(is_registered) == "0":
            eng_class.welcome_reg(call.message)
    if call.data == 'e_dashboard':
        # user_db = db_schema.User_db_update()
        # result, chat_lang, is_loggedin, is_registered, phone, password, last_login, login_expiry = user_db.get_user(
        #     call.message.chat.id)

        if str(is_registered) == "1":
            if str(is_loggedin) == "1":
                if time_stamp < login_expiry:
                    eng_class.dashboard(call.message)
                elif time_stamp >= login_expiry:
                    eng_class.welcome_back_login(
                        call.message)  # session expired login
            elif str(is_loggedin) == "0":
                eng_class.welcome_back_login(call.message)
        elif str(is_registered) == "0":
            eng_class.welcome_reg(call.message)

    if call.data == 'en_deposit_h':
        eng_class.en_deposit_h(call.message)

    if call.data == 'en_withdraw_h':
        eng_class.en_withdraw_h(call.message)

    if call.data == 'e_deposit':
        eng_class.e_deposit(call.message)

    if call.data == 'e_withdraw':
        eng_class.e_withdraw(call.message)

    if call.data == 'e_book_bet':
        eng_class.e_book_bet(call.message)


# B6maO5  # 4.>2d
# Language selection keyboard


def in_lang_keyboard():
    markup = types.InlineKeyboardMarkup()
    amh_btn = types.InlineKeyboardButton(
        str("አማርኛ"), callback_data=str("amharic"))  # KeyboardButton('አማርኛ')
    eng_btn = types.InlineKeyboardButton(
        str("English"), callback_data=str("english"))  # KeyboardButton('English')
    markup.add(amh_btn, eng_btn)
    return markup


# quit to main menu
def quit_to_main_menu_keyboard():
    markup = types.InlineKeyboardMarkup()

    btn_quit = types.InlineKeyboardButton(
        'My Dashboard', callback_data='e_dashboard')
    support_en = types.InlineKeyboardButton(
        str("Support"), callback_data=str("e_support"))  # KeyboardButton('እርዳታ')
    markup.add(support_en)
    markup.add(btn_quit)
    return markup


# For Cloud Deployment only
# Run Prometheus using server webhook
@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates(
        [telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://harifbot.herokuapp.com/' + TOKEN)
    return "!", 200


if __name__ == "__main__":
    bot.polling(none_stop=True)
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))


# # bot.polling(none_stop=True)
# # Testing only
# while True:
#     try:
#         print("Prometheus is running ... ")
#         bot.polling(none_stop=True)
#         # bot.infinity_polling(True)

#     except Exception as err:
#         logging.error(err)
#         time.sleep(5)
#         print(str(err) + "---Connection error!")
