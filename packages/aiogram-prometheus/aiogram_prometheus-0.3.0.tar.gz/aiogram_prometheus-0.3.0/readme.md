# Aiogram Prometheus Collector

Aiogram Based Metrics Collection for Prometheus

[![PyPI](https://img.shields.io/pypi/v/aiogram-prometheus)](https://pypi.org/project/aiogram-prometheus/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/aiogram-prometheus)](https://pypi.org/project/aiogram-prometheus/)
[![Docs](https://img.shields.io/badge/docs-exists-blue)](https://projects.rocshers.com/open-source/aiogram-prometheus)

[![Downloads](https://static.pepy.tech/badge/aiogram-prometheus)](https://pepy.tech/project/aiogram-prometheus)
[![GitLab stars](https://img.shields.io/gitlab/stars/rocshers/python/aiogram-prometheus)](https://gitlab.com/rocshers/python/aiogram-prometheus)
[![GitLab last commit](https://img.shields.io/gitlab/last-commit/rocshers/python/aiogram-prometheus)](https://gitlab.com/rocshers/python/aiogram-prometheus)

## Functionality

- Monitoring the `status` of bots and dispatchers
- Middleware for monitoring the bot's `network activity`
- Middleware for monitoring the `event handler performance`

![example](https://gitlab.com/rocshers/python/aiogram-prometheus/-/raw/release/docs/grafana_example.png)

## Installation

`pip install aiogram-prometheus`

## Quick start

- **aiogram_prometheus.PrometheusWrapperStorage** - Collecting `storage` usage metrics
- **aiogram_prometheus.PrometheusUpdatesMiddleware** - Collecting information about dispatcher `updates`

```python
import os

import aiogram
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from aiogram_prometheus import PrometheusUpdatesMiddleware, PrometheusWrapperStorage

bot = Bot(os.environ['ENV_TG_BOT'])

dp = Dispatcher(storage=PrometheusWrapperStorage(MemoryStorage()))
dp.update.middleware(PrometheusUpdatesMiddleware())

if __name__ == '__main__':
    asyncio.run(dp.start_polling(bot))

```

## Classes

### aiogram_prometheus.PrometheusWrapperStorage

A wrapper around any storage you use that will collect usage metrics

```python
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from aiogram_prometheus import PrometheusWrapperStorage

dp = Dispatcher(storage=PrometheusWrapperStorage(MemoryStorage()))
```

### aiogram_prometheus.PrometheusUpdatesMiddleware

Intermediate layer for collecting metrics of updates processing

```python
from aiogram import Dispatcher
from aiogram_prometheus import PrometheusUpdatesMiddleware

dp = Dispatcher()
dp.update.middleware(PrometheusUpdatesMiddleware())
```

## Contribute

Issue Tracker: <https://gitlab.com/rocshers/python/aiogram-prometheus/-/issues>  
Source Code: <https://gitlab.com/rocshers/python/aiogram-prometheus>

Before adding changes:

```bash
make install-dev
```

After changes:

```bash
make format test
```
