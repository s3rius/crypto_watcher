from pydantic import BaseModel


class Ticker(BaseModel):
    """Exchange rate response from cryptonator.com."""

    base: str
    target: str
    price: float
    volume: float
    change: float


class ExchangeRate(Ticker):
    """Exchange rate for cryptocurrency."""

    rate: str
