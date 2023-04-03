import logging
import logging.config

from helloworld.chat import Chat

logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)


def handler(event, context):
    logger.info("handler request in")
    return {
        'statusCode': 200,
        'body': Chat.getMessage().json()
    }
