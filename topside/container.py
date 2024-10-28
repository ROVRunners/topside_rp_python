import abc
import logging
import sys
from dependency_injector import containers, providers

class Container(containers.DeclarativeContainer):
    networkconfig = providers.Configuration()

    logging = providers.Resource(
        logging.basicConfig,
        level=logging.INFO,
        stream=sys.stdout,
    )
