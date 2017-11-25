from telegram.ext import Updater
import telegram
import logging
import urllib.request
from bs4 import BeautifulSoup
import requests
from requests.exceptions import HTTPError

TOKEN = ""
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher
def start(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id, text="type in the cc code e.g. ccst9010 to check info")

from telegram.ext import CommandHandler
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
updater.start_polling()
def echo(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id, text=update.message.text + "fuck")

def checkleft(code):
	if (len(code) != 8):
		return 'Error, no such CC Code'
	#code = input("which cc?\n")
	code = code.upper() #capitalizes code input for easier comparison
	website = BeautifulSoup(urllib.request.urlopen('https://sweb.hku.hk/ccacad/ccc_appl/enrol_stat.html').read(),'lxml')
	listofcells = website.select('body table tr td font')

	#list of cells is a list of text contained in each <font> element in <td> elements
	indices = []
	for i in range(len(listofcells)):
		if code == listofcells[i].getText():
			indices.append(i)
	finalstring = ""
	print(indices)
	if indices == []:
		return 'Error, no such CC Code'
	for index in indices:
		cccode = "CC Code: " + listofcells[index].getText() + '\n'
		title = "CC Name: " + listofcells[index + 1].getText() + '\n'
		subclass = 'SubClass: ' + listofcells[index + 2].getText() + '\n'
		quota = "Quota: " + listofcells[index + 3].getText() + '\n'
		pleft = "Places Left: " + listofcells[index + 4].getText() + '\n'
		waiting = "Waiting: " + listofcells[index + 5].getText() + '\n'
		finalstring = finalstring + cccode + title + subclass + quota + pleft + waiting + '\n'
		print(finalstring)

	#get time from end of page
	time = website.find('p', attrs={'style' : 'font-size:13px'})

	checkat = 'updated at ' + time.text[68:]
	return "CC Data Bot by Hugo\n" + finalstring + checkat + '\nTo get course info\n' + 'http://commoncore.hku.hk/'+code

def cc(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id, text=checkleft(update.message.text))

from telegram.ext import MessageHandler, Filters
echo_handler = MessageHandler(Filters.text, cc)
dispatcher.add_handler(echo_handler)
