# Crypto watcher
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/crypto_watcher?style=for-the-badge)](https://pypi.org/project/crypto-watcher/)
[![PyPI](https://img.shields.io/pypi/v/crypto_watcher?style=for-the-badge)](https://pypi.org/project/crypto-watcher/)
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/s3rius/crypto_watcher/Release%20crypto_watcher?style=for-the-badge)


## Cryptocurrency monitoring made simple.

This tool integrates with Binance, NBMiner and Cryptonator.

It' really simple to use. It monitors your crypto-currency minerson binance and shows your current profits converted to your local currency! Isn't that great?

You can take a look how it looks like.

[![asciicast](https://asciinema.org/a/409013.svg)](https://asciinema.org/a/409013?autoplay=1)

## Installation

To install the crypto_watcher you only need Python and Pip installed. And now you need to do the following:
```bash
pip install "crypto_watcher"
```

And now you can run it.

## Usage

You need to create and place somewhere your secrets file. It's  just a JSON file.
```json
{
    "api_key": "<your api key from binance>",
    "secret_key": "<your secret key from binance>",
    "user_name": "<your username>", // Your binance mining account username.
    "algorithm": "ethash" // This algorithm is used, if watcher can't connect to NBMiner API.
}
```
Default location of secrets file is `~/.binance_secrets`. But you can set your own by providing a parameter.

If you want to watch from other machine than your miner, you need to provide custom `--nbminer_api` parameter.

Usage:
```
crypto_watcher -n "http://192.168.1.55:22333/" -c EUR
```

Also, if binance can't handle your queries you can switch between binance api urls. You can find additional adresses [here](https://binance-docs.github.io/apidocs/spot/en/#general-info).

You can always check the `--help`.
