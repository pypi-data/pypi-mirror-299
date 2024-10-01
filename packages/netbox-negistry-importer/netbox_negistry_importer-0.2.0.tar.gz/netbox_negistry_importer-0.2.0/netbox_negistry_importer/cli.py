from netbox_negistry_importer.importers.Negistry import Negistry
from loguru import logger
import sys

from netbox_negistry_importer.config import settings
import click

logger.remove()
logger.add(sys.stderr,
           format='<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>',
           level=settings.get('LOGLEVEL', 'INFO').upper())


@click.command()
def import_negistry():
    negistry = Negistry()
    negistry.import_as_prefixes()


if __name__ == "__main__":
    import_negistry()
