from typing import Any, Dict, List, Optional

from rich.layout import Layout
from rich.table import Table
from rich.text import Text

from crypto_watcher.services.binance.models import BinanceStatus
from crypto_watcher.services.cryptonator.models import ExchangeRate
from crypto_watcher.services.nbminer.models import Device, NBMinerStatus


def _get_nb_devices_table(devices: List[Device]) -> Table:
    """Get info about mining devices.

    :param devices: List of mining devices.
    :return: renderable table.
    """
    table = Table(
        "info",
        "accepted",
        "invalid",
        "HashRate",
        "Temp",
        "Fan",
        "Mem",
        "Clock",
        title="Devices list",
    )
    for device in devices:
        table.add_row(
            device.info,
            str(device.accepted_shares),
            str(device.invalid_shares),
            device.hashrate,
            f"{device.temperature} °C",
            f"{device.fan}%",
            f"{device.mem_clock} ({device.mem_utilization}%)",
            f"{device.core_clock} ({device.core_utilization}%)",
        )
    return table


def _get_nb_stratum_table(nb_status: NBMinerStatus) -> Table:  # noqa: WPS213
    """Get NBMiner overall status table.

    :param nb_status: current NBMiner status.
    :return: renderable table of general NBMiner status.
    """
    table = Table.grid()
    table.add_column(justify="left")
    table.add_column(justify="right")
    table.add_row(
        "NBMiner version: ",
        nb_status.version,
    )
    table.add_row("Reboots: ", str(nb_status.reboot_times))
    table.add_row("URL: ", nb_status.stratum.url)
    table.add_row(
        "User: ",
        nb_status.stratum.user,
    )
    table.add_row(
        "Latency: ",
        str(nb_status.stratum.latency),
    )
    table.add_row(
        "Accepts: ",
        str(nb_status.stratum.accepted_shares),
    )
    table.add_row(
        "Rejects: ",
        str(nb_status.stratum.rejected_shares),
    )
    table.add_row("HashRate 10m: ", str(nb_status.stratum.pool_hashrate_10m))
    table.add_row("HashRate 1h: ", str(nb_status.stratum.pool_hashrate_4h))
    table.add_row("HashRate 24h: ", str(nb_status.stratum.pool_hashrate_24h))
    return table


def _get_nb_layout(nb_status: NBMinerStatus) -> Layout:
    """
    Get NBMiner layout.

    :param nb_status: current NBMiner status.
    :return: renderable layout.
    """
    layout = Layout(name="miner_status", ratio=2)
    layout.split_row(
        Layout(_get_nb_stratum_table(nb_status)),
        Layout(_get_nb_devices_table(nb_status.miner.devices), ratio=2),
    )
    return layout


def _get_profit_table(  # noqa: WPS210
    bin_status: BinanceStatus,
    profit_today: Dict[str, ExchangeRate],
    profit_yesterday: Dict[str, ExchangeRate],
) -> Table:
    """Render profit table.

    This table is used to show user's profits
    converted to his local currency.

    :param bin_status: current binance status.
    :param profit_today: today's calculated profit.
    :param profit_yesterday: yesterday's calcualted profit.
    :return: renderable table.
    """
    table = Table(
        "crypto name",
        "24h rate change",
        "profit today",
        "profit yesterday",
        title="Profits",
    )
    for crypto_name in bin_status.profit_today.keys():
        crypto_today = bin_status.profit_today.get(crypto_name, "N/A")
        crypto_yesterday = bin_status.profit_yesterday.get(crypto_name, "N/A")
        rate_today = profit_today.get(crypto_name, "N/A")
        rate_yesterday = profit_yesterday.get(crypto_name, "N/A")
        rate_color = "red" if rate_today.change < 0 else "green"
        table.add_row(
            crypto_name,
            Text(str(rate_today.change), rate_color),
            f"{crypto_today} ({rate_today.rate} {rate_today.target})",
            f"{crypto_yesterday} ({rate_yesterday.rate} {rate_yesterday.target})",
        )
    return table


def _get_binance_status(bin_status: BinanceStatus) -> Table:
    """
    Render a table with overall status from binance.

    :param bin_status: current binance status.
    :return: table with status.
    """
    table = Table.grid()
    table.add_column(justify="left")
    table.add_column(justify="right")
    table.add_row(
        "Today hashrate: ",
        str(bin_status.day_hashrate),
    )
    table.add_row(
        "Invalid shares: ",
        str(bin_status.invalid_num),
    )
    table.add_row(
        "Username: ",
        str(bin_status.user_name),
    )
    return table


def _get_binance_layout(
    bin_status: BinanceStatus,
    profit_today: Dict[str, ExchangeRate],
    profit_yesterday: Dict[str, ExchangeRate],
) -> Layout:
    """
    Binance info Layout.

    :param bin_status: current binance status.
    :param profit_today: today's calculated profit.
    :param profit_yesterday: yesterday's calcualted profit.
    :return: binance renderable layout.
    """
    layout = Layout(name="binance_status")
    layout.split_row(
        Layout(
            _get_binance_status(
                bin_status,
            ),
        ),
        Layout(
            _get_profit_table(bin_status, profit_today, profit_yesterday),
            ratio=2,
        ),
    )
    return layout


def get_layout(
    nb_status: Optional[NBMinerStatus],
    bin_status: BinanceStatus,
    profit_today: Dict[str, ExchangeRate],
    profit_yesterday: Dict[str, ExchangeRate],
) -> Layout:
    """
    Get cli layout.

    :param nb_status: current miner status.
    :param bin_status: current binanace status.
    :param profit_today: Mined amout of crypto today.
    :param profit_yesterday: Mined amount of crypto yesterday.
    :return: layout for render in terminal.
    """
    main_layout = Layout()
    nb_layout: Any = Text("Can't connect to NBMiner.", justify="center")
    if nb_status is not None:
        nb_layout = _get_nb_layout(nb_status)
    bin_layout = _get_binance_layout(bin_status, profit_today, profit_yesterday)
    main_layout.split_column(
        nb_layout,
        bin_layout,
    )
    return main_layout
