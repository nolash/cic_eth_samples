import sys
import os
import json
import logging

from session import Session
from contract import ContractTransaction

zeroAddr = '0x0000000000000000000000000000000000000000'

# set up logging
logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger('main')

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
addr_foo_one = ''
addr_foo_two = ''

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
r = c.callValue(addr_reserve_one, 1000000, 'deposit')

c = ContractTransaction(s.w3, s.w3.eth.accounts[1])
c.fromJsonFile(s.root + "/data/" + 'EtherToken.json')
c.callValue(addr_reserve_two, 1000000, 'deposit')


# deploy two foo-token contracts
#c = ContractTransaction(s.w3, s.w3.eth.accounts[2])
#c.fromJsonFile(s.root + '/data/' + 'FooToken.json')
#c.deploy(s.w3.eth.accounts[2], 'FooOne', 'FOO1', 3, 40000)
#addr_foo_one = c.rcpt['contractAddress']
#
#c = ContractTransaction(s.w3, s.w3.eth.accounts[3])
#c.fromJsonFile(s.root + '/data/' + 'FooToken.json')
#c.deploy(s.w3.eth.accounts[3], 'FooTwo', 'FOO2', 3, 40000)
#addr_foo_two = c.rcpt['contractAddress']


# deploy two smarttoken contracts
c = ContractTransaction(s.w3, s.w3.eth.accounts[0])
c.fromJsonFile(s.root + '/data/' + 'SmartToken.json')
c.deploy(s.w3.eth.accounts[0], 'SmartOne', 'SM1', 3)
addr_smart_one = c.rcpt['contractAddress']

c = ContractTransaction(s.w3, s.w3.eth.accounts[1])
c.fromJsonFile(s.root + '/data/' + 'SmartToken.json')
c.deploy(s.w3.eth.accounts[1], 'SmartOne', 'SM2', 3)
addr_smart_two = c.rcpt['contractAddress']




# deploy smart tokenn controllers
c = ContractTransaction(s.w3, s.w3.eth.accounts[0])
c.fromJsonFile(s.root + '/data/' + 'SmartTokenController.json')
c.deploy(s.w3.eth.accounts[0], addr_smart_one)
addr_smartcontroller_one = c.rcpt['contractAddress']

c = ContractTransaction(s.w3, s.w3.eth.accounts[1])
c.fromJsonFile(s.root + '/data/' + 'SmartTokenController.json')
c.deploy(s.w3.eth.accounts[1], addr_smart_two)
addr_smartcontroller_two = c.rcpt['contractAddress']


# deploy converter registry
c = ContractTransaction(s.w3, s.w3.eth.accounts[0])
c.fromJsonFile(s.root + '/data/' + 'BancorConverterRegistry.json')
c.deploy(s.w3.eth.accounts[0])
addr_registry = c.rcpt['contractAddress']


# deploy bancon network linked to registry
c = ContractTransaction(s.w3, s.w3.eth.accounts[0])
c.fromJsonFile(s.root + '/data/' + 'BancorNetwork.json')
c.deploy(s.w3.eth.accounts[0], addr_registry)
addr_network = c.rcpt['contractAddress']

# deploy contract registry utility contract
c = ContractTransaction(s.w3, s.w3.eth.accounts[0])
c.fromJsonFile(s.root + '/data/' + 'ContractRegistry.json')
c.deploy(s.w3.eth.accounts[0])
addr_contractregistry_one = c.rcpt['contractAddress']

c = ContractTransaction(s.w3, s.w3.eth.accounts[1])
c.fromJsonFile(s.root + '/data/' + 'ContractRegistry.json')
c.deploy(s.w3.eth.accounts[1])
addr_contractregistry_two = c.rcpt['contractAddress']


# deploy converter contracts
c = ContractTransaction(s.w3, s.w3.eth.accounts[0])
c.fromJsonFile(s.root + '/data/' + 'BancorConverter.json')
c.deploy(s.w3.eth.accounts[0], addr_smart_one, addr_contractregistry_one, 0, addr_reserve_one, 250000)
addr_converter_one = c.rcpt['contractAddress']

c = ContractTransaction(s.w3, s.w3.eth.accounts[1])
c.fromJsonFile(s.root + '/data/' + 'BancorConverter.json')
c.deploy(s.w3.eth.accounts[1], addr_smart_two, addr_contractregistry_two, 0, addr_reserve_two, 250000)
addr_converter_two = c.rcpt['contractAddress']


# add connector to each token
#c = ContractTransaction(s.w3, s.w3.eth.accounts[0])
#c.fromJsonFile(s.root + '/data/' + 'BancorConverter.json', addr_converter_one)
#c.call(s.w3.eth.accounts[0], 'addConnector', addr_foo_one, 25000, False)
#
#c = ContractTransaction(s.w3, s.w3.eth.accounts[1])
#c.fromJsonFile(s.root + '/data/' + 'BancorConverter.json', addr_converter_two)
#c.call(s.w3.eth.accounts[1], 'addConnector', addr_foo_two, 50000, False)



# set conversion fee on each converter
#c = ContractTransaction(s.w3, s.w3.eth.accounts[0])
#c.fromJsonFile(s.root + '/data/' + 'BancorConverter.json', addr_converter_one)
#c.call(s.w3.eth.accounts[0], 'setConversionFee', 10000)
#
#c = ContractTransaction(s.w3, s.w3.eth.accounts[1])
#c.fromJsonFile(s.root + '/data/' + 'BancorConverter.json', addr_converter_two)
#c.call(s.w3.eth.accounts[1], 'setConversionFee', 20000)


# transfer reserve tokens to converter
c = ContractTransaction(s.w3, s.w3.eth.accounts[0])
c.fromJsonFile(s.root + '/data/' + 'EtherToken.json', addr_reserve_one)
c.call(s.w3.eth.accounts[0], 'transfer', addr_converter_one, 1000000)

c = ContractTransaction(s.w3, s.w3.eth.accounts[1])
c.fromJsonFile(s.root + '/data/' + 'EtherToken.json', addr_reserve_two)
c.call(s.w3.eth.accounts[1], 'transfer', addr_converter_two, 1000000)


# transfer foo-tokens to converter
#c = ContractTransaction(s.w3, s.w3.eth.accounts[2])
#c.fromJsonFile(s.root + '/data/' + 'FooToken.json', addr_foo_one)
#c.call(s.w3.eth.accounts[2], 'transfer', addr_converter_one, 40000)
#
#c = ContractTransaction(s.w3, s.w3.eth.accounts[3])
#c.fromJsonFile(s.root + '/data/' + 'FooToken.json', addr_foo_two)
#c.call(s.w3.eth.accounts[3], 'transfer', addr_converter_two, 40000)


# check the connector balance
c = ContractTransaction(s.w3, s.w3.eth.accounts[0])
c.fromJsonFile(s.root + '/data/' + 'BancorConverter.json', addr_converter_one)
r = c.read(s.w3.eth.accounts[0], 'getConnectorBalance', addr_reserve_one)
r_expect = 1000000
if r != r_expect:
    raise Exception('converter one connector balance; expected ' + str(r_expect) + ', got ' + str(r))

c = ContractTransaction(s.w3, s.w3.eth.accounts[0])
c.fromJsonFile(s.root + '/data/' + 'BancorConverter.json', addr_converter_two)
r = c.read(s.w3.eth.accounts[0], 'getConnectorBalance', addr_reserve_two)
if r != r_expect:
    raise Exception('converter two connector balance; expected  ' + str(r_expect) + ', got ' + str(r))


# issue smart tokens
c = ContractTransaction(s.w3, s.w3.eth.accounts[0])
c.fromJsonFile(s.root + '/data/' + 'SmartToken.json', addr_smart_one)
c.call(s.w3.eth.accounts[0], 'issue', s.w3.eth.accounts[0], 4000000)

c = ContractTransaction(s.w3, s.w3.eth.accounts[1])
c.fromJsonFile(s.root + '/data/' + 'SmartToken.json', addr_smart_two)
c.call(s.w3.eth.accounts[1], 'issue', s.w3.eth.accounts[1], 4000000)


# set allowance for balance of tokens to converters
c = ContractTransaction(s.w3, s.w3.eth.accounts[0])
c.fromJsonFile(s.root + '/data/' + 'EtherToken.json', addr_reserve_one)
c.call(s.w3.eth.accounts[0], 'approve', addr_converter_one, 1000000)

c = ContractTransaction(s.w3, s.w3.eth.accounts[1])
c.fromJsonFile(s.root + '/data/' + 'EtherToken.json', addr_reserve_two)
c.call(s.w3.eth.accounts[1], 'approve', addr_converter_two, 1000000)


# transfer ownership of token to the token itself
c = ContractTransaction(s.w3, s.w3.eth.accounts[0])
c.fromJsonFile(s.root + '/data/' + 'BancorConverter.json', addr_converter_one)
c.call(s.w3.eth.accounts[0], 'transferOwnership', addr_smart_one)
#c.fromJsonFile(s.root + '/data/' + 'SmartToken.json', addr_smart_one)
#c.call(s.w3.eth.accounts[0], 'transferOwnership', addr_converter_one)

c = ContractTransaction(s.w3, s.w3.eth.accounts[1])
c.fromJsonFile(s.root + '/data/' + 'BancorConverter.json', addr_converter_two)
c.call(s.w3.eth.accounts[1], 'transferOwnership', addr_smart_one)
#c.fromJsonFile(s.root + '/data/' + 'SmartToken.json', addr_smart_two)
#c.call(s.w3.eth.accounts[1], 'transferOwnership', addr_converter_two)


# each side accepts token ownership change
c = ContractTransaction(s.w3, s.w3.eth.accounts[0])
#c.fromJsonFile(s.root + '/data/' + 'BancorConverter.json', s.w3.eth.accounts[0])
c.fromJsonFile(s.root + '/data/' + 'BancorConverter.json', s.w3.eth.accounts[0])
c.call(s.w3.eth.accounts[0], 'acceptTokenOwnership')

c = ContractTransaction(s.w3, s.w3.eth.accounts[1])
#c.fromJsonFile(s.root + '/data/' + 'BancorConverter.json', s.w3.eth.accounts[1])
c.fromJsonFile(s.root + '/data/' + 'BancorConverter.json', s.w3.eth.accounts[1])
c.call(s.w3.eth.accounts[1], 'acceptTokenOwnership')


# enable conversions
c = ContractTransaction(s.w3, s.w3.eth.accounts[0])
c.fromJsonFile(s.root + '/data/' + 'BancorConverter.json', addr_converter_one)
c.call(s.w3.eth.accounts[0], 'disableConversions', False)

c = ContractTransaction(s.w3, s.w3.eth.accounts[1])
c.fromJsonFile(s.root + '/data/' + 'BancorConverter.json', addr_converter_two)
c.call(s.w3.eth.accounts[1], 'disableConversions', False)


# do a conversion
c = ContractTransaction(s.w3, s.w3.eth.accounts[0])
c.fromJsonFile(s.root + '/data/' + 'BancorConverter.json', addr_converter_one)
#c.call(s.w3.eth.accounts[0], 'convert', addr_smart_one, addr_reserve_one, 1000, 1)
c.call(s.w3.eth.accounts[0], 'quickConvert', [addr_smart_one, addr_reserve_one], 1000, 1)
logg.info("send smart token back to contract hash %s, rcpt %s", c.hash, c.rcpt)


# output summary of deployed contracts
logg.debug("reserves: %s %s", addr_reserve_one, addr_reserve_two)
logg.debug("tokens: %s %s", addr_smart_one, addr_smart_two)
logg.debug("token controllers: %s %s", addr_smartcontroller_one, addr_smartcontroller_two)
logg.debug("registry: %s %s %s", addr_registry, addr_contractregistry_one, addr_contractregistry_two)
logg.debug("converters: %s %s", addr_converter_one, addr_converter_two)

