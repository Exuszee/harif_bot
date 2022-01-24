#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This is a testing environment for Customer suport of Harif Sport betting Platform.

import logging
import os
import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
import pyshorteners
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
import telegram
from telebot import types


class HS_ENG_keyboard:
    def __init__(self):
        # init markup
        self.inline_markup = types.InlineKeyboardMarkup()
        # Help Buttons
        self.btn_about = types.InlineKeyboardButton("", callback_data="")
        self.btn_call_support = types.InlineKeyboardButton(
            "", callback_data="")
        self.btn_deposit = types.InlineKeyboardButton("", callback_data="")
        self.btn_join = types.InlineKeyboardButton("", callback_data="")
        self.btn_withdrawal = types.InlineKeyboardButton("", callback_data="")
        self.book_en = types.InlineKeyboardButton("", callback_data="")
        # Menu
        self.btn_quit = types.InlineKeyboardButton("", callback_data="")
        self.deposit_en = types.InlineKeyboardButton("", callback_data="")
        self.login_en = types.InlineKeyboardButton("", callback_data="")
        self.register_en = types.InlineKeyboardButton("", callback_data="")
        self.support_en = types.InlineKeyboardButton("", callback_data="")
        self.withdraw_en = types.InlineKeyboardButton("", callback_data="")

        pass

    # English
    def in_eng_menu_keyboard_en(self):
        pass

    def login_reg_sup_keyboard_en(self):
        pass

    def login_keyboard_en(self):
        pass

    def register_keyboard_en(self):
        pass

    def share_phone_keyboard_en(self):
        pass

    def support_keyboard_en(self):
        pass

    def quit_to_main_menu_keyboard_en(self):
        pass

    def payment_gateway_keyboard_en(self):
        pass

    def main_menu_keyboard_en(self):
        pass

    # Amharic

    def in_eng_menu_keyboard_am(self):
        pass

    def login_reg_sup_keyboard_am(self):
        pass

    def login_keyboard_am(self):
        pass

    def register_keyboard_am(self):
        pass

    def share_phone_keyboard_am(self):
        pass

    def support_keyboard_am(self):
        pass

    def quit_to_main_menu_keyboard_am(self):
        pass

    def payment_gateway_keyboard_am(self):
        pass

    def main_menu_keyboard_am(self):
        pass
