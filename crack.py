import os
import uuid
import string
import random
import requests
import time
import telebot

# Initialize bot with your token
bot = telebot.TeleBot("7358264322:AAHUP1KZSzold1VsvhiFuf6K1mWFZwWogZE")

class Pyinzenjer:
    def __init__(self, target):
        self.target = target
        if "@" in self.target:
            self.data = {
                "_csrftoken":
                "".join(
                    random.choices(string.ascii_lowercase +
                                   string.ascii_uppercase + string.digits,
                                   k=32)),
                "user_email":
                self.target,
                "guid":
                uuid.uuid4(),
                "device_id":
                uuid.uuid4()
            }
        else:
            self.data = {
                "_csrftoken":
                "".join(
                    random.choices(string.ascii_lowercase +
                                   string.ascii_uppercase + string.digits,
                                   k=32)),
                "username":
                self.target,
                "guid":
                uuid.uuid4(),
                "device_id":
                uuid.uuid4()
            }

    def send_password_reset(self):
        head = {
            "user-agent":
            f"Instagram 150.0.0.0.000 Android (29/10; 300dpi; 720x1440; {''.join(random.choices(string.ascii_lowercase+string.digits, k=16))}/{''.join(random.choices(string.ascii_lowercase+string.digits, k=16))}; {''.join(random.choices(string.ascii_lowercase+string.digits, k=16))}; {''.join(random.choices(string.ascii_lowercase+string.digits, k=16))}; en_GB;)"
        }
        req = requests.post(
            "https://i.instagram.com/api/v1/accounts/send_password_reset/",
            headers=head,
            data=self.data)
        return req.json(), req.status_code

# Start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hello, I'm ninja hatori, made by @kiltes. Hit /help to use me")

# Help command
@bot.message_handler(commands=['help'])
def help_command(message):
    bot.reply_to(message,
                 "*Available Commands:*\n"
                 "/start - Start the bot\n"
                 "/help - Show all commands\n"
                 "/ping - Check if the bot is alive\n"
                 "/reset <target> - Send a password reset request for a target\n",
                 parse_mode="Markdown")

# Ping command
@bot.message_handler(commands=['ping'])
def ping(message):
    start_time = time.time()
    bot.send_chat_action(message.chat.id, 'typing')
    ping_duration = round((time.time() - start_time) * 1000)
    bot.reply_to(message, f"!!Bot is alive\nPing - `{ping_duration} ms`", parse_mode="Markdown")

# Reset password command
@bot.message_handler(commands=['reset'])
def reset_password(message):
    try:
        target = message.text.split()[1]
    except IndexError:
        bot.reply_to(message, "Please provide a valid target username or email.")
        return

    if target[0] == "@":
        bot.reply_to(message, "Enter the username without '@'")
        return

    pyinzenjer = Pyinzenjer(target)
    response, status_code = pyinzenjer.send_password_reset()

    if "obfuscated_email" in response:
        obfuscated_email = response["obfuscated_email"]
        status = response.get("status", "unknown")
        bot.reply_to(
            message,
            f"*PASSWORD RESET LINK SENT TO THE TARGET*\n"
            f"TARGET EMAIL - `{obfuscated_email}`\n"
            f"STATUS - `{status}`\n"
            f"BOT BY - @kiltes",
            parse_mode="Markdown"
        )
    else:
        bot.reply_to(message, f"Failed: {response.get('message', 'Unknown error')}")

# Polling
bot.polling()
