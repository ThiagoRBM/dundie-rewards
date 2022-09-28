from decimal import Decimal
from typing import Dict, List

import httpx
from pydantic import BaseModel, Field

from dundie.settings import API_BASE_URL


class USDRate(BaseModel):
    code: str = Field(default="USD")
    codein: str = Field(default="USD")
    name: str = Field(default="Dolar/Dolar")
    value: Decimal = Field(alias="high")  # alias é um apelido
    #  os dados retornados pela API estão no campo "high"
    #  mas queremos que na classe seja o nome "value"


def get_rates(currencies: List[str]) -> Dict[str, USDRate]:
    """Gets current rate for USD vs Currenfy"""
    return_data = {}
    for currency in currencies:
        if currency == "USD":
            return_data[currency] = USDRate(high=1)
        else:
            response = httpx.get(API_BASE_URL.format(currency=currency))
            if response.status_code == 200:
                # data = response.json()["USD"]  # parou de ser esse o padrão
                data = response.json()
                data = [*data.values()][0]
                # print(data)
                # breakpoint()
                return_data[currency] = USDRate(**data)
            else:
                return_data[currency] = USDRate(name="api/error", high=0)
    return return_data
