from django.core.management.base import BaseCommand
from django.conf import settings
import telebot

# from telegram import Bot
# from telegram import Update
# from telegram.ext import CallbackContext
# from telegram.ext import CommandHandler
# from telegram.ext import Filters
# from telegram.ext import MessageHandler
# from telegram.ext import Updater
# from telegram.utils.request import Request
#
from test_app.models import Player, Message

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

    bot.send_message(chat_id, '''Ха-ха ти в підвалі версії alfa 0.1) 
    тут ти можеш:
    /take_hostage - взяти когось в підвал
    /profile - перевірити свій профіль
    /count - переглянути кількість збережених повідомлень
    або просто написати, щось в бот (спробуй написати "Слава Україні! ;) )"
    ''')


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


def player_hostage(player_name):
    selected_player = Player.objects.filter(name=player_name).first()
    h_player = selected_player.hostage
    return h_player


def player_master(hostage_name):
    h_player = Player.objects.filter(name=hostage_name).first()
    m_player = Player.objects.filter(hostage_id=h_player.pk).first()
    return m_player


@bot.message_handler(commands=['take_hostage'])
def take_hostage(message):
    msg = bot.reply_to(message, "Введи ім'я людини яку хочеш узяти в заручники (тег без @)")
    bot.register_next_step_handler(msg, hostage)


def hostage(message):
    try:
        chat_id = message.chat.id
        h_name = message.text
        hostage_master = player_master(h_name)

        p, _ = Player.objects.get_or_create(
            external_id=chat_id,
        )

        if hostage_master == None and h_name != p.name and p != player_hostage(h_name):
            p.hostage = Player.objects.filter(name=h_name)[0]
            p.save()
            print(Player.objects.filter(name=h_name)[0])
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
        bot.reply_to(message, 'oooops')


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
