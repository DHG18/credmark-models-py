
import credmark.model
from credmark.types import Token, Address
from credmark.types.dto import DTO

from typing import (
    Dict,
    Union
)


class ExampleTokenLoadingOutput(DTO):
    loadedFromAddress: Token
    loadedFromSymbol: Token
    loadedNativeToken: Token
    loadedFromSymbolPrice: float
    loadedFromSymbolTotalSupply: float
    loadedFromSymbolBalanceOf: float
    loadedFromSymbolBalanceOfWei: int


@credmark.model.describe(slug='example.token-loading',
                         version='1.0',
                         input=None,
                         developer='credmark',
                         output=ExampleTokenLoadingOutput)
class ExampleTokenLoading(credmark.model.Model):
    def run(self, input) -> ExampleTokenLoadingOutput:
        cmk = Token(symbol='CMK')
        cmk_holder = Address("0xF6dBFf8433b643bc08cB53BeD6C535c8a57AC912")
        return ExampleTokenLoadingOutput(
            loadedFromAddress=Token(address='0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9'),
            loadedFromSymbol=cmk,
            loadedNativeToken=Token.native_token(),
            loadedFromSymbolPrice=cmk.price_usd,
            loadedFromSymbolTotalSupply=cmk.total_supply().scaled,
            loadedFromSymbolBalanceOf=cmk.balance_of(cmk_holder).scaled,
            loadedFromSymbolBalanceOfWei=cmk.balance_of(cmk_holder)
        )
