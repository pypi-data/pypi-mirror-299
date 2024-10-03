from nonebot import on_command
from nonebot.matcher import Matcher
from nonebot.params import CommandArg
from urllib.parse import quote
from nonebot.adapters.onebot.v11 import Message
from nonebot.adapters import Bot, Event
from nonebot.typing import T_State
from nonebot.plugin import PluginMetadata
from .config import Config

import aiohttp

__plugin_meta__ = PluginMetadata(
    name="{天气查询插件}",
    description="{查询天气}",
    usage="{查询天气{天气 城市}}",
    type="{application}",
    homepage="{https://github.com/hriyel/nonebot-weather.git}",
    config=Config,
    supported_adapters={"~onebot.v11", "~telegram"},
)

wettr = on_command('天气', aliases={'wttr', 'weather', 'tianqi'})

@wettr.handle()
async def _handle(matcher: Matcher, city: Message = CommandArg()):
    city_text = city.extract_plain_text()
    if city_text and city_text[0] != '_':
        matcher.set_arg('city', city_text)
    else:
        await wettr.finish('请输入正确的格式来让我观测，如[天气 「城市」] ')

@wettr.got('city', prompt='你想查询哪个城市的天气呢？')
async def handle_weather(bot: Bot, event: Event, state: T_State):
    city = state['city']
    await wettr.send('少女观星中...', at_sender=True)
    try:
        # 使用 quote 函数对城市名称进行URL编码
        escaped_city = quote(city)
        # 构建纯文本格式的URL
        text_url = f"http://wttr.in/{escaped_city}?FnQdT2&lang=zh"
        # 创建 aiohttp 客户端
        async with aiohttp.ClientSession() as session:
            # 发送HTTP请求获取天气信息
            async with session.get(text_url) as response:
                weather_data = await response.text()
                # 发送纯文本天气信息
                weather_data="\n我观测到"+str(city)+"的天气是\n"+weather_data
                await wettr.send(weather_data, at_sender=True)
    except Exception as e:
        # 如果发送失败，发送错误信息
        await wettr.send(f'观测失败，原因是：{str(e)}', at_sender=True)