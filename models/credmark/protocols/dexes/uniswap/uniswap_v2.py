import credmark.model
from credmark.types import (
    Address,
    Contract,
    Token,
)
from credmark.types.dto import (
    DTO
)

from models.tmp_abi_lookup import (
    SUSHISWAP_FACTORY_ABI,
    SUSHISWAP_PAIRS_ABI,
    ERC_20_TOKEN_CONTRACT_ABI,
)

@credmark.model.describe(slug="uniswap-v2-all-pools",
                         version="1.0",
                         display_name="UniswapV2 all pairs",
                         description="Returns the addresses of all pairs on Uniswap v2 protocol")
class UniswapV2AllPairs(credmark.model.Model):
    def run(self, input) -> dict:
        contract = self.context.web3.eth.contract(
            address="0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f",
            abi=SUSHISWAP_FACTORY_ABI
        )
        allPairsLength = contract.functions.allPairsLength().call()
        
        UNISWAP_PAIRS_ADDRESSES = []
        
        error_count = 0
        for i in range(allPairsLength):
            try:
                pair_address = contract.functions.allPairs(i).call()
                UNISWAP_PAIRS_ADDRESSES.append(Address(pair_address))
            except Exception as err:
                error_count += 1
        return {"result": UNISWAP_PAIRS_ADDRESSES}


class UniswapV2Pool(DTO):
    token0: Token
    token1: Token


@credmark.model.describe(slug="uniswap-v2-get-pool",
                         version="1.0",
                         display_name="UniswapV2 get pool for a pair of tokens",
                         description="Returns the addresses of the pool of both tokens on Suhsiswap protocol",
                         input=UniswapV2Pool)
class UniswapV2GetPair(credmark.model.Model):
    def run(self, input: UniswapV2Pool):
        output = {}
        print('DEBUG', input)
        contract = self.context.web3.eth.contract(
            address="0xC0AEe478e3658e2610c5F7A4A2E1777cE9e4f2Ac",
            abi=SUSHISWAP_FACTORY_ABI
        )
        token0 = self.context.web3.toChecksumAddress(input['token0'])
        token1 = self.context.web3.toChecksumAddress(input['token1'])
        pool = contract.functions.getPair(token0, token1).call()
        print(pool)
        return output


@credmark.model.describe(slug="uniswap-v2-get-pool-info",
                         version="1.0",
                         display_name="UniswapV2 get details for a pool",
                         description="Returns the token details of the pool",
                         input=Contract)
class UniswapV2GetPairDetails(credmark.model.Model):
    def try_or(self, func, default=None, expected_exc=(Exception,)):
        try:
            return func()
        except expected_exc:
            return default
    def run(self, input: Contract):
        output = {}
        print('DEBUG', input)
        contract = self.context.web3.eth.contract(
            address=input.address,
            abi=SUSHISWAP_PAIRS_ABI
        )
        token0 = contract.functions.token0().call()
        token1 = contract.functions.token1().call()
        getReserves = contract.functions.getReserves().call()
        token0_instance = self.context.web3.eth.contract(
            address=token0, abi=ERC_20_TOKEN_CONTRACT_ABI)
        _token0_name = self.try_or(lambda: token0_instance.functions.name().call())
        _token0_symbol = self.try_or(lambda: token0_instance.functions.symbol().call())
        _token0_decimals = token0_instance.functions.decimals().call()
        token1_instance = self.context.web3.eth.contract(
            address=token1, abi=ERC_20_TOKEN_CONTRACT_ABI)
        _token1_name = self.try_or(lambda: token1_instance.functions.name().call())
        _token1_symbol = self.try_or(lambda: token1_instance.functions.symbol().call())
        _token1_decimals = token1_instance.functions.decimals().call()
        token0_reserve = getReserves[0]/pow(10, _token0_decimals)
        token1_reserve = getReserves[1]/pow(10, _token1_decimals)
        output = {'pairAddress': input.address, 'token0': token0, 'token0_name': _token0_name, 'token0_symbol': _token0_symbol,
                  'token0_reserve': token0_reserve, 'token1': token1, 'token1_name': _token1_name, 'token1_symbol': _token1_symbol, 'token1_reserve': token1_reserve}
        print(output)