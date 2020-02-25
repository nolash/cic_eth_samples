#!/usr/bin/python3

import sys
import logging

SEMPO_ROOT = "/home/lash/src/ext/sempo/SempoBlockchain"
SEMPO_PATHS = ["app/server", "app", "."]

logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger("main")

# add include paths to sys search path
# (move to init)
for i in range(len(SEMPO_PATHS)):
    p = SEMPO_ROOT + "/" + SEMPO_PATHS[i]
    logg.debug("adding sys path: %s", p)
    sys.path.append(p)

from utils import blockchain_tasks
from server import create_app

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        b = blockchain_tasks.BlockchainTasker()
        b.deploy_exchange_network("0xa4783439e84b594661ef74540889fc17fe53ce2e")
