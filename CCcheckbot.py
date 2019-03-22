from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram
import os
import logging
import urllib.request
from bs4 import BeautifulSoup
import requests
from requests.exceptions import HTTPError


def start(bot, update):
    bot.sendMessage(
        chat_id=update.message.chat_id,
        text='Type in the common core course code e.g. "CCST9010" to check info',
    )


def echo(bot, update):
    bot.sendMessage(
        chat_id=update.message.chat_id, text=update.message.text + "Testing"
    )


def check_vacancies(code):
    if len(code) != 8:
        return "Error, no such CC Code"
    code = code.upper()  # capitalizes code input for easier comparison
    website = BeautifulSoup(
        urllib.request.urlopen(
            "https://sweb.hku.hk/ccacad/ccc_appl/enrol_stat.html"
        ).read(),
        "lxml",
    )
    listofcells = website.select("body table tr td font")

    # list of cells is a list of text contained in each <font> element in <td> elements
    indices = []
    for i in range(len(listofcells)):
        if code == listofcells[i].getText():
            indices.append(i)
    finalstring = ""
    if indices == []:
        return "Error, no such CC Code"
    for index in indices:
        cccode = "CC Code: " + listofcells[index].getText() + "\n"
        title = "CC Name: " + listofcells[index + 1].getText() + "\n"
        subclass = "SubClass: " + listofcells[index + 2].getText() + "\n"
        quota = "Quota: " + listofcells[index + 3].getText() + "\n"
        pleft = "Places Left: " + listofcells[index + 4].getText() + "\n"
        waiting = "Waiting: " + listofcells[index + 5].getText() + "\n"
        finalstring = (
            finalstring + cccode + title + subclass + quota + pleft + waiting + "\n"
        )

    # get time from end of page
    time = website.find("p", attrs={"style": "font-size:13px"})

    checkat = "Updated at " + time.text[68:]
    return (
        "CC Data Bot by Hugo\n"
        + finalstring
        + checkat
        + "\nTo get course info\n"
        + "http://commoncore.hku.hk/"
        + code
    )


def cc(bot, update):
    bot.sendMessage(
        chat_id=update.message.chat_id, text=check_vacancies(update.message.text)
    )


if __name__ == "__main__":
    TOKEN = os.environ.get("TG_TOKEN", "")
    if TOKEN == "":
        print("Set environment variable 'TG_TOKEN' to your telegram bot token")
        exit(0)
    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher

    # handlers
    start_handler = CommandHandler("start", start)
    help_handler = CommandHandler("help", start)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    updater.start_polling()
    echo_handler = MessageHandler(Filters.text, cc)
    dispatcher.add_handler(echo_handler)
