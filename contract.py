import json
import os
import logging
import time

logg = logging.getLogger('contract')

class ContractTransaction:

    """Encapsulates a single contract transaction

    Args:
        w3l: If speificed sets static web3 object for all contract transactions
    """
    def __init__(self, w3l, addr):
        self.contract = None
        self.hash = None
        self.rcpt = None
        self.addr = addr
        if w3l != None:
            self.w3 = w3l


    """Load contract data from json file

    Uses json format from truffle build 
    
    Args:
        js_file: absolute path to json file

    todo:
        check if json format from truffle is same as remix etc
    """
    def fromJsonFile(self, js_file, address=None):
        fd = os.open(js_file, os.O_RDONLY)
        data = os.read(fd, 1024 * 1024 * 10)
        os.close(fd)
        contract_json = json.loads(data)
        self.contract = self.w3.eth.contract(address=address, bytecode=contract_json['bytecode'], abi=contract_json['abi'])


    """Call constructor for contract

    Args:
        account:
            web3 account object
    """
    def deploy(self, account, *args):
        hsh = ''
        if len(args) == 0:
            hsh = self._deployNoArgs(account)
        if len(args) == 1:
            hsh = self._deployOneArgs(account, args[0])
        if len(args) == 2:
            hsh = self._deployTwoArgs(account, args[0], args[1])
        if len(args) == 3:
            hsh = self._deployThreeArgs(account, args[0], args[1], args[2])
        if len(args) == 4:
            hsh = self._deployFourArgs(account, args[0], args[1], args[2], args[3])
        if len(args) == 5:
            hsh = self._deployFiveArgs(account, args[0], args[1], args[2], args[3], args[4])
        if hsh == '':
            raise Exception('hash missing ' + str(self.contract))
        logg.debug("deploy hash %s", hsh)
        self.rcpt = self.w3.eth.waitForTransactionReceipt(hsh)
        self.hash = hsh.hex()

    def _deployNoArgs(self, account):
       return self.contract.constructor().transact({'from': account})
    
    def _deployOneArgs(self, account, one):
       return self.contract.constructor(one).transact({'from': account})

    def _deployTwoArgs(self, account, one, two):
       return self.contract.constructor(one, two).transact({'from': account})

    def _deployThreeArgs(self, account, one, two, three):
        return self.contract.constructor(one, two, three).transact({'from': account})

    def _deployFourArgs(self, account, one, two, three, four):
       return self.contract.constructor(one, two, three, four).transact({'from': account})

    def _deployFiveArgs(self, account, one, two, three, four, five):
        return self.contract.constructor(one, two, three, four, five).transact({'from': account, 'gas': 6000000})


    """Call function on contract with eth value transfer

    Args:
        addr:
            address of contract
        value: 
            eth value to send to contract (account must have enough balance)
        functionName:
            function name to call
        args:
            array of args to pass to contract function
    """        
    def callValue(self, addr, value, functionName, *args):
        f = self.contract.get_function_by_name(functionName)
        if len(args) == 1:
            return self._callValueOneArg(f, args[0])


    def _callValueOneArg(self, f, arg):
        return f(args).transact({
            'from': self.addr,
            'value': value,
        })


    """Call function on contract with eth value transfer

    Args:
        addr:
            address of contract
        functionName:
            function name to call
        args:
            array of args to pass to contract function
    """        
    def call(self, addr, functionName, *args):
        f = self.contract.get_function_by_name(functionName)
        if len(args) == 2:
            return self._callTwoArg(f, addr, args[0], args[1])


    def _callTwoArg(self, f, addr, one, two):
        return f(one, two).transact({
            'from': self.addr,
        })
