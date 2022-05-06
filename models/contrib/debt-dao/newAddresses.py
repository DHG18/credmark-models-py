from credmark.cmf.model import Model
from credmark.cmf.types.ledger import TransactionTable
from credmark.dto import DTO


class BlockNumberInput(DTO):
    start_block:int

@Model.describe(
    slug='contrib.debt-dao-new-addresses',
    display_name='New Addresses in the past interval',
    description="",
    version='1.0',
    developer='dhg.eth',
    input=BlockNumberInput,
    output=dict
)
class NewAddresses(Model):
    def run(self, input: BlockNumberInput):
        return self.context.ledger.get_transactions(columns=[TransactionTable.Columns.FROM_ADDRESS],
        where=f'{TransactionTable.Columns.NONCE}=0 and {TransactionTable.Columns.BLOCK_NUMBER} > {input.start_block}')
