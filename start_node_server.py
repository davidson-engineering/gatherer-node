import asyncio
import logging
import os
from dotenv import load_dotenv

load_dotenv()

HOSTNAME = os.getenv('HOSTNAME')
PORT = int(os.getenv('PORT'))

from data_node_network.node_data_gatherer import GathererNodeTCP

logger = logging.getLogger(__name__)


def main():
    address = (HOSTNAME, PORT)
    node_id = 0

    # Create and start the server
    node_server = GathererNodeTCP(address=address)
    node_server.start()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    # asyncio.run(main())
    main()
