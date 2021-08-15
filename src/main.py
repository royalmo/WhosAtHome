#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#################################################################################
# MIT License

# Copyright (c) 2021 Eric Roy

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#################################################################################

"""
This is the main module, that needs to be executed when running the bot.
"""

# Telegram bot dependencies
import telepot
from telepot.loop import MessageLoop

# REPO_PATH contains the output of the classical pwd command
from pathlib import Path
REPO_PATH = str(Path(__file__).parent.parent.absolute()) + "/"

# Getting information from the .ini file
from configparser import ConfigParser
cnf = ConfigParser()
cnf.read(REPO_PATH + "telegram_token.ini")

# Bot handler importing
from bothandler import BotHandler

# Getting bot token and starting the bot
TOKEN = cnf['Telegram-token']['Token']
bot = telepot.Bot(TOKEN)

# Starting BotHandler and Bot
bh = BotHandler(bot, REPO_PATH)
MessageLoop(bot, bh.new_message).run_as_thread()


# Infinite loop
if __name__ == "__main__":

    while True:
        continue
