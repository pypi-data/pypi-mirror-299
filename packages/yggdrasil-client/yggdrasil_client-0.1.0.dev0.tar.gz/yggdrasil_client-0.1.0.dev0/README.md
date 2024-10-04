# Yggdrasil Client based on ADOFAI

基于 [ADOFAI](https://github.com/silverteal/adofai) 和 aiohttp 的 (未完成的) Minecraft Yggdrasil 协议兼容客户端，支持 Mojang 后端。

Yggdrasil 是 Minecraft 中身份验证服务的实现名称。

## 快速开始

```python
import asyncio
from yggdrasil_client import AuthInjCompatibleProvider, MojangProvider


async def usage_example():
    littleskin = AuthInjCompatibleProvider("https://littleskin.cn/api/yggdrasil")
    mojang = MojangProvider()
    async with littleskin as r:
        print(await r.hasJoined("Notch", "serverid"))
        print(await r.query_by_name("Notch"))
        print((await r.profile_public_key()).export_key().decode())
        print((await r.profile_public_keys())[0].export_key().decode())

    async with mojang as r:
        print(await r.hasJoined("Notch", "serverid"))
        print(await r.query_by_name("Notch"))

    asyncio.run(usage_example())

```

没有文档，但是做完的那部分代码很简单。

## 另请参阅

[ADOFAI](https://github.com/silverteal/adofai) 是一组数据模型和配套工具，旨在简化自定义实现 Authlib-injector 的规范
Yggdrasil 服务端、客户端及其配套程序的过程。

[Yggdrasil Scaffold](https://github.com/silverteal/yggdrasil-scaffold) 是基于 ADOFAI 和 FastAPI 的 Yggdrasil
身份验证协议实现脚手架。