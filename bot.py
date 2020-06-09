#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys
import config
import time
import datetime
import re
import subprocess
import tty
import pty
import logging
import telebot
from telebot import types
from telebot import util
 


# ##### TONTgBot

# API Token
bot = telebot.TeleBot(config.TgBotAPIKey)
# /API Token

# ##### TONTgBot

 
# Log
logger = telebot.logger
telebot.logger.setLevel(logging.ERROR) # Outputs Error messages to console.
# /Log
 
# Start
@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
  if message.from_user.id == config.tg:
    bot.send_message(config.tg, "Hello \U0001F44B\nI'm here to help you with your smart contracts \U0001F9BE\nJust send me *.sol and wait =)")
  else:
    pass
# /Start


@bot.message_handler(content_types=['document'])
def handle_docs(message):
  if message.from_user.id == config.tg:
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    soldoc = "/opt/tontgbotcontract/data/" + file_info.file_path
    with open(soldoc, "wb") as cntrct:
      cntrct.write(downloaded_file)
    abicodecompiler = "cd " + config.compiler + " && " + config.solccompiler + " " + soldoc
    abicodecompiler = str(subprocess.check_output(abicodecompiler, shell = True,encoding='utf-8').rstrip())
    time.sleep(0.1)
    outpufrst = abicodecompiler
    ############ .code + .abi.json
    frst_code = re.findall(r'(?:.*)(.*)(\s\w+\.code)', outpufrst)
    frst_code = ("".join(frst_code[0]).strip())
    scnd_abijson = re.findall(r'(?:.*)(.*)(\s\w+\.abi.json)', outpufrst)
    scnd_abijson = ("".join(scnd_abijson[0]).strip())
    ############ .code + .abi.json
    
    ############ .tvc
    tvcccmd = "compile " + config.compiler + frst_code + " --lib /opt/ton-solidity-compiler/lib/stdlib_sol.tvm"
    tvccompile = "cd " + config.tvc + " && " + config.tvmlinker + " " + tvcccmd
    tvccompile = str(subprocess.check_output(tvccompile, shell = True,encoding='utf-8').rstrip())
    tvcfile = tvccompile
    #tvc
    tvcfile = re.findall(r'Saved contract to file (\w+\.tvc)', tvcfile)
    tvcfile = ("".join(tvcfile[0]).strip())
    time.sleep(0.1)
    ############ .tvc
    
    tonoccliconf = "/opt/tonos-cli/target/release/tonos-cli config --url " + config.tcurl
    tonoccliconfexc = str(subprocess.call(tvccompile, shell = True,encoding='utf-8'))
    time.sleep(0.1)
    walletfile = int(time.time())
    # Wallet
    walletfile = str(walletfile) + ".keys.json"
    genaddrcmd = "cd " + config.keys + " && " + config.tonoscli + " genaddr " + config.tvc + tvcfile + " " + config.compiler + scnd_abijson + " --genkey " + walletfile
    genaddrcmd = str(subprocess.check_output(genaddrcmd, shell = True,encoding='utf-8').rstrip())
    rawaddr = genaddrcmd
    rawaddr = re.findall(r'Raw address: (\w+.*)', rawaddr)
    # raw
    rawaddr = ("".join(rawaddr[0]).strip())
    time.sleep(0.1)

    # Status check
    stcheck = config.tonoscli + " account " + rawaddr
    stcheck = str(subprocess.check_output(stcheck, shell = True,encoding='utf-8').rstrip())
    time.sleep(0.1)
    # gruntabi
    gruntabicmd = config.tonoscli + " call --abi " + config.gruntabi + " '0:3b3a3344aa6338c22bfdcd1765d0c7f84bd264df55229e59a2d4201ef25fb114' grant '{\"addr\":\"" + rawaddr + "\"}'"
    gruntabicmd = str(subprocess.call(gruntabicmd, shell = True,encoding='utf-8'))
    time.sleep(0.1)

    deployy = config.tonoscli + " deploy --abi " + config.compiler + scnd_abijson + " --sign " + config.keys + walletfile + " " + config.tvc + tvcfile + " {}"
    deployy = str(subprocess.check_output(deployy, shell = True,encoding='utf-8').rstrip())
    
    itog = tvccompile + "\n" + genaddrcmd + "\n" + deployy
    bot.send_message(config.tg, text = itog)
  else:
    pass

while True:
  try:
    bot.polling(none_stop=True, timeout=10) #constantly get messages from Telegram
  except:
    bot.stop_polling()
    time.sleep(5)
