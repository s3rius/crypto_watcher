from typing import Dict

from pydantic import BaseModel, Field


class BinanceStatus(BaseModel):
    """Current binance status."""

    algo: str
    unit: str

    day_hashrate: float = Field(alias="dayHashRate")
    fifteen_min_hashrate: float = Field(alias="fifteenMinHashRate")

    invalid_num: int = Field(alias="invalidNum")
    profit_today: Dict[str, float] = Field(alias="profitToday")
    profit_yesterday: Dict[str, float] = Field(alias="profitYesterday")

    user_name: str = Field(alias="userName")
