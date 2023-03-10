from django.core.management.base import BaseCommand
from django.conf import settings
import telebot
from telebot.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
import random

# from telegram import Bot
# from telegram import Update
# from telegram.ext import CallbackContext
# from telegram.ext import CommandHandler
# from telegram.ext import Filters
# from telegram.ext import MessageHandler
# from telegram.ext import Updater
# from telegram.utils.request import Request
#
from test_app.models import Player, Message, Event, EventResult, Basement

bot = telebot.TeleBot(settings.TOKEN, parse_mode=None)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    chat_id = message.chat.id

    p, _ = Player.objects.get_or_create(
        external_id=chat_id,
        defaults={
            'name': message.from_user.username,
        }
    )
    b = Basement.objects.get_or_create(
        defaults={
            'master': p,
        }
    )

    bot.send_message(chat_id, '''Ха-ха ти в підвалі версії alfa 0.1) 
    тут ти можеш:
    /take_hostage - взяти когось в підвал
    /profile - перевірити свій профіль
    /count - переглянути кількість збережених повідомлень
    або просто написати, щось в бот (спробуй написати "Слава Україні! ;) )"
    ''', reply_markup=gen_markup())


def gen_markup():
    markup = ReplyKeyboardMarkup()
    markup.row_width = 2
    events = Event.objects.all()
    for event in events:
        markup.add(KeyboardButton(event.name))
    return markup


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "pgb_clean":
        bot.send_message("You cleaned your room")


# @bot.message_handler(func=lambda message: True)
# def message_handler(message):
#     bot.send_message(message.chat.id, "Шо?", reply_markup=gen_markup())


@bot.message_handler(commands=['count'])
def count_messages(message):
    chat_id = message.chat.id

    p, _ = Player.objects.get_or_create(
        external_id=chat_id,
        defaults={
            'name': message.from_user.username,
        }
    )

    count = Message.objects.filter(profile=p).count()
    reply_text = f'Кількість повідомлень = {count}'
    bot.reply_to(message, reply_text)


def player_hostage(player: Player):
    player_basement = player.basement
    h_player = player_basement.hostage
    return h_player


def player_master(hostage_player: Player):
    basement_in_which_hostage = Basement.objects.filter(hostage_id=hostage_player.pk).first()
    if basement_in_which_hostage == None:
        m_player = None
    else:
        m_player = basement_in_which_hostage.master
    return m_player


@bot.message_handler(commands=['take_hostage'])
def take_hostage(message):
    msg = bot.reply_to(message, "Введи ім'я людини яку хочеш узяти в заручники (тег без @)")
    bot.register_next_step_handler(msg, hostage)


def hostage(message):
    try:
        chat_id = message.chat.id
        h_name = message.text
        h_player = Player.objects.filter(name=h_name).first()

        p, _ = Player.objects.get_or_create(
            external_id=chat_id,
        )
        b = p.basement

        if player_master(h_player) == None and h_name != p.name and p != h_player:
            b.hostage = Player.objects.filter(name=h_name)[0]
            b.save()
            print(Basement.objects.filter(hostage_id=h_player.pk)[0])
            bot.send_message(chat_id, "Ти узяв в заручники " + h_name)
        elif h_name == p.name:
            reply_text = f"Пробач :( але ти не можеш узяти себе в заручники"
            bot.reply_to(message, reply_text)
        elif p == player_hostage(h_name):
            reply_text = f"Ти в підвалі цього гравця і не можеш закрити його/її свому підвалі"
            bot.reply_to(message, reply_text)
        else:
            reply_text = f"Пробач :( але цей гравець в вже в іншому підвалі"
            bot.reply_to(message, reply_text)

    except Exception as e:
        bot.reply_to(message, 'oooops. Скоріш за все той кого ти хочеш узяти в підвал не в грі.')


@bot.message_handler(commands=['profile'])
def profile_info(message):
    chat_id = message.chat.id
    p, _ = Player.objects.get_or_create(external_id=chat_id)
    p_name = p.name
    p_hostage = p.hostage
    p_master = player_master(p_name)
    message_text = f"Ваш профайл: {p_name}.\n...\nУ вас в підвалі {p_hostage}.\n...\nВи в підвалі у {p_master}."
    bot.send_message(chat_id, message_text)


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    chat_id = message.chat.id
    text = message.text

    if text == 'Слава Україні!' or text == 'Слава Україні':
        bot.reply_to(message, 'Героям слава!')
    elif text == 'Прибирання':
        def predicate(event: Event):
            return event.name == text

        event: Event = next(filter(predicate, Event.objects.all()))

        def mapRes(result: EventResult):
            return result.probability

        result: EventResult = random.choices(event.results.all(), weights=tuple(map(mapRes, event.results.all())), k=1)[
            0]

        bot.send_message(chat_id, result.name)
    else:
        p, _ = Player.objects.get_or_create(
            external_id=chat_id,
            defaults={
                'name': message.from_user.username,
            }
        )
        m = Message(
            profile=p,
            text=text,
        )
        m.save()
        reply_text = f'Ваш ID = {chat_id}\n{text}'
        bot.reply_to(message, reply_text)


bot.infinity_polling()
#
# class Command(BaseCommand):
#     help = 'Telegram-bot'
#
#     def log_errors(f):
#
#         def inner(*args, **kwargs):
#             try:
#                 return f(*args, **kwargs)
#             except Exception as e:
#                 error_message = f'Произошла ошибка: {e}'
#                 print(error_message)
#                 raise e
#
#         return inner
#
#     # @log_errors
#     def do_echo(update: Update, context: CallbackContext):
#         chat_id = update.message.chat_id
#         text = update.message.text
#
#         # p, _ = Profile.objects.get_or_create(
#         #     external_id=chat_id,
#         #     defaults={
#         #         'name': update.message.from_user.username,
#         #     }
#         # )
#         # m = Message(
#         #     profile=p,
#         #     text=text,
#         # )
#         # m.save()
#
#         reply_text = f'Ваш ID = {chat_id}\n{text}'
#         update.message.reply_text(
#             text=reply_text,
#         )
#
#     def handle(self, *args, **options):
#         request = Request(
#             con_pool_size=8,
#             connect_timeout=0.5,
#             read_timeout=1.0,
#         )
#         bot = Bot(
#             request=request,
#             token=settings.TOKEN,
#         )
#         print(bot.get_me())
#
#         updater = Updater(
#             bot=bot,
#             use_context=True,
#         )
#
#         # 2 -- обработчики
#
#         message_handler = MessageHandler(Filters.text, self.do_echo)
#         updater.dispatcher.add_handler(message_handler)
#         # updater.dispatcher.add_handler(CommandHandler('count', do_count))
#
#         # 3 -- запустить бесконечную обработку входящих сообщений
#         updater.start_polling()
#         updater.idle()
