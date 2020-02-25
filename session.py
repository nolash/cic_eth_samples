from web3 import Web3
import configparser

class Session:
  
    """Singleton collecting config and rpc objects

    Args:
        root=root:
            root working dir
        rpc=rpc:
            rpc host in format [proto]://[host]:[port]. Default http://localhost:8545
    """
    w3 = None
    root = ""
    rpc = "http://localhost:8545"
    config = None
    def __init__(self, **kwargs):
        if kwargs['root'] != None:
            self.root = kwargs['root']

        self.config = configparser.ConfigParser()
        self.config.read(self.root + '/config.ini')

        # set rpc from config
        try:
            self.rpc = self.config['ETH']['rpc_protocol'] + '://' + self.config['ETH']['rpc_host'] + ":" + self.config['ETH']['rpc_port']
        except:
            pass

        # override config from arg
        try:
            self.rpc = kwargs['rpc']
        except:
            pass
       
        # initialize web3 provider
        w3provider = Web3.HTTPProvider(self.rpc)
        self.w3 = Web3(w3provider)


