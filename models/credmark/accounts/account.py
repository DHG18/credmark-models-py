from credmark.cmf.model import Model
from credmark.cmf.types import (
    Token,
    Account,
    Portfolio,
    NativeToken,
    NativePosition,
    TokenPosition
)
from credmark.cmf.types.ledger import TokenTransferTable


@Model.describe(
    slug="account.portfolio",
    version="1.0",
    display_name="Account Portfolio",
    description="All of the token holdings for an account",
    developer="Credmark",
    input=Account,
    output=Portfolio)
class WalletInfoModel(Model):
    def run(self, input: Account) -> Portfolio:
        token_addresses = self.context.ledger.get_erc20_transfers(
            columns=[TokenTransferTable.Columns.TOKEN_ADDRESS],
            where=' '.join(
                [f"{TokenTransferTable.Columns.FROM_ADDRESS}='{input.address}'",
                 "or",
                 f"{TokenTransferTable.Columns.TO_ADDRESS}='{input.address}'"]))

        print("token addresses: ", token_addresses)
        positions = []
        positions.append(
            NativePosition(
                amount=self.context.web3.eth.get_balance(input.address),
                asset=NativeToken()
            )
        )

        for t in list(dict.fromkeys([t['token_address'] for t in token_addresses])):
            try:
                token = Token(address=t)
                balance = float(token.functions.balanceOf(input.address).call())
                if balance > 0.0:
                    positions.append(
                        TokenPosition(asset=token, amount=balance))
            except Exception as _err:
                # TODO: currently skip NFTs
                pass

        return Portfolio(
            positions=positions
        )
