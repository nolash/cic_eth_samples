import json
import os

class ContractTransaction:

    """Encapsulates a single contract transaction

    Args:
        w3l: If speificed sets static web3 object for all contract transactions
    """
    w3 = None
    def __init__(self, w3l):
        self.contract = None
        self.hash = None
        self.rcpt = None
        if w3l != None:
            self.w3 = w3l


    """Load contract data from json file

    Uses json format from truffle build 
    
    Args:
        js_file: absolute path to json file

    todo:
        check if json format from truffle is same as remix etc
    """
    def fromJsonFile(self, js_file):
        fd = os.open(js_file, os.O_RDONLY)
        data = os.read(fd, 1024000)
        os.close(fd)
        contract_json = json.loads(data)
        self.contract = self.w3.eth.contract(bytecode=contract_json['bytecode'], abi=contract_json['abi'])

    """Call constructor for contract

    Args:
        account:
            web3 account object
    """
    def deploy(self, account):
        self.hash = self.contract.constructor().transact({'from': account})
        self.rcpt = self.w3.eth.waitForTransactionReceipt(self.hash)

    """Call function on contract

    Args:
        functionName:
            function name to call
        args:
            array of args to function
    """        
    def call(self, functionName):
        pass


