import sys
import os
import json
import logging
import configparser
from web3 import Web3

# set up logging
logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger("main")

# read and set up configuration
ROOT = os.path.dirname(os.path.abspath(__file__))
config = configparser.ConfigParser()
config.read("config.ini")


class ContractTransaction:

    w3 = None

    def __init__(self, w3l):
        self.contract = None
        self.hash = None
        self.rcpt = None
        if w3l != None:
            self.w3 = w3l

    def fromJsonFile(self, js_file):
        fd = os.open(js_file, os.O_RDONLY)
        data = os.read(fd, 1024000)
        os.close(fd)
        contract_json = json.loads(data)
        self.contract = self.w3.eth.contract(bytecode=contract_json['bytecode'], abi=contract_json['abi'])

    def deploy(self, account):
        self.hash = self.contract.constructor().transact({'from': account})
        self.rcpt = self.w3.eth.waitForTransactionReceipt(self.hash)

    def call(self, functionName):
        pass


class Session:
   
    w3 = None
    root = ""
    rpc = "http://localhost:8545"

    def __init__(self, **kwargs):
        if kwargs['root'] != None:
            self.root = kwargs['root']
        if kwargs['rpc'] != None:
            self.rpc = kwargs['rpc']

        w3provider = Web3.HTTPProvider(self.rpc)
        self.w3 = Web3(w3provider)

try:
    config['PATHS']['root'] != None
    ROOT = config['paths']['root']
except:
    pass

# set up global vars for easy reading later
# ETH_RPC = config['ETH']['rpc_protocol'] + '://' + config['ETH']['rpc_host'] + ":" + config['ETH']['rpc_port']

logg.debug("using root: %s", ROOT)

s = Session(
        root = ROOT,
        rpc = config['ETH']['rpc_protocol'] + '://' + config['ETH']['rpc_host'] + ":" + config['ETH']['rpc_port'],
)
logg.debug("session: %s %s %s", s.root, s.rpc, s.w3.clientVersion)


# deploy ethertoken contract
c = ContractTransaction(s.w3)
c.fromJsonFile(s.root + "/data/" + 'EtherToken.json')
c.deploy(s.w3.eth.accounts[0])
logg.debug("deploy ethertoken rcpt %s", c.rcpt)
