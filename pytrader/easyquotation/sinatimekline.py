# coding:utf8
"""
# pylint: disable=line-too-long
url = "https://quotes.sina.cn/cn/api/jsonp_v2.php/var%20_sh688017_5_1632742847429=/CN_MarketDataService.getKLineData?symbol=sh688017&scale=5&ma=no&datalen=1023"
"""

import json

import basequotation, helpers


class SinaTimeKline(basequotation.BaseQuotation):
    """新浪5分钟行情获取"""

    max_num = 1

    @property
    def stock_api(self) -> str:
        return "https://quotes.sina.cn/cn/api/jsonp_v2.php/jsonp/CN_MarketDataService.getKLineData?symbol="

    def _gen_stock_prefix(self, stock_codes):
        return [
            helpers.get_stock_type(code) + code[-6:] + "&scale=5&ma=no&datalen=1023"
            for code in stock_codes
        ]

    def _fetch_stock_data(self, stock_list):
        """因为 timekline 的返回没有带对应的股票代码，所以要手动带上"""
        stock_list_ = self._gen_stock_prefix(stock_codes=stock_list)
        res = super()._fetch_stock_data(stock_list_)

        with_stock = []
        for stock, resp in zip(stock_list, res):
            if resp is not None:
                with_stock.append((stock, resp))
        return with_stock

    def format_response_data(self, rep_data, **kwargs):
        stock_dict = dict()
        for stock_code, stock_detail in rep_data:
            stock_detail = stock_detail.split("\n")[1]
            # pylint: disable=line-too-long
            data = stock_detail[stock_detail.index("["):-2]
            stock_dict[stock_code] = json.loads(data)
        return stock_dict

if __name__ == "__main__":
    timeline = SinaTimeKline()
    print(timeline.get_stock_data(["sz000001"]))