
import credmark.model


swap_abi = '[{"name":"TokenExchange","inputs":[{"type":"address","name":"buyer","indexed":true},{"type":"int128","name":"sold_id","indexed":false},{"type":"uint256","name":"tokens_sold","indexed":false},{"type":"int128","name":"bought_id","indexed":false},{"type":"uint256","name":"tokens_bought","indexed":false}],"anonymous":false,"type":"event"},{"name":"TokenExchangeUnderlying","inputs":[{"type":"address","name":"buyer","indexed":true},{"type":"int128","name":"sold_id","indexed":false},{"type":"uint256","name":"tokens_sold","indexed":false},{"type":"int128","name":"bought_id","indexed":false},{"type":"uint256","name":"tokens_bought","indexed":false}],"anonymous":false,"type":"event"},{"name":"AddLiquidity","inputs":[{"type":"address","name":"provider","indexed":true},{"type":"uint256[2]","name":"token_amounts","indexed":false},{"type":"uint256[2]","name":"fees","indexed":false},{"type":"uint256","name":"invariant","indexed":false},{"type":"uint256","name":"token_supply","indexed":false}],"anonymous":false,"type":"event"},{"name":"RemoveLiquidity","inputs":[{"type":"address","name":"provider","indexed":true},{"type":"uint256[2]","name":"token_amounts","indexed":false},{"type":"uint256[2]","name":"fees","indexed":false},{"type":"uint256","name":"token_supply","indexed":false}],"anonymous":false,"type":"event"},{"name":"RemoveLiquidityImbalance","inputs":[{"type":"address","name":"provider","indexed":true},{"type":"uint256[2]","name":"token_amounts","indexed":false},{"type":"uint256[2]","name":"fees","indexed":false},{"type":"uint256","name":"invariant","indexed":false},{"type":"uint256","name":"token_supply","indexed":false}],"anonymous":false,"type":"event"},{"name":"CommitNewAdmin","inputs":[{"type":"uint256","name":"deadline","indexed":true,"unit":"sec"},{"type":"address","name":"admin","indexed":true}],"anonymous":false,"type":"event"},{"name":"NewAdmin","inputs":[{"type":"address","name":"admin","indexed":true}],"anonymous":false,"type":"event"},{"name":"CommitNewParameters","inputs":[{"type":"uint256","name":"deadline","indexed":true,"unit":"sec"},{"type":"uint256","name":"A","indexed":false},{"type":"uint256","name":"fee","indexed":false},{"type":"uint256","name":"admin_fee","indexed":false}],"anonymous":false,"type":"event"},{"name":"NewParameters","inputs":[{"type":"uint256","name":"A","indexed":false},{"type":"uint256","name":"fee","indexed":false},{"type":"uint256","name":"admin_fee","indexed":false}],"anonymous":false,"type":"event"},{"outputs":[],"inputs":[{"type":"address[2]","name":"_coins"},{"type":"address[2]","name":"_underlying_coins"},{"type":"address","name":"_pool_token"},{"type":"uint256","name":"_A"},{"type":"uint256","name":"_fee"}],"constant":false,"payable":false,"type":"constructor"},{"name":"get_virtual_price","outputs":[{"type":"uint256","name":"out"}],"inputs":[],"constant":true,"payable":false,"type":"function","gas":1084167},{"name":"calc_token_amount","outputs":[{"type":"uint256","name":"out"}],"inputs":[{"type":"uint256[2]","name":"amounts"},{"type":"bool","name":"deposit"}],"constant":true,"payable":false,"type":"function","gas":4239939},{"name":"add_liquidity","outputs":[],"inputs":[{"type":"uint256[2]","name":"amounts"},{"type":"uint256","name":"min_mint_amount"}],"constant":false,"payable":false,"type":"function","gas":6479997},{"name":"get_dy","outputs":[{"type":"uint256","name":"out"}],"inputs":[{"type":"int128","name":"i"},{"type":"int128","name":"j"},{"type":"uint256","name":"dx"}],"constant":true,"payable":false,"type":"function","gas":2543681},{"name":"get_dx","outputs":[{"type":"uint256","name":"out"}],"inputs":[{"type":"int128","name":"i"},{"type":"int128","name":"j"},{"type":"uint256","name":"dy"}],"constant":true,"payable":false,"type":"function","gas":2543687},{"name":"get_dy_underlying","outputs":[{"type":"uint256","name":"out"}],"inputs":[{"type":"int128","name":"i"},{"type":"int128","name":"j"},{"type":"uint256","name":"dx"}],"constant":true,"payable":false,"type":"function","gas":2543506},{"name":"get_dx_underlying","outputs":[{"type":"uint256","name":"out"}],"inputs":[{"type":"int128","name":"i"},{"type":"int128","name":"j"},{"type":"uint256","name":"dy"}],"constant":true,"payable":false,"type":"function","gas":2543512},{"name":"exchange","outputs":[],"inputs":[{"type":"int128","name":"i"},{"type":"int128","name":"j"},{"type":"uint256","name":"dx"},{"type":"uint256","name":"min_dy"}],"constant":false,"payable":false,"type":"function","gas":5184573},{"name":"exchange_underlying","outputs":[],"inputs":[{"type":"int128","name":"i"},{"type":"int128","name":"j"},{"type":"uint256","name":"dx"},{"type":"uint256","name":"min_dy"}],"constant":false,"payable":false,"type":"function","gas":5200817},{"name":"remove_liquidity","outputs":[],"inputs":[{"type":"uint256","name":"_amount"},{"type":"uint256[2]","name":"min_amounts"}],"constant":false,"payable":false,"type":"function","gas":153898},{"name":"remove_liquidity_imbalance","outputs":[],"inputs":[{"type":"uint256[2]","name":"amounts"},{"type":"uint256","name":"max_burn_amount"}],"constant":false,"payable":false,"type":"function","gas":6479708},{"name":"commit_new_parameters","outputs":[],"inputs":[{"type":"uint256","name":"amplification"},{"type":"uint256","name":"new_fee"},{"type":"uint256","name":"new_admin_fee"}],"constant":false,"payable":false,"type":"function","gas":146105},{"name":"apply_new_parameters","outputs":[],"inputs":[],"constant":false,"payable":false,"type":"function","gas":133512},{"name":"revert_new_parameters","outputs":[],"inputs":[],"constant":false,"payable":false,"type":"function","gas":21835},{"name":"commit_transfer_ownership","outputs":[],"inputs":[{"type":"address","name":"_owner"}],"constant":false,"payable":false,"type":"function","gas":74512},{"name":"apply_transfer_ownership","outputs":[],"inputs":[],"constant":false,"payable":false,"type":"function","gas":60568},{"name":"revert_transfer_ownership","outputs":[],"inputs":[],"constant":false,"payable":false,"type":"function","gas":21925},{"name":"withdraw_admin_fees","outputs":[],"inputs":[],"constant":false,"payable":false,"type":"function","gas":12831},{"name":"kill_me","outputs":[],"inputs":[],"constant":false,"payable":false,"type":"function","gas":37878},{"name":"unkill_me","outputs":[],"inputs":[],"constant":false,"payable":false,"type":"function","gas":22015},{"name":"coins","outputs":[{"type":"address","name":"out"}],"inputs":[{"type":"int128","name":"arg0"}],"constant":true,"payable":false,"type":"function","gas":2190},{"name":"underlying_coins","outputs":[{"type":"address","name":"out"}],"inputs":[{"type":"int128","name":"arg0"}],"constant":true,"payable":false,"type":"function","gas":2220},{"name":"balances","outputs":[{"type":"uint256","name":"out"}],"inputs":[{"type":"int128","name":"arg0"}],"constant":true,"payable":false,"type":"function","gas":2250},{"name":"A","outputs":[{"type":"uint256","name":"out"}],"inputs":[],"constant":true,"payable":false,"type":"function","gas":2081},{"name":"fee","outputs":[{"type":"uint256","name":"out"}],"inputs":[],"constant":true,"payable":false,"type":"function","gas":2111},{"name":"admin_fee","outputs":[{"type":"uint256","name":"out"}],"inputs":[],"constant":true,"payable":false,"type":"function","gas":2141},{"name":"owner","outputs":[{"type":"address","name":"out"}],"inputs":[],"constant":true,"payable":false,"type":"function","gas":2171},{"name":"admin_actions_deadline","outputs":[{"type":"uint256","unit":"sec","name":"out"}],"inputs":[],"constant":true,"payable":false,"type":"function","gas":2201},{"name":"transfer_ownership_deadline","outputs":[{"type":"uint256","unit":"sec","name":"out"}],"inputs":[],"constant":true,"payable":false,"type":"function","gas":2231},{"name":"future_A","outputs":[{"type":"uint256","name":"out"}],"inputs":[],"constant":true,"payable":false,"type":"function","gas":2261},{"name":"future_fee","outputs":[{"type":"uint256","name":"out"}],"inputs":[],"constant":true,"payable":false,"type":"function","gas":2291},{"name":"future_admin_fee","outputs":[{"type":"uint256","name":"out"}],"inputs":[],"constant":true,"payable":false,"type":"function","gas":2321},{"name":"future_owner","outputs":[{"type":"address","name":"out"}],"inputs":[],"constant":true,"payable":false,"type":"function","gas":2351}]'
erc_20_abi = '[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"           }        ],        "payable": false,        "stateMutability": "view",        "type": "function"    },    {        "constant": true,        "inputs": [],        "name": "symbol",        "outputs": [            {                "name": "",                "type": "string"            }        ],        "payable": false,        "stateMutability": "view",        "type": "function"    },    {        "constant": false,        "inputs": [            {                "name": "_to",                "type": "address"            },            {                "name": "_value",                "type": "uint256"            }        ],        "name": "transfer",        "outputs": [            {                "name": "",                "type": "bool"            }        ],        "payable": false,        "stateMutability": "nonpayable",        "type": "function"    },    {        "constant": true,        "inputs": [            {                "name": "_owner",                "type": "address"            },            {                "name": "_spender",                "type": "address"            }        ],        "name": "allowance",        "outputs": [            {                "name": "",                "type": "uint256"            }        ],        "payable": false,        "stateMutability": "view",        "type": "function"    },    {        "payable": true,        "stateMutability": "payable",        "type": "fallback"    },    {        "anonymous": false,        "inputs": [            {                "indexed": true,                "name": "owner",                "type": "address"            },            {                "indexed": true,                "name": "spender",                "type": "address"            },            {                "indexed": false,                "name": "value",                "type": "uint256"            }        ],        "name": "Approval",        "type": "event"    },    {        "anonymous": false,        "inputs": [            {                "indexed": true,                "name": "from",                "type": "address"            },            {                "indexed": true,                "name": "to",                "type": "address"            },            {                "indexed": false,                "name": "value",                "type": "uint256"            }        ],        "name": "Transfer",        "type": "event"    }]'

swap_addresses = [
    "0x79a8c46dea5ada233abaffd40f3a0a2b1e5a4f27",
    "0xa2b47e3d5c44877cca798226b7b8118f9bfb7a56",
    "0x06364f10b501e868329afbc005b3492902d6c763",
    "0x93054188d876f558f4a66b2ef1d97d16edf0895b",
    "0x7fc77b5c7614e1533320ea6ddc2eb61fa00a9714",
    "0xa5407eae9ba41422680e2e00537571bcc53efbfd",
    "0x45f783cce6b7ff23b2ab2d70e416cdb7d6055f51",
]
lp_token_addresses = [
    "0xD905e2eaeBe188fc92179b6350807D8bd91Db0D8",
    "0xC25a3A3b969415c80451098fa907EC722572917F",
    "0x3b3ac5386837dc563660fb6a0937dfaa5924333b",
    "0x845838df265dcd2c412a1dc9e959c7d08537f8a2",
    "0xdf5e0e81dff6faf3a7e52ba697820c5e32d806a8",
    "0x9fC689CCaDa600B6DF723D9E47D84d76664a1F23",
    "0x075b1bb99792c9E1041bA13afEf80C91a1e70fB3",
    "0x49849C98ae39Fff122806C06791Fa73784FB3675",
    "0x1AEf73d49Dedc4b1778d0706583995958Dc862e6",
    "0x6D65b498cb23deAba52db31c93Da9BFFb340FB8F",
    "0x4f3E8F405CF5aFC05D68142F3783bDfE13811522",
    "0x97E2768e8E73511cA874545DC5Ff8067eB19B787",
    "0x5B5CFE992AdAC0C9D48E05854B2d91C73a003858",
    "0x6c3F90f043a72FA612cbac8115EE7e52BDe6E490"
]

crv_token = [
    "0xd533a949740bb3306d119cc777fa900ba034cd52"
]


@credmark.model.it(slug="curve-fi-pool-info",
                   version="1.0",
                   display_name="Curve Finance Pool Liqudity",
                   description="The amount of Liquidity for Each Token in a Curve Pool")
class CurveFinancePoolInfo(credmark.model.Model):

    def run(self, input) -> dict:
        pool_address = input['poolAddress']
        pool_contract = self.context.web3.eth.contract(
            address=self.context.web3.toChecksumAddress(pool_address),
            abi=swap_abi
        )
        tokens = []
        for i in range(0, 100):
            try:
                tok = pool_contract.functions.coins(i).call()
                tokens.append(tok)
            except:
                break

        balances = []
        for i in range(0, 100):
            try:
                bal = pool_contract.functions.balances(i).call()
                balances.append(bal)
            except:
                break
        virtual_price = pool_contract.functions.get_virtual_price().call()
        a = pool_contract.functions.A().call()

        return {
            "virtualPrice": virtual_price,
            "tokens": tokens,
            "balances": balances,
            "A": a
        }


@credmark.model.it(slug="curve-fi-pool-yield",
                   version="1.0",
                   display_name="Curve Finance Pool Liqudity",
                   description="The amount of Liquidity for Each Token in a Curve Pool")
class CurveFinancePoolYield(credmark.model.Model):

    def run(self, input) -> dict:
        return super().run(input)


@credmark.model.it(slug="curve-fi-all-pool-info",
                   version="1.0",
                   display_name="Curve Finance Pool Liqudity",
                   description="The amount of Liquidity for Each Token in a Curve Pool")
class CurveFinanceTotalTokenLiqudity(credmark.model.Model):

    def run(self, input) -> dict:
        pool_infos = []
        for pool in swap_addresses:
            pool_info = self.context.run_model("curve-fi-pool-info", {"poolAddress": pool})
            pool_infos.append(pool_info)
        return {"pools": pool_infos}