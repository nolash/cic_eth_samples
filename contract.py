import json
import os
import logging

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
        data = os.read(fd, 1024000)
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
        if len(args) == 3:
            hsh = self._deployThreeArgs(account, args[0], args[1], args[2])
        self.rcpt = self.w3.eth.waitForTransactionReceipt(hsh)
        self.hash = hsh

    def _deployNoArgs(self, account):
       return self.contract.constructor().transact({'from': account})

    def _deployThreeArgs(self, account, one, two, three):
       return self.contract.constructor(one, two, three).transact({'from': account})
    

    """Call function on contract

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


    def call(self, addr, functionName, *args):
        f = self.contract.get_function_by_name(functionName)
        if len(args) == 2:
            return self._callTwoArg(f, addr, args[0], args[1])


    def _callTwoArg(self, f, addr, one, two):
        return f(one, two).transact({
            'from': self.addr,
        })


