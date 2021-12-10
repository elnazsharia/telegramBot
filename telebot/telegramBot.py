from telebot import types
import telebot
import random
from datetime import date, datetime
from khayyam import JalaliDatetime
from gtts import gTTS
import qrcode
from playsound import playsound

bot = telebot.TeleBot("2137129971:AAG6DMKN2YCYZLqOafB-Awkit2rySBJdvWA")

user_dict = {}

# this is class user that gets the name of the user and also his/her age


class User:
    def __init__(self, name, text):
        self.name = name
        self.age = None
        self.num = None
        self.array[None] = None
        self.text = text


@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, """\
        Hi there.
        What's your name?
        """)
    bot.register_next_step_handler(message, process_name_step)


def process_name_step(message):
    try:
        name = message.text
        """ user = User(name) """
        bot.reply_to(message, 'Nice to meet you ' + name)
    except Exception as e:
        bot.reply_to(message, 'oooops')


# game of guessing a number
@bot.message_handler(commands=["game"])
def guse_number_game(message):
    global number
    number = random.randint(1, 100)
    user = bot.send_message(message.chat.id, "Please guess a number! ")
    bot.register_next_step_handler(user, game)


def game(user_guse):
    global number
    if user_guse.text == "Guess Game":
        user_guse = bot.send_message(
            user_guse.chat.id, "What number you guess ")
        number = random.randint(1, 100)
        bot.register_next_step_handler(user_guse, game)
    else:
        try:
            if int(user_guse.text) < number:
                user_guse = bot.send_message(user_guse.chat.id, "GO UP")
                bot.register_next_step_handler(user_guse, game)
            elif int(user_guse.text) > number:
                user_guse = bot.send_message(user_guse.chat.id, "GO DOWN")
                bot.register_next_step_handler(user_guse, game)
            else:
                bot.send_message(user_guse.chat.id, "Congradulation")
        except:
            user_guse = bot.send_message(
                user_guse.chat.id, "Please enter number")
            bot.register_next_step_handler(user_guse, game)


@bot.message_handler(commands=['age'])
def convert_age(massage):
    bot.reply_to(massage, """\
        please enter your birthday ->(1377/8/11)<-
        """)
    bot.register_next_step_handler(massage, convert_to)


def convert_to(massage):
    try:
        birth = list(map(int, massage.text.split('/')))
        diffrence = JalaliDatetime.now(
        ) - JalaliDatetime(birth[0], birth[1], birth[2])
        diffrence = str(diffrence).split()
        days = int(diffrence[0])
        bot.reply_to(massage, days//365)

    except Exception as e:
        bot.reply_to(massage, 'oooops')


# find the maximum number in an array
@bot.message_handler(commands=['max'])
def max_number(message):
    bot.reply_to(message, """\
        Please enter an array of numbers:
        for example:1-2-4-7
    """)
    bot.register_next_step_handler(message, process_array_max)


def process_array_max(message):

    try:
        numbers = list(map(int, message.text.split('-')))
        bot.send_message(message.chat.id, max(numbers))
    except Exception as e:
        bot.reply_to(message, 'oooops')


@bot.message_handler(commands=['argmax'])
def max_arr_(message):
    array = bot.send_message(
        message.chat.id, 'Enter your array :9,15,8,3')
    bot.register_next_step_handler(array, max_index)


def max_index(message):
    numbers = list(map(int, message.text.split(',')))
    bot.send_message(message.chat.id, numbers.index(max(numbers)))


@bot.message_handler(commands=['voice'])
def process_voice(message):
    bot.reply_to(message, 'Type yout text')
    bot.register_next_step_handler(message, voice_en)


def voice_en(message):
    language = 'en'
    my_text = message.text
    myObj = gTTS(text=my_text, lang=language, slow=False)
    myObj = myObj.save("myObj.mp3")
    """ new_myObj = playsound("myObj.mp3") """
    new_myObj = open("myObj.mp3", 'rb')
    bot.send_audio(message.chat.id, new_myObj)


@bot.message_handler(commands=['qrcode'])
def process_qrcode(message):
    bot.reply_to(message, """\
        Please type whatever you want!
    """)
    bot.register_next_step_handler(message, qrcode_step)


def qrcode_step(message):
    try:

        qr = qrcode.QRCode(
            version=1,
            box_size=10,
            border=5)
        qr.add_data(message.text)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        img.save('qrcode001.png')
        show_image = open("qrcode001.png", 'rb')
        bot.send_photo(message.chat.id, show_image)
    except Exception as e:
        bot.reply_to(message, 'oooops')


@bot.message_handler(commands=['help'])
def process_help(message):
    bot.send_message(message.chat.id, """\
    commands are
    1-start:             
    it gets your name and welcome you
    2-game:              
    playe a game of numbers
    3-age:             
    you in enter your compelete birthday in shamsi calender and it sends you what is your age
    4-max:               
    you send an array of numbers and it returns the maximum number
    5-maxarg:            
    you ssend an array of numbers and it returns you the index of the maximmum number
    6-voic:              
    you type a text and it converts it into a voice and send to you
    7-qrcode:            
    you type a text and it makes the qrcode and send it for you""")


bot.infinity_polling()
