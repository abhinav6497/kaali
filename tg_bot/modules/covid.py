
import html
import wikipedia
import re
from datetime import datetime
from typing import Optional, List
from covid import Covid

import requests
from telegram import Message, Chat, Update, Bot, MessageEntity
from telegram import ParseMode, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CommandHandler, run_async, Filters
from telegram.utils.helpers import escape_markdown, mention_html
from telegram.error import BadRequest

from tg_bot import dispatcher, OWNER_ID, SUDO_USERS, SUPPORT_USERS, WHITELIST_USERS

from tg_bot.__main__ import STATS, USER_INFO
from tg_bot.modules.disable import DisableAbleCommandHandler
from tg_bot.modules.helper_funcs.extraction import extract_user



from requests import get

cvid = Covid(source="worldometers")




@run_async
def covid(bot: Bot, update: Update):
    message = update.effective_message
    chat = update.effective_chat
    country = str(message.text[len(f'/covid '):])
    if country == '':
        country = "world"
    if country.lower() in ["south korea", "korea"]:
        country = "s. korea"
    try:
        c_case = cvid.get_status_by_country_name(country)
    except Exception:
        message.reply_text(tld(chat.id, "misc_covid_error"))
        return
    active = format_integer(c_case["active"])
    confirmed = format_integer(c_case["confirmed"])
    country = c_case["country"]
    critical = format_integer(c_case["critical"])
    deaths = format_integer(c_case["deaths"])
    new_cases = format_integer(c_case["new_cases"])
    new_deaths = format_integer(c_case["new_deaths"])
    recovered = format_integer(c_case["recovered"])
    total_tests = c_case["total_tests"]
    if total_tests == 0:
        total_tests = "N/A"
    else:
        total_tests = format_integer(c_case["total_tests"])
    reply = tld(chat.id,
                "misc_covid").format(country, confirmed, new_cases, active,
                                     critical, deaths, new_deaths, recovered,
                                     total_tests)
    message.reply_markdown(reply)




COVID_HANDLER = DisableAbleCommandHandler("covid", covid, admin_ok=True)

