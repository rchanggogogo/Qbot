# coding:utf8
import re
from datetime import datetime
from typing import Optional

import basequotation


class Tencent(basequotation.BaseQuotation):
    """腾讯免费行情获取"""

    grep_stock_code = re.compile(r"(?<=_)\w+")
    max_num = 60

    @property
    def stock_api(self) -> str:
        """
        获取股票当天的详细信息
        """
        return "http://qt.gtimg.cn/q="

    def format_response_data(self, rep_data, prefix=False):
        stocks_detail = "".join(rep_data)
        stock_details = stocks_detail.split(";")
        stock_dict = dict()
        for stock_detail in stock_details:
            stock = stock_detail.split("~")
            if len(stock) <= 49:
                continue
            stock_code = (
                self.grep_stock_code.search(stock[0]).group()
                if prefix
                else stock[2]
            )
            stock_dict[stock_code] = {
                "name": stock[1],
                "code": stock_code,
                "now": float(stock[3]),
                "close": float(stock[4]),
                "open": float(stock[5]),
                "volume": float(stock[6]) * 100,
                "bid_volume": int(stock[7]) * 100,
                "ask_volume": float(stock[8]) * 100,
                "bid1": float(stock[9]),
                "bid1_volume": int(stock[10]) * 100,
                "bid2": float(stock[11]),
                "bid2_volume": int(stock[12]) * 100,
                "bid3": float(stock[13]),
                "bid3_volume": int(stock[14]) * 100,
                "bid4": float(stock[15]),
                "bid4_volume": int(stock[16]) * 100,
                "bid5": float(stock[17]),
                "bid5_volume": int(stock[18]) * 100,
                "ask1": float(stock[19]),
                "ask1_volume": int(stock[20]) * 100,
                "ask2": float(stock[21]),
                "ask2_volume": int(stock[22]) * 100,
                "ask3": float(stock[23]),
                "ask3_volume": int(stock[24]) * 100,
                "ask4": float(stock[25]),
                "ask4_volume": int(stock[26]) * 100,
                "ask5": float(stock[27]),
                "ask5_volume": int(stock[28]) * 100,
                "最近逐笔成交": stock[29],
                "datetime": datetime.strptime(stock[30], "%Y%m%d%H%M%S"),
                "涨跌": float(stock[31]),
                "涨跌(%)": float(stock[32]),
                "high": float(stock[33]),
                "low": float(stock[34]),
                "价格/成交量(手)/成交额": stock[35],
                "成交量(手)": int(stock[36]) * 100,
                "成交额(万)": float(stock[37]) * 10000,
                "turnover": self._safe_float(stock[38]),
                "PE": self._safe_float(stock[39]),
                "unknown": stock[40],
                "high_2": float(stock[41]),  # 意义不明
                "low_2": float(stock[42]),  # 意义不明
                "振幅": float(stock[43]),
                "流通市值": self._safe_float(stock[44]),
                "总市值": self._safe_float(stock[45]),
                "PB": float(stock[46]),
                "涨停价": float(stock[47]),
                "跌停价": float(stock[48]),
                "量比": self._safe_float(stock[49]),
                "委差": self._safe_acquire_float(stock, 50),
                "均价": self._safe_acquire_float(stock, 51),
                "市盈(动)": self._safe_acquire_float(stock, 52),
                "市盈(静)": self._safe_acquire_float(stock, 53),
            }
        return stock_dict

    def _safe_acquire_float(self, stock: list, idx: int) -> Optional[float]:
        """
        There are some securities that only have 50 fields. See example below:
        ['\nv_sh518801="1',
        '国泰申赎',
        '518801',
        '2.229',
        ......
         '', '0.000', '2.452', '2.006', '"']
        """
        try:
            return self._safe_float(stock[idx])
        except IndexError:
            return None

    def _safe_float(self, s: str) -> Optional[float]:
        try:
            return float(s)
        except ValueError:
            return None

if __name__ == "__main__":
    quotation = Tencent()
    print(quotation.get_stock_data(["sz000001"]))

    # {'000001': {'name': '平安银行', 'code': '000001', 'now': 10.43, 'close': 10.46, 'open': 10.42, 'volume': 90636100.0, 'bid_volume': 38137300, 'ask_volume': 52498800.0, 'bid1': 10.43, 'bid1_volume': 654400, 'bid2': 10.42, 'bid2_volume': 1173100, 'bid3': 10.41, 'bid3_volume': 990700, 'bid4': 10.4, 'bid4_volume': 1567500, 'bid5': 10.39, 'bid5_volume': 1335900, 'ask1': 10.44, 'ask1_volume': 654100, 'ask2': 10.45, 'ask2_volume': 550500, 'ask3': 10.46, 'ask3_volume': 632400, 'ask4': 10.47, 'ask4_volume': 512200, 'ask5': 10.48, 'ask5_volume': 816100, '最近逐笔成交': '', 'datetime': datetime.datetime(2024, 4, 8, 16, 15), '涨跌': -0.03, '涨跌(%)': -0.29, 'high': 10.49, 'low': 10.37, '价格/成交量(手)/成交额': '10.43/906361/945290441', '成交量(手)': 90636100, '成交额(万)': 945290000.0, 'turnover': 0.47, 'PE': 4.36, 'unknown': '', 'high_2': 10.49, 'low_2': 10.37, '振幅': 1.15, '流通市值': 2024.0, '总市值': 2024.04, 'PB': 0.5, '涨停价': 11.51, '跌停价': 9.41, '量比': 0.83, '委差': 25563.0, '均价': 10.43, '市盈(动)': 4.36, '市盈(静)': 4.36}}