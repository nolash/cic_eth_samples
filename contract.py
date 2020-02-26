import json
import os
import logging

logg = logging.getLogger('contract')
GAS_DONTCARE = 8000000

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
        if len(args) == 1:
            hsh = self._deployOneArgs(account, args[0])
        elif len(args) == 2:
            hsh = self._deployTwoArgs(account, args[0], args[1])
        elif len(args) == 3:
            hsh = self._deployThreeArgs(account, args[0], args[1], args[2])
        elif len(args) == 4:
            hsh = self._deployFourArgs(account, args[0], args[1], args[2], args[3])
        elif len(args) == 5:
            hsh = self._deployFiveArgs(account, args[0], args[1], args[2], args[3], args[4])
        else:
            hsh = self._deployNoArgs(account)
        if hsh == '':
            raise Exception('hash missing ' + str(self.contract))
        logg.debug("deploy hash %s", hsh)
        self.rcpt = self.w3.eth.waitForTransactionReceipt(hsh)
        self.hash = hsh.hex()

    def _deployNoArgs(self, account):
        return self.contract.constructor().transact({'from': account, 'gas': 9000000})
    
    def _deployOneArgs(self, account, one):
       return self.contract.constructor(one).transact({'from': account, 'gas': 9000000})

    def _deployTwoArgs(self, account, one, two):
       return self.contract.constructor(one, two).transact({'from': account, 'gas': 9000000})

    def _deployThreeArgs(self, account, one, two, three):
        return self.contract.constructor(one, two, three).transact({'from': account, 'gas': 9000000})

    def _deployFourArgs(self, account, one, two, three, four):
       return self.contract.constructor(one, two, three, four).transact({'from': account, 'gas': 9000000})

    def _deployFiveArgs(self, account, one, two, three, four, five):
        return self.contract.constructor(one, two, three, four, five).transact({'from': account, 'gas': 9000000})


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
            return self._callValueOneArgs(addr, value, f, args[0])
        else:
            return self._callValueNoArgs(addr, value, f)

    def _callValueNoArgs(self, addr, value, f):
        return f().transact({
            'to': addr,
            'from': self.addr,
            'value': value,
        })
         
    def _callValueOneArgs(self, addr, f, arg):
        return f(args).transact({
            'to': addr,
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
        hsh = ''
        f = self.contract.get_function_by_name(functionName)
        if len(args) == 1:
            hsh = self._callOneArgs(f, addr, args[0])
        elif len(args) == 2:
            hsh = self._callTwoArgs(f, addr, args[0], args[1])
        elif len(args) == 3:
            hsh = self._callThreeArgs(f, addr, args[0], args[1], args[2])
        elif len(args) == 4:
            hsh = self._callFourArgs(f, addr, args[0], args[1], args[2], args[3])
        else:
            hsh = self._callNoArgs(f, addr)
        self.rcpt = self.w3.eth.waitForTransactionReceipt(hsh)
        self.hash = hsh.hex()


    def _callNoArgs(self, f, addr):
        return f().transact({
            'from': self.addr,
            'gas': GAS_DONTCARE,
            'gasPrice': 10,
        })
 
    def _callOneArgs(self, f, addr, one):
        return f(one).transact({
            'from': self.addr,
            'gas': GAS_DONTCARE,
            'gasPrice': 10,
        })

    def _callTwoArgs(self, f, addr, one, two):
        return f(one, two).transact({
            'from': self.addr,
            'gas': GAS_DONTCARE,
            'gasPrice': 10,
        })

    def _callThreeArgs(self, f, addr, one, two, three):
        return f(one, two, three).transact({
            'from': self.addr,
            'gas': GAS_DONTCARE,
            'gasPrice': 10,
        })


    def _callFourArgs(self, f, addr, one, two, three, four):
        return f(one, two, three, four).transact({
            'from': self.addr,
            'gas': GAS_DONTCARE,
            'gasPrice': 10,
        })


    def read(self, addr, functionName, *args):
        f = self.contract.get_function_by_name(functionName)
        if len(args) == 1:
            return f(args[0]).call()
        elif len(args) == 2:
            return f(args[0], args[1]).call()
        elif len(args) == 3:
            return f(args[0], args[1], args[2]).call()
        elif len(args) == 4:
            return f(args[0], args[1], args[2], args[3]).call()
        else:
            return f().call()


