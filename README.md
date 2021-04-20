# Crypto watcher
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/crypto_watcher?style=for-the-badge)
![PyPI](https://img.shields.io/pypi/v/crypto_watcher?style=for-the-badge)
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/s3rius/crypto_watcher/Release%20crypto_watcher?style=for-the-badge)


Simple monitoring for your crypto miner.

This tool integrates with binance and NBMiner.

Add secrets file before use.
```
{
    "api_key": "<your api key from binance>",
    "secret_key": "<your secret key from binance>",
    "user_name": "<your username>",
    "algorithm": "ethash"
}
```
Default location of secrets file is `~/.binance_secrets`. But you can set your own by providing parameter.

If you watching from other machine than your miner. You need to provide custom `--nbminer_api` parameter.

Usage:
```
crypto_watcher -n "http://192.168.1.55:22333/" -c EUR
```

You can always check the `--help`.
