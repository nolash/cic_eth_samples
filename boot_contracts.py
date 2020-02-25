import sys
import os
import json
import logging

from session import Session
from contract import ContractTransaction

# set up logging
logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger("main")

# read and set up configuration
ROOT = os.path.dirname(os.path.abspath(__file__))


# set up session object with paths, rcp etc
try:
    config['PATHS']['root'] != None
    ROOT = config['paths']['root']
except:
    pass
s = Session(
        root = ROOT,
)
logg.debug("session: %s %s %s", s.root, s.rpc, s.w3.clientVersion)


# deploy ethertoken contract
c = ContractTransaction(s.w3)
c.fromJsonFile(s.root + "/data/" + 'EtherToken.json')
c.deploy(s.w3.eth.accounts[0])
logg.debug("deploy ethertoken rcpt %s", c.rcpt)
