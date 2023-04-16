import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests
import json
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hi! I'm a weather bot. \nSend me the name of a city / PIN Code / Co-ordinates and I'll tell you the current weather.")

def weather(update, context):
    location = update.message.text
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "appid": os.getenv("OPENWEATHERMAP_API_KEY"),
        "units": "metric"
    }
    try:
        # LAT & LONG
        if ',' in location:
            lat, lon = location.split(',')
            params['lat'] = float(lat.strip())
            params['lon'] = float(lon.strip())
        # ZIP
        elif location.isdigit() and len(location) == 6:
            params['zip'] = location + ',in'
        # CITY
        else:
            params['q'] = location
    except:
        update.message.reply_text("Sorry, I couldn't understand your input. Please try again.")
        return
    response = requests.get(url, params=params)
    data = json.loads(response.text)
    # Decode Reposnes JSON
    try:
        temperature = round(data['main']['temp'], 2)  # round off to 2 decimal places
        description = data['weather'][0]['description']
        city_name = data['name']
        message = f'The temperature in {city_name} is {temperature}°C with {description}.'
    except KeyError:
        message = 'Sorry, I could not get the weather information. Please try again.'
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

def help(update, context):
    """Display the help message."""
    help_message = "Here are the available commands:\n\n"
    help_message += "-> Name of the City - Get the details of weather for a City.\n"
    help_message += "-> PINCode - Get the details of weather for a PIN Code.\n"
    help_message += "-> Latitude,Longitude - Get the details of weather for a specific co-ordinate.\n"
    help_message += "-> /start - Start the bot.\n"
    help_message += "-> /help - Show this message.\n"
    help_message += "-> /contact - Show the developer's contact details.\n"
    help_message += "-> /stop - To stop the bot.\n"
    update.message.reply_text(help_message)

def contact(update, context):
    """Display the developer's contact details."""
    contact_message = "You can contact the developer at:\n"
    contact_message += "Email: dsouzaglen30@gmail.com\n"
    contact_message += "Linkedin: Glen Dsouza\n"
    contact_message += "Github: GlenDsza\n"
    contact_message += "Telegram: @GlenDsza\n"

     # Define the keyboard buttons
    email_button = InlineKeyboardButton(text="Email", url="mailto:dsouzaglen30@gmail.com")
    linkedin_button = InlineKeyboardButton(text="Linkedin", url="www.linkedin.com/in/glen-dsza")
    github_button = InlineKeyboardButton(text="Github", url="https://github.com/GlenDsza")
    telegram_button = InlineKeyboardButton(text="Telegram", url="https://t.me/GlenDsza")

    # Add the buttons to the keyboard
    keyboard = [[email_button, linkedin_button, github_button, telegram_button]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send the message with the keyboard
    update.message.reply_text(contact_message, reply_markup=reply_markup)

def stop(update, context):
    """Stop the bot."""
    update.message.reply_text("Byee, Have a Good Day! ❤️")
    context.bot.stop()
    exit()

updater = Updater(token=BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

help_handler = CommandHandler('help', help)
dispatcher.add_handler(help_handler)

weather_handler = MessageHandler(Filters.text & ~Filters.command, weather)
dispatcher.add_handler(weather_handler)

stop_handler = CommandHandler('stop', stop)
dispatcher.add_handler(stop_handler)

contact_handler = CommandHandler('contact', contact)
dispatcher.add_handler(contact_handler)

updater.start_polling()
updater.idle()