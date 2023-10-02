# anime_image_search
search anime image 自用机器人搜图封装

提供图片的url地址即可返回搜索结果。

结果已经使用CQ码描述好可以直接发送。

## 🚀目前支持的网站

| 网站名称    | 是否支持 | 备注 |
| --------   | -------  | ----- |
| [ascii2d](https://ascii2d.net/)    | ✔        | ascii2d色阶搜索 |
| [AnimeTrace](https://ai.animedb.cn/) | ✔        | 番剧、Galgame游戏角色搜索 |
| [SauceNAO](https://saucenao.com)   | ✔        | saucenao以图搜图 |
| [TraceMoe](https://trace.moe/)   | ✔        | 番剧截图搜索 |
| [Yandex](https://yandex.com/images)     | ❌       | yandex图片搜索 |
| [EHentai](https://e-hentai.org)    | ❌        | 漫画搜索 |
| [IqDB](https://iqdb.org/)       | ❌        | idqb聚合图片搜索


## 🍭使用示例
安装依赖
```shell
pip install requests requests-toolbelt
```

saucenao搜图API需要API_KEY才能使用，请手动修改以下代码
```python
# SAUCENAO的APIKEY
# API KEY可以在SAUCENAO注册账号之后在用户中心-API处获取https://saucenao.com/user.php?page=search-api
SAUCENAO_API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

可以设置默认返回图片的数量。默认为3个，消息不会过长也能保证搜索精准度。
```python
# 最多返回图片数量
MAX_FIND_IMAGE_COUNT = 3
```

```python
>>> from search_image import *
```

### SauceNAO
<div align="center"> <img src="https://blog.jixiaob.cn/content/uploadfile/202210/0b191665462315.jpg" width="50%"> </div>

```python
>>> get_saucenao_image('https://blog.jixiaob.cn/content/uploadfile/202210/0b191665462315.jpg')
```
```
Saucenao识图成功！
【相似度95.42%】
[CQ:image,file=https://img1.saucenao.com/res/pixiv/10202/manga/102024818_p1.jpg?auth=qYkKnXhzCjoAfBqm0d2C6w&exp=1696359600]
https://www.pixiv.net/member_illust.php?mode=medium&illust_id=102024818
【相似度96.68%】
[CQ:image,file=https://img3.saucenao.com/booru/1/6/169dc549d2c67aaf92ddc831774746c1_2.jpg?auth=qg_Q_-Vf_5qBpvgRIa0Atg&exp=1696359600]  
https://danbooru.donmai.us/post/show/5761914
https://yande.re/post/show/1030049
https://gelbooru.com/index.php?page=post&s=view&id=7833081
https://konachan.com/post/show/348799
【相似度96.62%】
[CQ:image,file=https://img3.saucenao.com/booru/8/9/896859de81a951729d5d3961add7477a_2.jpg?auth=YfPaVw3-fwRYqdctpKyOGQ&exp=1696359600]  
https://danbooru.donmai.us/post/show/5761913
https://yande.re/post/show/1030050
https://gelbooru.com/index.php?page=post&s=view&id=7833082
https://konachan.com/post/show/348800
```
<div align="center"> <img src="https://github.com/Zhaokugua/anime_image_search/blob/main/screenshots/Screenshot_2023-10-02-21-31-48-320_com.tencent.mobileqq.png" width="50%"> </div>

### ascii2d
图片色阶搜索

>已知问题：使用qq私聊图片链接(https://c2cpicdw.qpic.cn/offpic_new/ 这种链接格式)搜索有可能得到无效的搜索结果。
>
>因为未知原因导致ascii2d所读取到的图片信息并非想搜索的信息，而是qq空间的图片防盗链默认图片（此图片来自QQ空间未经允许不可引用）

<div align="center"> <img src="https://blog.jixiaob.cn/content/uploadfile/202210/0b191665462315.jpg" width="50%"> </div>

```python
>>> get_ascii2d_image('https://blog.jixiaob.cn/content/uploadfile/202210/0b191665462315.jpg')
```
```
ascii2d识图成功！
子鶏の姫
[CQ:image,file=https://ascii2d.net/thumbnail/8/9/6/8/896859de81a951729d5d3961add7477a.jpg]
https://www.pixiv.net/artworks/102024818
子鶏の姫
[CQ:image,file=https://ascii2d.net/thumbnail/1/6/9/d/169dc549d2c67aaf92ddc831774746c1.jpg]
https://www.pixiv.net/artworks/102024818
2021.05.09
[CQ:image,file=https://ascii2d.net/thumbnail/0/2/6/6/0266d95e02d694d5ab5ea922bea3fabb.jpg]
https://twitter.com/ShindoWolf0825/status/1391166021571067906
```
<div align="center"> <img src="https://github.com/Zhaokugua/anime_image_search/blob/main/screenshots/Screenshot_2023-10-02-21-31-25-054_com.tencent.mobileqq.png" width="50%"> </div>

### TraceMoe
根据番剧截图搜索番剧，图片尽量不要裁剪，不要有黑边，保持完整的画面，搜索的结果更佳。
<div align="center"> <img src="https://azurlane-anime.jp/story/images/09-4.jpg" width="50%"> </div>

```python
>>> get_trace_moe_image('https://azurlane-anime.jp/story/images/09-4.jpg')
```
```
trace.moe搜图成功！
【相似度95.54%】
[CQ:image,file=https://media.trace.moe/image/104159/%5BOhys-Raws%5D%20Azur%20Lane%20the%20Animation%20-%2009%20(BS11%201280x720%20x264%20AAC).mp4.jpg?t=977.375&now=1696251600&token=y7RxbdZsHZzceq3J5RTO84dWTY]
Azur Lane
AZUR LANE
アズールレーン
Azur Lane
[Ohys-Raws] Azur Lane the Animation - 09 (BS11 1280x720 x264 AAC).mp4 16:15
【相似度95.54%】
[CQ:image,file=https://media.trace.moe/image/104159/Azur%20Lane%20the%20Animation%20-%2009%20(BD%201280x720%20x264%20AAC).mp4.jpg?t=973.29&now=1696251600&token=MStkXFiCkdFARUsImLEtrclVv1A]
Azur Lane
AZUR LANE
アズールレーン
Azur Lane
Azur Lane the Animation - 09 (BD 1280x720 x264 AAC).mp4 16:11
【相似度77.88%】
[CQ:image,file=https://media.trace.moe/image/114043/Shokugeki%20no%20Souma%20Gou%20no%20Sara%20-%2008%20(BD%201280x720%20x264%20AAC).mp4.jpg?t=853.835&now=1696251600&token=WUITHK9z51HTGE4Y41J1XbxmUw]
Shokugeki no Souma: Gou no Sara
Food Wars! The Fifth Plate
食戟のソーマ 豪ノ皿
食戟之靈 豪之皿
Shokugeki no Souma Gou no Sara - 08 (BD 1280x720 x264 AAC).mp4 14:13
```
<div align="center"> <img src="https://github.com/Zhaokugua/anime_image_search/blob/main/screenshots/Screenshot_2023-10-02-21-30-33-864_com.tencent.mobileqq.png" width="50%"> </div>

### AnimeTrace

搜索番剧/部分游戏里的角色

model默认为anime_model_lovelive（最新高准确率公测动漫模型）

还可以选择：anime（地准确率动漫模型） pre_stable（高准确率动漫模型）
<div align="center"> <img src="https://azurlane-anime.jp/story/images/09-4.jpg" width="50%"> </div>

```python
>>> get_animedb_info('https://azurlane-anime.jp/story/images/09-4.jpg')
```
```
animedb搜索成功！识别到6个角色。
【角色1】
ユニコーン《碧蓝航线》
阿波連 れん《测不准的阿波连同学》
一柳 結梨《突击莉莉》
【角色2】
綾波《Azur Lane: Bisoku Zenshin!》
ニニム・ラーレイ《天才王子的赤字国家振兴术》
祝ノリ《Chaos Dragon: Sekiryuu Seneki》
【角色3】
ジャベリン《Azur Lane: Bisoku Zenshin!》
ミズ・シタターレ《Futari wa Precure: Splash☆Star》
キアナ・カスラナ《崩坏3 Reburn》
【角色4】
宮森 あおい《SHIROBAKO》
ペトラ・レイテ《Re：ゼロから始める異世界生活》
羽村 めぐむ（はねむら めぐむ）《絶園のテンペスト》
【角色5】
コマコ・セメノビッチ《少女波子汽水》
刀藤 綺凛《学战都市Asterisk》
イア《Nihonbashi Koukashita R Keikaku》
【角色6】
ラフィー《碧蓝航线》
綾波《Azur Lane: Bisoku Zenshin!》
ベルゼブブ《スライム倒して300年、知らないうちにレベルMAXになってました》
```
搜索Galgame游戏及角色

model可以选择game（低准确率Galgame模型）或者game_model_kirakira（高准确率公测Galgame模型）
<div align="center"> <img src="https://clan.akamai.steamstatic.com/images//36817056/74b0f5fca29e62ded54b8a5ccb7a7389ee20f817.png" width="50%"> </div>

```python
>>> get_animedb_info('https://clan.akamai.steamstatic.com/images//36817056/74b0f5fca29e62ded54b8a5ccb7a7389ee20f817.png', model='game_model_kirakira')
```
```
animedb搜索成功！识别到2个角色。
【角色1】
御園 苺華《巧克甜戀》
天鳥 那由多《NOeSIS 嘘を吐いた記憶の物語》
白花《保健室的老师与沉迷吹泡泡的助手》
【角色2】
雪村 千絵莉《巧克甜戀》
千柚《いもおか》
ミュー《D.C.II To You ～ダ・カーポII～トゥーユー サイドエピソード》
```
