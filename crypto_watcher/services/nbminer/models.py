from typing import List

from pydantic import BaseModel


class Device(BaseModel):
    """Miner device model."""

    id: int
    info: str  # noqa: WPS110
    pci_bus_id: int
    power: int

    accepted_shares: int
    invalid_shares: int

    mem_clock: int
    mem_utilization: int
    core_clock: int
    core_utilization: int
    fan: int
    temperature: int

    hashrate: str
    hashrate_raw: str


class MinerStatus(BaseModel):
    """Overall miner status."""

    devices: List[Device]
    total_hashrate: str
    total_hashrate_raw: float
    total_power_consume: int


class StratumStatus(BaseModel):
    """NBminer settings and status."""

    accepted_shares: int
    algorithm: str
    difficulty: str
    dual_mine: bool
    invalid_shares: int
    latency: int

    pool_hashrate_10m: str  # noqa: WPS114
    pool_hashrate_4h: str  # noqa: WPS114
    pool_hashrate_24h: str  # noqa: WPS114

    url: str
    use_ssl: bool
    user: str

    rejected_shares: int


class NBMinerStatus(BaseModel):
    """NBMiner current status."""

    miner: MinerStatus
    stratum: StratumStatus

    start_time: int
    reboot_times: int
    version: str
