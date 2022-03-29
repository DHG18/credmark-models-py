from typing import (
    Union,
    Optional,
)

import credmark.model
from credmark.dto import (
    DTO,
)
from credmark.types import (
    Price,
    Token,
    Address,
    Contract,
    Contracts
)
from models.dtos.volume import TradingVolume, TokenTradingVolume
from models.tmp_abi_lookup import UNISWAP_V2_SWAP_ABI
UNISWAP_V2_FACTORY_ADDRESS = "0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f"


@credmark.model.describe(slug='uniswap-v2.get-pools',
                         version='1.0',
                         display_name='Uniswap v2 Token Pools',
                         description='The Uniswap v2 pools that support a token contract',
                         input=Token,
                         output=Contracts)
class UniswapV2GetPoolsForToken(credmark.model.Model):

    def run(self, input: Token) -> Contracts:

        factory = Contract(address=UNISWAP_V2_FACTORY_ADDRESS)
        tokens = [Token(symbol="USDC"),
                  Token(symbol="WETH"),
                  Token(symbol="DAI")]
        contracts = []
        for token in tokens:
            pair_address = factory.functions.getPair(input.address, token.address).call()
            if not pair_address == Address.null():
                contracts.append(Contract(address=pair_address, abi=UNISWAP_V2_SWAP_ABI).info)
        return Contracts(contracts=contracts)


@credmark.model.describe(slug='uniswap-v2.get-average-price',
                         version='1.0',
                         display_name='Uniswap v2 Token Price',
                         description='The Uniswap v2 price, averaged by liquidity',
                         input=Token,
                         output=Price)
class UniswapV2GetAveragePrice(credmark.model.Model):
    def run(self, input: Token) -> Price:
        pools = self.context.run_model('uniswap-v2.get-pools',
                                       input,
                                       return_type=Contracts)

        prices = []
        reserves = []
        weth_price = None
        for pool in pools:
            reserves = pool.functions.getReserves().call()
            if input.address == pool.functions.token0().call():
                token1 = Token(address=pool.functions.token1().call())
                reserve = reserves[0]
                price = token1.scaled(reserves[1]) / input.scaled(reserves[0])

                if token1.symbol == 'WETH':
                    if weth_price is None:
                        weth_price = self.context.run_model('uniswap-v2.get-average-price',
                                                            token1,
                                                            return_type=Price).price
                    price = price * weth_price
            else:
                token0 = Token(address=pool.functions.token0().call())
                reserve = reserves[1]
                price = token0.scaled(reserves[0]) / input.scaled(reserves[1])
                if token0.symbol == 'WETH':
                    if weth_price is None:
                        weth_price = self.context.run_model('uniswap-v2.get-average-price',
                                                            token0,
                                                            return_type=Price).price
                    price = price * weth_price
            prices.append((price, reserve))
        if len(prices) == 0:
            return Price(price=None)
        return Price(price=sum([p * r for (p, r) in prices]) / sum([r for (p, r) in prices]))


@credmark.model.describe(slug='uniswap-v2.pool-volume',
                         version='1.0',
                         display_name='Uniswap v2 Pool Swap Volumes',
                         description='The volume of each token swapped in a pool in a window',
                         input=Contract,
                         output=TradingVolume)
class UniswapV2PoolSwapVolume(credmark.model.Model):
    def run(self, input: Contract) -> TradingVolume:
        input = Contract(address=input.address, abi=UNISWAP_V2_SWAP_ABI)
        swaps = input.events.Swap.createFilter(
            fromBlock=self.context.block_number - int(86400 / 14),
            toBlock=self.context.block_number).get_all_entries()
        token0 = Token(address=input.functions.token0().call())
        token1 = Token(address=input.functions.token1().call())
        return TradingVolume(
            tokenVolumes=[
                TokenTradingVolume(
                    token=token0,
                    sellAmount=sum([s['args']['amount0In'] for s in swaps]),
                    buyAmount=sum([s['args']['amount0Out'] for s in swaps])),
                TokenTradingVolume(
                    token=token1,
                    sellAmount=sum([s['args']['amount1In'] for s in swaps]),
                    buyAmount=sum([s['args']['amount1Out'] for s in swaps]))
            ])
