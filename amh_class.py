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
import formatter
import db_schema
import re


class Amharic_bot:
    def __init__(self, bot):
        self.bot = bot
        self.eng_lang, self.am_lang = lang_dict.lang_dict_opt()

        print("called english bot")

    # Welcome English

    def welcome(self, message):
        print("English Selected!")
        reply = self.bot.send_message(message.chat.id,
                                      formatter.format_me(str(self.eng_lang['welcome']).format(
                                          message.from_user.first_name)), parse_mode='HTML',
                                      reply_markup=login_reg_sup_keyboard_en())
        # Check DB return
        return reply

    def welcome_reg(self, message):
        print("English registration Selected!")
        reply = self.bot.send_message(message.chat.id,
                                      formatter.format_me(str(self.eng_lang['welcome']).format(
                                          message.from_user.first_name)), parse_mode='HTML',
                                      reply_markup=register_keyboard_en())
        # Check DB return
        return reply

    def welcome_login(self, message):
        print("English Selected!")
        reply = self.bot.send_message(message.chat.id,
                                      formatter.format_me(str(self.eng_lang['login']['welcome']).format(
                                          message.from_user.first_name)), parse_mode='HTML',
                                      reply_markup=login_keyboard_en())
        # Check DB return
        return reply

    def welcome_back_login(self, message):
        print("English Selected!")
        reply = self.bot.send_message(message.chat.id,
                                      formatter.format_me(str(self.eng_lang['login']['welcome_back']).format(
                                          message.from_user.first_name)), parse_mode='HTML',
                                      reply_markup=login_keyboard_en())
        # Check DB return
        return reply

    def dashboard(self, message):
        reply = self.bot.send_message(message.chat.id, formatter.format_me("################\n# My Dashboard #\n################\n".format(
            message.from_user.first_name)), parse_mode='HTML', reply_markup=in_eng_menu_keyboard_en())
        print("Dashboard Selected!")
        return reply

    def e_all_main_menu(self, message):
        reply = self.bot.send_message(message.chat.id, formatter.format_me("\n################\n# My Dashboard #\n################\n".format(
            message.from_user.first_name)), parse_mode='HTML', reply_markup=main_menu_keyboard())
        print("Main Menu Selected!")
        return reply
    ############# LOGIN/ REGISTER ###############
    # Login English

    def login_en(self, message):
        # Enter password or redirect to account
        print("Login selected!")
        msg = self.bot.send_message(message.chat.id, formatter.format_me("Dear {} PLease Type your password and press send to Login.".format(
            message.from_user.first_name)), parse_mode='HTML',
            reply_markup=quit_to_main_menu_keyboard())
        self.bot.register_next_step_handler(msg, self.verify_login)
        return msg

    def verify_login(self, message):
        self.bot.delete_message(message.chat.id, message.id)
        self.bot.send_message(message.chat.id, formatter.format_me(
            "Processing request, Please wait ..."), parse_mode='HTML')
        db = db_schema.User_db_update()
        unix_ts = int(message.date)  # unix timestamp
        time_stamp = formatter.unix_to_date(unix_ts)
        session_expiry = formatter.set_session_expiry(time_stamp)
        db_check = db_schema.User_db_checker()
        result, chat_lang, is_loggedin, is_registered, phone, password, last_login, login_expiry = db_check.get_user(
            message.chat.id)
        if message.text == str(password):
            msg = self.bot.send_message(
                message.chat.id, formatter.format_me("Login Successful!"), parse_mode="HTML")
            db.update_db(str(message.chat.id), chat_lang, phone, password,
                         str(message.from_user.id), "1", "1", "None", time_stamp, session_expiry)
            self.dashboard(msg)

        elif message.text != str(password):
            msg = self.bot.send_message(
                message.chat.id, formatter.format_me("Login Failed! Your password is incorrect"), parse_mode='HTML')
            self.login_en(msg)

    def register_en_phone(self, message):
        print("Register selected!")
        reply = self.bot.send_message(message.chat.id, formatter.format_me("Dear {} PLease share your number to register ... ".format(
            message.from_user.first_name)), parse_mode='HTML',
            reply_markup=share_phone_keyboard_en())
        # remove keyboard
        return reply

    def register_en_pass(self, message, user_id, phone):
        db = db_schema.User_db_update()
        unix_ts = int(message.date)  # unix timestamp
        time_stamp = formatter.unix_to_date(unix_ts)
        session_expiry = formatter.set_session_expiry(time_stamp)

        print("Get PAssword")
        print(phone)
        # Check for Ethiopia Phone number
        phone_regex = re.compile(r'[11]?[+]?[+251]?0?(9\d\d\d\d\d\d\d\d)')
        phone = phone_regex.findall(phone)[0]
        # Generate a random password, save it on db and send it
        password = formatter.generate_pass_hs()
        reply = self.bot.send_message(message.chat.id, formatter.format_me("Thanks, Got it!\n I have Generated a new password for you.\nYou can go to ") +
                                      "<a href='https://www.harifsport.com'>Harf Sport Website </a> to Login or change your Password\n\n> YOUR NEW PASSWORD =  <b>{}</b>\n\n <b>FOR SECURITY PURPOSES THIS MESSAGE WILL SELF DISTRUCT IN 60 SECONDS!</b>\n<b>PLEASE TAKE NOTE OF YOUR PASSWORD NOW!</b>".format(password), parse_mode='HTML', reply_markup=db_quit_to_main_menu_keyboard())

        data = ['english', phone, password,
                user_id, "1", "1", "None"]
        db.update_db(str(message.chat.id), 'english', phone, password,
                     str(user_id), "1", "1", "None", time_stamp, session_expiry)
        time.sleep(60)
        self.bot.delete_message(message.chat.id, reply.id)
        self.dashboard(message)
        # return reply

    def remove_keyboard_no_message(self, message):
        self.bot.send_message(message.chat.id, formatter.format_me(
            ''), parse_mode='HTML', reply_markup=ReplyKeyboardRemove())

    ############# SUPPORT ###############
    # Support English

    def support_en(self, message):
        print("Support English")
        reply = self.bot.send_message(message.chat.id, formatter.format_me("Welcome {}! We highly value your feedback at Harifsport, Please Follow the Link Below to Access FAQ's or Press the Button Below to Get more info.\n\n*************************\n").format(
            message.from_user.first_name) + "Q: What is Harif Sport and Sport Betting?\nA: <a href='https://t.me/harifsport/928'>About Us</a>\n*************************\nQ: Do you Get Paid instantly for your Winning?\nA: <a href='https://www.harifsport.com'>Getting Paid Instantly</a>\n*************************\nQ: How to Place a Bet on HarifSport Telegram Bot?\nA: <a href='https://www.harifsport.com'>How to Place a Bet</a>\n*************************\nQ: How to Book a bet on HarifSport?\nA: <a href='https://www.harifsport.com'>Book a bet on Harifsport</a>\n*************************\nQ: How do I withdraw my Winning?\nA: <a href='https://www.harifsport.com'>Withdraw my Winnings</a>\n*************************\nQ: How to Deposit Money to my Account?\nA: <a href='https://www.harifsport.com'>Deposit to my Accunt</a>\n*************************\nQ: How to Withdraw Money?\nA: <a href='https://www.harifsport.com'>Withdraw Money</a>\n*************************\nQ: What Payment Methods Do you have to Withdraw and Deposit?\nA:<a href='https://www.harifsport.com'>Available Payment Methods</a>\n*************************\nQ: I haven't Received my Money After Withdrawing from my Account\nA: <a href='https://www.harifsport.com'>Problems Withdrawing from my account</a>\n*************************\nQ: I haven't received my Money on my HarifSport Account?\nA: <a href='https://www.harifsport.com'>Problem recieving money from Harifsport</a> ", parse_mode='HTML',
            reply_markup=support_keyboard_en(), disable_web_page_preview=True)
        return reply

    def en_about_h(self, message):
        print("About Selected")
        reply = self.bot.send_photo(message.chat.id, photo=open(
            '/home/ghost/Documents/Telegram_Prometheus/Customer_Support/resources/about.png', 'rb'), parse_mode='HTML',
            reply_markup=quit_to_main_menu_keyboard())
        print("About Pressed!")
        return reply

    def en_deposit_h(self, message):
        print("How to deposit Pressed ... ")
        reply = self.bot.send_message(message.chat.id,
                                      "<a href='https://youtu.be/FbRl8s1j8H0'>How to Deposit</a>",
                                      parse_mode="HTML", reply_markup=quit_to_main_menu_keyboard())
        return reply

    def en_withdraw_h(self, message):
        print("How to withdraw Pressed ... ")
        reply = self.bot.send_message(message.chat.id,
                                      "<a href='https://youtu.be/vKKPjd3m4qQ'>How to Withdraw</a>",
                                      parse_mode="HTML", reply_markup=quit_to_main_menu_keyboard())
        return reply

    def e_deposit(self, message):
        self.bot.send_message(message.chat.id, formatter.format_me(
            "Choose Your Payment Gateway"), parse_mode='HTML', reply_markup=payment_gateway_keyboard())
        print("e_deposit Selected!")

    def e_withdraw(self, message):
        print("e_withdraw Selected!")

    def e_book_bet(self, message):
        print("e_book_bet Selected!")

    def e_hello_cash(self, message):
        print("e_hello_cash Selected!")

    def e_cbe(self, message):
        print("e_cbe Selected!")

    def e_amole(self, message):
        print("e_amole Selected!")

    # About English


# Main Menu Keyboard markup English
def in_eng_menu_keyboard_en():
    # markup = types.InlineKeyboardMarkup()
    markup = types.InlineKeyboardMarkup()

    book_en = types.InlineKeyboardButton(
        str("Book-Bet"), callback_data=str("e_book_bet"))  # KeyboardButton('ይወራረዱ')
    deposit_en = types.InlineKeyboardButton(
        str("Deposit"), callback_data=str("e_deposit"))  # KeyboardButton('ገንዘብ ያስገቡ')
    withdraw_en = types.InlineKeyboardButton(
        str("Withdraw"), callback_data=str("e_withdraw"))  # KeyboardButton('ገንዘብ ያዉጡ')
    support_en = types.InlineKeyboardButton(
        str("Support"), callback_data=str("e_support"))  # KeyboardButton('እርዳታ')

    markup.row(book_en,
               deposit_en)
    markup.row(withdraw_en, support_en)

    return markup


def login_reg_sup_keyboard_en():
    # markup = types.InlineKeyboardMarkup()
    markup = types.InlineKeyboardMarkup()

    login_en = types.InlineKeyboardButton(
        str("Login"), callback_data=str("e_login"))  # KeyboardButton('ይግቡ')
    register_en = types.InlineKeyboardButton(
        str("Register"), callback_data=str("e_register"))  # KeyboardButton('ይመዝገቡ')
    support_en = types.InlineKeyboardButton(
        str("Support"), callback_data=str("e_support"))  # KeyboardButton('እርዳታ')
    book_bet = types.InlineKeyboardButton(
        str("Book a Bet"), callback_data=str("e_book_bet"))

    markup.row(login_en, register_en)
    markup.row(book_bet, support_en)
    return markup


# Login Keyboard
def login_keyboard_en():
    # markup = types.InlineKeyboardMarkup()
    markup = types.InlineKeyboardMarkup()

    login_en = types.InlineKeyboardButton(
        str("Login"), callback_data=str("e_login"))  # KeyboardButton('ይግቡ')
    support_en = types.InlineKeyboardButton(
        str("Support"), callback_data=str("e_support"))  # KeyboardButton('እርዳታ')
    book_en = types.InlineKeyboardButton(
        str("Book a Bet"), callback_data=str("e_book_bet"))

    markup.row(login_en, book_en)
    markup.row(support_en)
    return markup


# Register Keyboard
def register_keyboard_en():
    # markup = types.InlineKeyboardMarkup()
    markup = types.InlineKeyboardMarkup()

    register_en = types.InlineKeyboardButton(
        str("Register"), callback_data=str("e_register"))  # KeyboardButton('ይመዝገቡ')
    support_en = types.InlineKeyboardButton(
        str("Support"), callback_data=str("e_support"))  # KeyboardButton('እርዳታ')
    book_bet = types.InlineKeyboardButton(
        str("Book a Bet"), callback_data=str("e_book_bet"))

    markup.row(register_en, book_bet)
    markup.row(support_en)
    return markup


# share_phone_keyboard
def share_phone_keyboard_en():
    markup = ReplyKeyboardMarkup(
        row_width=2, resize_keyboard=True, one_time_keyboard=True)
    share_phone = KeyboardButton('Share contact', request_contact=True)
    suppoprt_en = KeyboardButton('Support')

    markup.add(share_phone)
    markup.add(suppoprt_en)
    return markup


# Support Keyboard
def support_keyboard_en():
    markup = types.InlineKeyboardMarkup(row_width=3)
    # About
    btn_about = types.InlineKeyboardButton(
        "What is Harif Betting?", url=s.bitly.short('https://harifsport.com/pages/harifsport/about-us'))
    # How to deposit
    btn_deposit = types.InlineKeyboardButton(
        'How to Deposit', callback_data='en_deposit_h')
    # Hoe to withdraw
    btn_withdrawal = types.InlineKeyboardButton(
        'How to Withdraw', callback_data='en_withdraw_h')
    # Join Community
    btn_join = types.InlineKeyboardButton(
        "Join our Community", url='https://t.me/harifsport/928')
    # Call 9353
    btn_call_support = types.InlineKeyboardButton(
        "Call Support", url=s.bitly.short('https://link-to-tel.herokuapp.com/tel/9353'))
    # Quit to main Menu
    btn_quit = types.InlineKeyboardButton(
        'Quit to Main Menu', callback_data='e_main_menu')
    markup.row(btn_deposit, btn_withdrawal)
    markup.row(btn_join, btn_call_support)
    # markup.add(btn_deposit)
    # markup.add(btn_withdrawal)
    markup.row(btn_about, btn_quit)
    # markup.add(btn_call_support)
    # markup.add(btn_quit)

    # markup.row(btn)
    return markup


# quit to main menu
def quit_to_main_menu_keyboard():
    markup = types.InlineKeyboardMarkup()

    btn_quit = types.InlineKeyboardButton(
        'Main Menu', callback_data='e_main_menu')
    support_en = types.InlineKeyboardButton(
        str("Support"), callback_data=str("e_support"))  # KeyboardButton('እርዳታ')
    markup.add(support_en)
    markup.add(btn_quit)
    return markup


# quit to main menu
def db_quit_to_main_menu_keyboard():
    markup = types.InlineKeyboardMarkup()

    btn_quit = types.InlineKeyboardButton(
        'My Dashboard', callback_data='e_main_menu')
    support_en = types.InlineKeyboardButton(
        str("Support"), callback_data=str("e_support"))  # KeyboardButton('እርዳታ')
    markup.add(support_en)
    markup.add(btn_quit)
    return markup


# Payment gateways
def payment_gateway_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=3)
    # About
    btn_about = types.InlineKeyboardButton(
        "What is Harif Betting?", url=s.bitly.short('https://harifsport.com/pages/harifsport/about-us'))
    # How to deposit
    btn_hellocash = types.InlineKeyboardButton(
        'Hellocash', callback_data='e_hello_cash')
    # Hoe to withdraw
    btn_cbe = types.InlineKeyboardButton(
        'CBE', callback_data='e_cbe')
    # Join Community
    btn_amole = types.InlineKeyboardButton(
        "Amole", callback_data='e_amole')
    # Call 9353
    btn_call_support = types.InlineKeyboardButton(
        "Support", callback_data='e_support')
    # Quit to main Menu
    btn_quit = types.InlineKeyboardButton(
        'Quit to Main Menu', callback_data='e_main_menu')
    markup.row(btn_hellocash, btn_cbe)
    markup.row(btn_amole, btn_call_support)
    # markup.add(btn_deposit)
    # markup.add(btn_withdrawal)
    markup.row(btn_quit)
    # markup.add(btn_call_support)
    # markup.add(btn_quit)

    # markup.row(btn)
    return markup
# Main Menu Keyboard


def main_menu_keyboard():
    # markup = types.InlineKeyboardMarkup()
    markup = types.InlineKeyboardMarkup()

    login_en = types.InlineKeyboardButton(
        str("Login"), callback_data=str("e_login"))  # KeyboardButton('ይግቡ')
    register_en = types.InlineKeyboardButton(
        str("Register"), callback_data=str("e_register"))  # KeyboardButton('ይመዝገቡ')
    support_en = types.InlineKeyboardButton(
        str("Support"), callback_data=str("e_support"))  # KeyboardButton('እርዳታ')
    book_en = types.InlineKeyboardButton(
        str("Book a Bet"), callback_data=str("e_book_bet"))

    markup.row(login_en, register_en)
    markup.row(book_en, support_en)

    return markup


############### MISC FUNCTIONS ####################
# Url shortner
bit_ly_token = "2db5345934e2ccd4e46a15cab306cf595517e37d"
s = pyshorteners.Shortener(api_key=bit_ly_token)
