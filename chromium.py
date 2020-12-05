from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
import logging
from telegram.ext import Updater, CommandHandler, run_async
from telegram import ChatAction
from config import Config
from os import execl
from sys import executable
import pickle

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
updater = Updater(token = Config.BOT_TOKEN, use_context=True)
dp = updater.dispatcher
options = webdriver.ChromeOptions()
options.add_argument("--disable-infobars")
options.add_argument("--window-size=1200,800")
options.add_argument("user-agent='User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'")
options.add_experimental_option("prefs", { \
    "profile.default_content_setting_values.media_stream_mic": 2,     # 1:allow, 2:block
    "profile.default_content_setting_values.media_stream_camera": 2,
     "profile.default_content_setting_values.notifications": 2
  })
browser = webdriver.Chrome(options=options)
title=0

@run_async
def restart(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Restarting, Please wait!")
    browser.quit()
    execl(executable, executable, "chromium.py")

def status(update, context):
	browser.save_screenshot("ss.png")
	context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.UPLOAD_PHOTO)
	context.bot.send_photo(chat_id=update.message.chat_id, photo=open('ss.png', 'rb'), timeout = 120).message_id
	os.remove('ss.png')

def login(update, context):
	try:
		context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
		usernameStr = Config.USERNAME
		passwordStr = Config.PASSWORD
		browser.get('https://accounts.google.com/o/oauth2/auth/identifier?client_id=717762328687-iludtf96g1hinl76e4lc1b9a82g457nn.apps.googleusercontent.com&scope=profile%20email&redirect_uri=https%3A%2F%2Fstackauth.com%2Fauth%2Foauth2%2Fgoogle&state=%7B%22sid%22%3A1%2C%22st%22%3A%2259%3A3%3Abbc%2C16%3Afad07e7074c3d678%2C10%3A1601127482%2C16%3A9619c3b16b4c5287%2Ca234368b2cab7ca310430ff80f5dd20b5a6a99a5b85681ce91ca34820cea05c6%22%2C%22cdl%22%3Anull%2C%22cid%22%3A%22717762328687-iludtf96g1hinl76e4lc1b9a82g457nn.apps.googleusercontent.com%22%2C%22k%22%3A%22Google%22%2C%22ses%22%3A%22d18871cbc2a3450c8c4114690c129bde%22%7D&response_type=code&flowName=GeneralOAuthFlow')
		username = browser.find_element_by_id('identifierId')
		username.send_keys(usernameStr)
		nextButton = browser.find_element_by_id('identifierNext')
		nextButton.click()
		time.sleep(7)
		browser.save_screenshot("ss.png")
		context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.UPLOAD_PHOTO)
		context.bot.send_photo(chat_id=update.message.chat_id, photo=open('ss.png', 'rb'), timeout = 120).message_id
		os.remove('ss.png')
		password = browser.find_element_by_xpath("//input[@class='whsOnd zHQkBf']")
		password.send_keys(passwordStr)
		signInButton = browser.find_element_by_id('passwordNext')
		signInButton.click()
		time.sleep(7)
		browser.get('https://youtube.com')
		time.sleep(7)
		if os.path.exists("login.pkl"):
			os.remove('login.pkl')
			time.sleep(7)
		pickle.dump( browser.get_cookies() , open("login.pkl","wb"))
		context.bot.send_message(chat_id=update.message.chat_id, text="Logged In Successfully!")
	except Exception as e:
		context.bot.send_message(chat_id=update.message.chat_id, text="Error Occurred . Try to /login on Local Machine not Heroku")
		print(str(e))
		try:
			browser.save_screenshot("ss.png")
			context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.UPLOAD_PHOTO)
			context.bot.send_photo(chat_id=update.message.chat_id, photo=open('ss.png', 'rb'), timeout = 120).message_id
			os.remove('ss.png')
		except:
			pass
	browser.quit()
	execl(executable, executable, "chromium.py")

def youtube(update,context):

	def newvideo(context):
		global title
		x = title
		try:
			browser.refresh()
			latestvid = browser.find_element_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-grid-renderer/div[1]/ytd-grid-video-renderer[1]/div[1]/div[1]/div[1]/h3')
			title = str(latestvid.text)
			if (x != title and x != 0):
				browser.find_element_by_xpath('//*[@id="items"]/ytd-grid-video-renderer[1]').click()
				time.sleep(5)
				channel = str(browser.find_element_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[4]/div[1]/div/div[6]/div[3]/ytd-video-secondary-info-renderer/div/div[2]/ytd-video-owner-renderer/div[1]/ytd-channel-name/div/div').text)
				actions = browser.find_element_by_xpath('//html')
				actions.send_keys(Keys.PAGE_DOWN)
				commentStr = Config.MESSAGE
				time.sleep(3)
				browser.find_element_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[4]/div[1]/div/ytd-comments/ytd-item-section-renderer/div[1]/ytd-comments-header-renderer/div[5]/ytd-comment-simplebox-renderer/div[1]').click()
				time.sleep(3)
				browser.find_element_by_id('contenteditable-root').send_keys(commentStr)
				time.sleep(3)
				browser.save_screenshot("ss.png")
				context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.UPLOAD_PHOTO)
				context.bot.send_photo(chat_id=update.message.chat_id, photo=open('ss.png', 'rb'), caption="Commented On New Video of " + channel + "\n \n" + title , timeout = 120).message_id
				os.remove('ss.png')
				browser.find_element_by_id('submit-button').click()
				time.sleep(3)
				browser.get(yt_channel + '/videos')
				time.sleep(5)

		except Exception as e:
			context.bot.send_message(chat_id=update.message.chat_id, text="Error Occurred Please Check")
			print(str(e))
			try:
				browser.save_screenshot("ss.png")
				context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.UPLOAD_PHOTO)
				context.bot.send_photo(chat_id=update.message.chat_id, photo=open('ss.png', 'rb'), timeout = 120).message_id
				os.remove('ss.png')
			except:
				pass
			browser.quit()
			execl(executable, executable, "chromium.py")


	logging.info("STARTED COMMENTOR!")
	try:
		context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
		yt_channel = update.message.text.split()[-1]
		cookies = pickle.load(open("login.pkl", "rb"))
		browser.get('https://accounts.google.com/o/oauth2/auth/identifier?client_id=717762328687-iludtf96g1hinl76e4lc1b9a82g457nn.apps.googleusercontent.com&scope=profile%20email&redirect_uri=https%3A%2F%2Fstackauth.com%2Fauth%2Foauth2%2Fgoogle&state=%7B%22sid%22%3A1%2C%22st%22%3A%2259%3A3%3Abbc%2C16%3Afad07e7074c3d678%2C10%3A1601127482%2C16%3A9619c3b16b4c5287%2Ca234368b2cab7ca310430ff80f5dd20b5a6a99a5b85681ce91ca34820cea05c6%22%2C%22cdl%22%3Anull%2C%22cid%22%3A%22717762328687-iludtf96g1hinl76e4lc1b9a82g457nn.apps.googleusercontent.com%22%2C%22k%22%3A%22Google%22%2C%22ses%22%3A%22d18871cbc2a3450c8c4114690c129bde%22%7D&response_type=code&flowName=GeneralOAuthFlow')
		for cookie in cookies:
			browser.add_cookie(cookie)
		browser.get(yt_channel + '/videos')
		channel = str(browser.find_element_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-browse/div[3]/ytd-c4-tabbed-header-renderer/app-header-layout/div/app-header/div[2]/div[2]/div/div[1]/div/div[1]/ytd-channel-name/div').text)
		context.bot.send_message(chat_id=update.message.chat_id, text="Starting Comment bot For Channel: \n" + channel)
		time.sleep(3)
		browser.save_screenshot("ss.png")
		context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.UPLOAD_PHOTO)
		context.bot.send_photo(chat_id=update.message.chat_id, photo=open('ss.png', 'rb'), caption="Waiting for New Video", timeout = 120).message_id
		os.remove('ss.png')

	except Exception as e:
		if not os.path.exists("login.pkl"):
			context.bot.send_message(chat_id=update.message.chat_id, text="Login Credentials Not generated. Try /login or re-deploy Bot")
		else:
			context.bot.send_message(chat_id=update.message.chat_id, text="Error Occurred Please Check")
		print(str(e))
		try:
			browser.save_screenshot("ss.png")
			context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.UPLOAD_PHOTO)
			context.bot.send_photo(chat_id=update.message.chat_id, photo=open('ss.png', 'rb'), timeout = 120).message_id
			os.remove('ss.png')
		except:
			pass
		browser.quit()
		execl(executable, executable, "chromium.py")
	j = updater.job_queue
	j.run_repeating(newvideo, 10, 0)

def main():
	dp.add_handler(CommandHandler("yt", youtube))
	dp.add_handler(CommandHandler("login", login))
	dp.add_handler(CommandHandler("restart", restart))
	dp.add_handler(CommandHandler("status", status))
	updater.start_polling()

if __name__ == '__main__':
    main()
