import setuptools

with open("README.md", "r", encoding="utf-8", errors="ignore") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nonebot-weather",
    version="1.3",
    author="hriyel",
    author_email="1249781871@qq.com",
    keywords=["pip", "nonebot2", "nonebot", "weather", "nonebot_plugin"],
    description="一个以nonebot为框架的天气查询插件",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hriyel/nonebot-weather.git",  # Removed the incorrect quotation mark
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    platforms="any",
    install_requires=[
        "nonebot2 >= 2.0.0b1",
        "nonebot-adapter-onebot >= 2.0.0b1",  # Added the missing comma
        "aiohttp >= 3.0"
    ]
)