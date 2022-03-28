from abc import abstractmethod
from datetime import (
    date,
    datetime,
    timezone,
)

from typing import (
    Callable,
    List,
    Any,
    Generator,
    Tuple,
)

import itertools

import pandas as pd

from credmark.dto import (
    DTO,
    DTOField,
)

from credmark.types import (
    Portfolio,
    Token,
)

from credmark.model import (
    ModelRunError,
)

import os
import pickle


class MarketTarget(DTO):
    key: str  # ensure unique in market oject
    artifact: Any


class Recipe(DTO):
    key: str  # ensure unique in global cache
    target_key: str  # key for MarketTarget
    method: str
    input: dict
    post_proc: Callable = DTOField(default=lambda x: x)


class Cook:
    def __init__(self, context, reset_cache=False, use_cache=True):
        self._cache_file = os.path.join('tmp', 'chain.cache.pkl')
        self._cache = {}
        self._cache_hit = 0
        self._total_hit = 0
        self._cache_saved = True
        self._context = context
        self._use_cache = use_cache

        if self._use_cache:
            if reset_cache:
                self.save_cache()
            else:
                self.load_cache()

    def __del__(self):
        if self._use_cache:
            self.print_cache()
            if not self._cache_saved:
                self.save_cache()

    def load_cache(self):
        self._cache = {}
        try:
            if os.path.isfile(self._cache_file):
                with open(self._cache_file, 'rb') as handle:
                    self._cache = pickle.load(handle)
        except EOFError:
            self.save_cache()

    def save_cache(self):
        cache_dir = os.path.dirname(self._cache_file)
        if not os.path.isdir(cache_dir):
            os.mkdir(cache_dir)
        with open(self._cache_file, 'wb') as handle:
            pickle.dump(self._cache, handle, protocol=pickle.HIGHEST_PROTOCOL)

    @property
    def context(self):
        return self._context

    @property
    def cache_hit(self):
        return self._cache_hit

    @property
    def total_hit(self):
        return self._total_hit

    def print_cache(self):
        self._context.logger.info(
            f'Local cache hit {self.cache_hit} for {self.total_hit} requests '
            f'rate={self.cache_hit/self.total_hit*100:.1f}%')

    def cook(self, rec: Recipe):
        result = None
        if self._use_cache and rec.key in self._cache:
            result = self._cache[rec.key]
            self._cache_hit += 1
            self._total_hit += 1
        else:
            if rec.method == 'run_model':
                result = self._context.run_model(**rec.input)
            elif rec.method == 'run_model_historical':
                result = self._context.historical.run_model_historical(
                    **rec.input)  # model_return_type=BlockSeries[dict]
            else:
                raise ModelRunError(f'Unknown {rec.method=}')
            result = rec.post_proc(result)
            self._cache[rec.key] = result
            self._cache_saved = False
            self._total_hit += 1

        return result


def validate_as_of(as_of):
    return isinstance(as_of, datetime) and as_of.tzinfo is not None


class Plan:
    def __init__(self, tag, target: MarketTarget,  **data):
        self._tag = tag
        self._target = target
        self._data = data

    @abstractmethod
    def execute(self, cook):
        pass


class HistoricalBlockPlan(Plan):
    def post_proc_block_series(self, blocks):
        blocks = blocks.dict()
        df_blocks = (pd.DataFrame(blocks['series'])
                     .drop(columns=['output'])
                     .sort_values(['blockNumber'], ascending=False))

        df_blocks.loc[:, 'blockTime'] = df_blocks.blockTimestamp.apply(
            lambda x: datetime.fromtimestamp(x, timezone.utc))
        df_blocks.loc[:, 'sampleTime'] = df_blocks.sampleTimestamp.apply(
            lambda x: datetime.fromtimestamp(x, timezone.utc))

        block_numbers = df_blocks.blockNumber.to_list()
        return {'block_numbers': block_numbers,
                'block_table': df_blocks}

    def execute(self, cook):
        method = 'run_model_historical'
        slug = 'finance.get-one'
        as_of = self._data['as_of']
        window = self._data['window']
        interval = self._data['interval']

        if validate_as_of(as_of):
            as_of_timestamp = as_of.timestamp()
        elif isinstance(as_of, date) and self._tag == 'eod':
            dt_from_date = datetime.combine(as_of, datetime.max.time(), tzinfo=timezone.utc)
            as_of_timestamp = int(dt_from_date.timestamp())
        else:
            raise ModelRunError(f'Unsupported {as_of=}')

        _as_of_block = cook.context.block_number.from_timestamp(as_of_timestamp)

        recipe = Recipe(key=f'{method}.{slug}.{window}.{interval}.{as_of_timestamp}',
                        target_key=self._target.key,
                        method='run_model_historical',
                        input={'model_slug': slug, 'window': window,
                               'interval': interval, 'end_timestamp': as_of_timestamp},
                        post_proc=self.post_proc_block_series
                        )
        result = cook.cook(recipe)
        return result


class EODPlan(Plan):
    def execute(self, cook):
        if self._tag == 'eod':
            as_of = self._data['as_of']
            window = '1 day'
            interval = '1 day'
        elif self._tag == 'eod_var_scenario':
            window = self._data['window']
            as_of = self._data['as_of']
            interval = self._data['interval']
        else:
            raise ModelRunError(f'Unknown {self._tag=}')

        target = MarketTarget(key='HistoricalBlock', artifact=None)
        pre_plan = HistoricalBlockPlan(self._tag,
                                       target,
                                       as_of=as_of,
                                       window=window,
                                       interval=interval)

        pre_plan_results = pre_plan.execute(cook)

        block_numbers = pre_plan_results['block_numbers']
        block_table = pre_plan_results['block_table']

        dish = block_table.copy()
        for block_number in block_numbers:
            if isinstance(self._target.artifact, Token):
                method = 'run_model'
            else:
                raise ModelRunError(f'Unsupported artifact {self._target.artifact=}')

            rec = Recipe(key=f'{self._target.key}.{method}.{block_number}',
                         target_key=self._target.key,
                         method=method,
                         # other choices:
                         # - 'token.price-ext',
                         # - 'uniswap-v3.get-average-price',
                         # - 'token.price',
                         input={'slug': 'token.price-ext',
                                'input': self._target.artifact,
                                'block_number': block_number},
                         )

            rec_result = cook.cook(rec)
            for k, v in rec_result.items():
                dish.loc[dish.blockNumber == rec.input['block_number'],
                         f'{rec.target_key}.{k}'] = v

        if self._tag == 'eod':
            return {'raw': dish,
                    'extracted': dish[f'{self._target.key}.price'][0]}
        elif self._tag == 'eod_var_scenario':
            price_series = dish[f'{self._target.key}.price']
            rolling_interval = self._data['rolling_interval']
            if rolling_interval is not None:
                val_leading = price_series[:-rolling_interval].to_numpy()
                val_lagging = price_series[rolling_interval:].to_numpy()
                ret_series = val_leading / val_lagging
            else:
                raise ModelRunError('rolling_interval undefined for VaR scenario generation.')
            return {'raw': dish,
                    'extracted': ret_series}
        raise ModelRunError(f'Unknown {self._tag=}')


class Tradeable:
    def __init__(self, tid, traces):
        """
        traces is a table stores all properties of the trade in time sequence.
        """
        self.__tid = tid
        self.__traces = traces

    @property
    def tid(self):
        return self.__tid

    @property
    def traces(self):
        return self.__traces

    @abstractmethod
    def requires(self) -> Generator[MarketTarget, None, None]:
        pass

    @abstractmethod
    def value(self, new_as_of, mkt, mkt_adj=lambda x: x) -> float:
        pass

    @abstractmethod
    def value_scenarios(self, new_as_of, mkt, mkt_scenarios) -> pd.Series:
        pass


class TokenTradeable(Tradeable):
    def __init__(self, tid, traces, as_of, token, amount, init_price):
        super().__init__(tid, traces)
        assert validate_as_of(as_of)
        self._as_of = as_of
        self._token = token
        self._amount = amount
        self._init_price = init_price
        self._key = f'Token.{self._token.address}'

    @property
    def key(self):
        return self._key

    def requires(self) -> Generator[MarketTarget, None, None]:
        mkt_target = MarketTarget(key=self.key,
                                  artifact=self._token)
        yield mkt_target

    def value(self, new_as_of, mkt, mkt_adj=lambda x: x) -> float:
        """
        TokenTrade's value does not change with the new_as_of to the Tradeable's own as_of
        Other type of trade could have time value.
        """

        # DEPRECATED code of retriving price
        # idx_last = mkt_piece.index.get_loc(
        #   mkt_piece.index[mkt_piece['blockTime'] <= new_as_of][0])
        # curent_price = mkt_piece[f'{self.key}.price'].iloc[idx_last]

        curent_price = mkt_adj(mkt[self.key]['extracted'])
        pnl = curent_price - self._init_price
        pnl *= self._amount
        return pnl

    def value_scenarios(self, new_as_of, mkt, mkt_scenarios) -> pd.Series:
        base_pnl = self.value(new_as_of, mkt)
        scen_pnl = []
        scenarios = mkt_scenarios[self.key]['extracted']
        for scen in scenarios:
            new_pnl = self.value(new_as_of, mkt, lambda x, scen=scen: x * scen)
            scen_pnl.append(new_pnl)
        return pd.Series(scen_pnl) - base_pnl


class ContractTradeable(Tradeable):
    def __init__(self, as_of, tid):
        super().__init__(as_of, tid)

    def requires(self) -> Generator[MarketTarget, None, None]:
        yield from []

    def value(self, new_as_of, mkt, mkt_adj=lambda x: x) -> float:
        return 0

    def value_scenarios(self, new_as_of, mkt, mkt_scenarios) -> pd.Series:
        return pd.Series([0 for _ in mkt_scenarios])


# PortfolioManage shall request to Market to build the market information


class Market(dict):
    pass

# TODO: to be merged with framework's Portfolio


class PortfolioManager:
    def __init__(self, trades: List[Tradeable], as_of, context):
        self._trades = trades
        self._as_of = as_of
        self._cook = Cook(context)

    @classmethod
    def from_portfolio(cls, as_of, portfolio: Portfolio, context):
        trades = []
        for (pos_n, pos) in enumerate(portfolio.positions):
            if not pos.asset.address:
                raise ModelRunError(f'Input position is invalid, {input}')

            tid = f'{pos_n}.{pos.asset.address}'
            t = TokenTradeable(tid, [], as_of, pos.asset, pos.amount, init_price=0)
            trades.append(t)
        return cls(trades, as_of, context)

    def requires(self) -> Generator[Tuple[str, MarketTarget], None, None]:
        key_set = set()
        for t in self._trades:
            for req in t.requires():
                if req.key not in key_set:
                    key_set.add(req.key)
                    yield req.key, req

    def prepare_market(self, tag, **data):
        mkt_target = dict(self.requires())
        mkt = Market({key: EODPlan(tag, target, **data).execute(self._cook)
                      for key, target in mkt_target.items()})
        return mkt

    def value(self, mkt: Market, as_df=True, **data):
        values = []
        new_as_of = data.get('as_of', self._as_of)

        for t in self._trades:
            v = t.value(new_as_of, mkt)
            values.append((t.tid, v))
        df_res = pd.DataFrame(values, columns=['TRADE_ID', 'VALUE'])
        if as_df:
            return df_res
        return df_res.loc[:, ['TRADE_ID', 'VALUE']].to_dict()

    def value_scenarios(self, mkt: Market, mkt_scenarios: Market, as_df=True, **data):
        values = []
        new_as_of = data.get('as_of', self._as_of)

        for t in self._trades:
            v = t.value_scenarios(new_as_of, mkt, mkt_scenarios)
            values.extend(zip(itertools.count(1), itertools.repeat(t.tid), v))
        df_res = (pd.DataFrame(values, columns=['SCEN_ID', 'TRADE_ID', 'VALUE'])
                  .sort_values(['SCEN_ID', 'TRADE_ID'])
                  .reset_index(drop=True))
        if as_df:
            return df_res
        return df_res.to_dict(orient='index')