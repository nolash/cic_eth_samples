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


# deploy two ethertoken contracts
# these hold the reserves of each side of cic conversion

# contract addresses for the reserve tokens
addr_reserve_one = ''
addr_reserve_two = ''
addr_smart_one = ''
addr_smart_two = ''

c = ContractTransaction(s.w3, s.w3.eth.accounts[0])
c.fromJsonFile(s.root + "/data/" + 'EtherToken.json')
c.deploy(s.w3.eth.accounts[0])
addr_reserve_one = c.rcpt['contractAddress']

c = ContractTransaction(s.w3, s.w3.eth.accounts[1])
c.fromJsonFile(s.root + "/data/" + 'EtherToken.json')
c.deploy(s.w3.eth.accounts[1])
addr_reserve_two = c.rcpt['contractAddress']


# deposit eth in the reserve tokens
c = ContractTransaction(s.w3, s.w3.eth.accounts[0])
c.fromJsonFile(s.root + "/data/" + 'EtherToken.json')
c.callValue(addr_reserve_one, 1000000, 'deposit')

c = ContractTransaction(s.w3, s.w3.eth.accounts[0])
c.fromJsonFile(s.root + "/data/" + 'EtherToken.json')
c.callValue(addr_reserve_two, 1000000, 'deposit')


# deploy two smarttoken contracts
c = ContractTransaction(s.w3, s.w3.eth.accounts[0])
c.fromJsonFile(s.root + '/data/' + 'SmartToken.json')
c.deploy(s.w3.eth.accounts[0], 'SmartOne', 'SM1', 3)
addr_smart_one = c.rcpt['contractAddress']

c = ContractTransaction(s.w3, s.w3.eth.accounts[1])
c.fromJsonFile(s.root + '/data/' + 'SmartToken.json')
c.deploy(s.w3.eth.accounts[1], 'SmartOne', 'SM2', 3)
addr_smart_two = c.rcpt['contractAddress']


# issue smart tokens
c = ContractTransaction(s.w3, s.w3.eth.accounts[0])
c.fromJsonFile(s.root + '/data/' + 'SmartToken.json', addr_smart_one)
c.call(s.w3.eth.accounts[0], 'issue', s.w3.eth.accounts[0], 40000)

c = ContractTransaction(s.w3, s.w3.eth.accounts[1])
c.fromJsonFile(s.root + '/data/' + 'SmartToken.json', addr_smart_two)
c.call(s.w3.eth.accounts[1], 'issue', s.w3.eth.accounts[1], 40000)

