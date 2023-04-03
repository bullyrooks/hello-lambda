import logging
import logging.config

logging.config.fileConfig('logging.conf')



logger = logging.getLogger(__name__)


def handler(event, context):
    logger.info("handler request in")
    return {
        'statusCode': 200,
        'body': "hello world!"
    }
