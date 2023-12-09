

import logging

from telegram import __version__ as TG_VER

try:
  from telegram import __version_info__
except ImportError:
  __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
  raise RuntimeError(
      f"This example is not compatible with your current PTB version {TG_VER}. To view the "
      f"{TG_VER} version of this example, "
      f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html")

import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from keep_alive import keep_alive
import os
 
keep_alive()

# Define your bot token here
TOKEN = os.environ['TOKEN']


def scrape_paragraphs():
  url = 'https://factrepublic.com/random-facts-generator/'
  headers = {
      'User-Agent':
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
  }
  response = requests.get(url, headers=headers, proxies={})

  if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all paragraphs with class "td-sml-description"
    first_paragraph = soup.find('span', class_='td-sml-description')
    first_source_link = soup.find('a', class_='button source')

    paragraph_text = f"{first_paragraph.p.text.strip()}" if first_paragraph else "No paragraphs found on the page."

    source_link_text = f"Source Link: {first_source_link['href']}" if first_source_link else "No source link found on the page."

    return f"{paragraph_text}\n{source_link_text}"

  else:
    return f"Failed to retrieve the page. Status code: {response.status_code}"


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
  # Call the function to scrape the first paragraph
  result = scrape_paragraphs()
  await update.message.reply_text(result)


if __name__ == '__main__':
  print('Starting..')
  app = Application.builder().token(TOKEN).build()
  app.add_handler(CommandHandler('start', start_command))
  print('Running..')
  app.run_polling(poll_interval=3)
while True:
	pass