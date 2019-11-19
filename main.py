import os
import sys
import json
import logging
import telegram

from commands import command_handler, default_handler, is_command, parse_command
from exceptions import CommandNotFound, CharacterNotFound, CampaignNotFound, InvalidCommand

from telegram.ext import Updater
from telegram.ext import CommandHandler

logger = logging.getLogger()
if logger.handlers:
    for handler in logger.handlers:
        logger.removeHandler(handler)
logging.basicConfig(format='%(message)s', level=logging.INFO)

OK_RESPONSE = {
    'statusCode': 200,
    'headers': {'Content-Type': 'application/json'},
    'body': json.dumps('ok')
}
ERROR_RESPONSE = {
    'statusCode': 500,
    'body': json.dumps('Oops, something went wrong!')
}

def configure_telegram():
    """
    Configures the bot with a Telegram Token.
    Returns a bot instance.
    """

    TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
    if not TELEGRAM_TOKEN:
        logger.error('The TELEGRAM_TOKEN must be set')
        raise NotImplementedError

    return telegram.Bot(TELEGRAM_TOKEN)

def webhook(event, context):
    """
    Runs the Telegram webhook.
    """

    bot = configure_telegram()
    logger.info(json.loads(event.get('body')))

    if event.get('httpMethod') == 'POST' and event.get('body'):
        update = telegram.Update.de_json(json.loads(event.get('body')), bot)

        if not is_command(update):
            return OK_RESPONSE

        username = update.message.from_user.username if update.message.from_user.username else update.message.from_user.first_name
        command = parse_command(update.message.text)
        txt_args = ' '.join(update.message.text.split(' ')[1:])

        try:
            command_handler(command)(bot, update, command, txt_args)
        except (CommandNotFound, InvalidCommand):
            default_handler(bot, update, 'Invalid command')
        except CharacterNotFound:
            default_handler(bot, update, 'Character not found. Cannot execute command')
        except CampaignNotFound:
            default_handler(bot, update, 'Campaign not found. There must be an active campaign')
        except json.JSONDecodeError:
            default_handler(bot, update, 'Error parsing JSON')
        except NotADM:
            default_handler(bot, update, f'Only the Dungeon Master can execute {command} command')
        #except Exception:
        #    logger.error(sys.exc_info()[2])
        #    default_handler(bot, update, 'Unhandled error. Check server logs for more details')

    return OK_RESPONSE


def set_webhook(event, context):
    """
    Sets the Telegram bot webhook.
    """

    logger.info('Event: {}'.format(event))
    bot = configure_telegram()
    url = 'https://{}/{}/'.format(
        event.get('headers').get('Host'),
        event.get('requestContext').get('stage'),
    )
    webhook = bot.set_webhook(url)

    if webhook:
        return OK_RESPONSE

    return ERROR_RESPONSE
