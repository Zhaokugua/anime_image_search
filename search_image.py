"""
@FILE_NAME : search_image
-*- coding : utf-8 -*-
@Author : Zhaokugua
@Time : 2023/12/4 11:47
"""
import re
import requests
from requests_toolbelt import MultipartEncoder
#  以图搜图工具
# 采用saucenao、ascii2d和iqdb搜索
# 接口地址
API_URL_SAUCENAO = "https://saucenao.com/search.php"
API_URL_ASCII2D = "https://ascii2d.net/search/url/"
API_URL_IQDB = "https://iqdb.org/"
API_URL_TRACE_MOE = "https://api.trace.moe/search?cutBorders&url="
API_URL_ANIME_DB = "https://aiapiv2.animedb.cn/"

# SAUCENAO的APIKEY
SAUCENAO_API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
# AI_OR_NOT的APIKEY
AI_OR_NOT_KEY = 'YOUR_API_KEY'
# 最多返回搜图结果数量
MAX_FIND_IMAGE_COUNT = 3


def get_saucenao_image(img_url):
    params = {
        "output_type": 2,
        "api_key": SAUCENAO_API_KEY,
        "testmode": 1,
        "numres": 6,
        "db": 999,
        "url": img_url,
    }
    res_data = requests.post(API_URL_SAUCENAO, params=params).json()
    if res_data["header"]["status"] != 0:
        return f"Saucenao识图失败..status：{res_data['header']['status']}"
    data = res_data["results"]
    data = (
        data
        if len(data) < MAX_FIND_IMAGE_COUNT
        else data[: MAX_FIND_IMAGE_COUNT]
    )
    res_message = 'Saucenao识图成功！'
    for image_info in data:
        if image_info['data'].get('ext_urls'):
            image_links_str = '\n'.join(image_info['data']['ext_urls'])
        else:
            jp_name = image_info['data'].get('jp_name')
            eng_name = image_info['data'].get('eng_name')
            title = image_info['data'].get('title')
            part = image_info['data'].get('part')
            if jp_name or eng_name:
                image_links_str = f"{jp_name}\n{eng_name}"
            elif title or part:
                image_links_str = f'{title} {part}'
            else:
                image_links_str = str(image_info['data'])
        res_message = res_message + '\n' + f'【相似度{image_info["header"]["similarity"]}%】\n' \
                                           f'[CQ:image,file={image_info["header"]["thumbnail"]}]\n' \
                                           f'{image_links_str}'
    return res_message


def get_ascii2d_image(img_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.47'
    }
    search_url = f'https://ascii2d.net/search/url/{img_url}'
    res_info = requests.get(search_url, headers=headers)
    # redirect_url = res_info.history[0].text[35:101]
    # res_info2 = requests.get(redirect_url, headers=headers)
    html_text = res_info.text.replace('\n', '').replace('\r', '')
    re_res = re.findall(r'item-box.*?lazy(.*?)alt=.*?noopener(.*?)>(.*?)</a>.*?clearfix', html_text)
    re_res = re_res[:MAX_FIND_IMAGE_COUNT]
    res_message = 'ascii2d识图成功！'
    base_url = 'https://ascii2d.net/'
    for img_info in re_res:
        res_message = res_message + '\n' + img_info[2] + '\n' +\
                      f'[CQ:image,file={base_url + img_info[0][8:-2]}]\n' + img_info[1][8:-1]

    return res_message


def get_trace_moe_image(img_url):
    result = requests.get(API_URL_TRACE_MOE + img_url).json().get('result')
    if not result:
        return 'trace.moe搜图失败！'
    result = result[:MAX_FIND_IMAGE_COUNT]
    res_message = 'trace.moe搜图成功！'
    for each_info in result:
        media_name_dict = get_anime_info_by_id(each_info['anilist'])['title']
        title_list = media_name_dict.values()
        if None not in title_list:
            media_name_str = '\n'.join(title_list)
        else:
            media_name_str = ''
        similarity = round(each_info["similarity"]*100, 2)
        time_info = f'{int(each_info["from"])//60}:{int(each_info["from"])%60}'
        res_message = res_message + '\n' + f'【相似度{similarity}%】\n[CQ:image,file={each_info["image"]}]\n' \
                                           f'{media_name_str}\n' \
                                           f'{each_info["filename"]} {time_info}'
    return res_message


def get_anime_info_by_id(anime_id):
    query = '''
    query ($id: Int) { # Define which variables will be used in the query (id)
      Media (id: $id, type: ANIME) { # Insert our variables into the query arguments (id) (type: ANIME is hard-coded in the query)
        id
        title {
          romaji
          english
          native
        }
      }
    }
    '''

    req_url = 'https://trace.moe/anilist/'
    variables = {
        'id': anime_id
    }
    res_info = requests.post(req_url, json={'query': query, 'variables': variables}).json()
    return res_info['data']['Media']


def get_animedb_info(img_url, model='anime_model_lovelive'):
    # anime model: anime anime_model_lovelive pre_stable
    # galgame model: game game_model_kirakira
    image_data_content = requests.get(img_url).content
    encoder = MultipartEncoder(
        {
            'image': ('test.jpg', image_data_content, "image/jpeg"),
        }
    )

    headers = {
        'Content-Type': encoder.content_type,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.47',
        'Referer': 'https://ai.animedb.cn/',
        'Origin': 'https://ai.animedb.cn'
    }
    result_json = requests.post(f'{API_URL_ANIME_DB}ai/api/detect?force_one=1&model={model}&ai_detect=1', headers=headers, data=encoder).json()
    ai_info = result_json['ai']
    ai_msg = '【该图片很可能是ai图】' if ai_info else '【该图片可能不是ai图】'
    if not result_json['data']:
        return ai_msg + '\n' + 'animedb搜索失败！找不到高相似度的匹配。'
    face_num = len(result_json['data'])
    msg = ai_msg + '\n' + f'animedb搜索成功！识别到{face_num}个角色。'
    count = 1
    for charactor in result_json["data"]:
        char_list = [f'{x["name"]}《{x["cartoonname"]}》' for x in charactor['char'][:MAX_FIND_IMAGE_COUNT]]
        msg = msg + '\n' + f'【角色{count}】\n' + '\n'.join(char_list)
        count += 1
    return msg


def ai_detect(image_url, mode=1):
    if mode == 0:
        res_message = '根据aiornot.com的鉴定结果，'
        # 免费版API每月限额100
        AI_OR_NOT_headers = {
            'Authorization': 'Bearer ' + AI_OR_NOT_KEY,
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
        AI_OR_NOT_url = 'https://api.aiornot.com/v1/reports/image'
        AI_OR_NOT_body = {
            'object': f'{image_url}'
        }
        res = requests.post(AI_OR_NOT_url, headers=AI_OR_NOT_headers, json=AI_OR_NOT_body).json()
        res_message = res_message + '该图片很有可能是AI图' if res['report']['ai']['is_detected'] else res_message + '该图片很可能不是AI图'
    else:
        res_message = 'hivemoderation.com的鉴定结果概率如下：\n'

        # 这是自己试出来的直接提供图片url鉴别的方法
        req_url = f'https://ajax.thehive.ai/api/demo/classify?endpoint=ai_generated_image_detection&email_to=&data_url=&hash=&check_cache=true&image_url={image_url}'
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json',
            'Origin': 'https://hivemoderation.com',
            'Referer': 'https://hivemoderation.com/',
        }
        data = {
            'media_type': 'photo',
            'model_type': 'classification',
        }
        res = requests.post(req_url, headers=headers, json=data).json()

        # 下面是官网抓包得到的POST上传图片的方法
        # req_url = f'https://ajax.thehive.ai/api/demo/classify?endpoint=ai_generated_image_detection&email_to=&data_url=&hash=&check_cache=true&image_url='
        # image_data_content = requests.get(image_url).content
        # encoder = MultipartEncoder(
        #     {
        #         'media_type': 'photo',
        #         'model_type': 'classification',
        #         'image': ('test.jpg', image_data_content, "image/jpeg"),
        #     }
        # )
        # headers = {
        #     'Accept': 'application/json, text/plain, */*',
        #     'Content-Type': encoder.content_type,
        #     'Origin': 'https://hivemoderation.com',
        #     'Referer': 'https://hivemoderation.com/',
        # }
        #
        # res = requests.post(req_url, data=encoder, headers=headers).json()
        translate_dict = {
            'not_ai_generated': '不是AI生成',
            'ai_generated': '是AI生成',
            'none': '未检测到AI',
            'dalle': 'OpenAI Dalle模型生成',
            'midjourney': 'midjourney模型生成',
            'stablediffusion': 'StableDiffusion(SD)模型生成',
            'hive': 'hive模型生成',
            'bingimagecreator': '必应图片生成工具生成',
            'gan': 'GAN生成对抗网络生成',
            'adobefirefly': 'Adobe Firefly萤火虫生成',
            'kandinsky': 'kandinsky开源AI模型生成',
            'stablediffusionxl': 'StableDiffusionXL(SDXL)模型生成'
        }
        # {'return_code': 400, 'message': 'Unable to download file from url'}
        if not res.get('response'):
            if res['message'] == 'Unable to download file from url':
                return f'图片无法上传到ai图片鉴别的服务器。请尝试压缩图片或在群里发送图片。'

            print('搜索出错！：\n', res)
            return f'ai图片鉴别出错，请稍后重试。\n{res}'
            
        res_classes = res['response']['output'][0]['classes']
        res_classes = [{'class': translate_dict.get(x['class'], x['class']), 'score': x['score']} for x in res_classes]
        res_classes = sorted(res_classes, key=lambda x: x['score'], reverse=True)
        res_classes = res_classes[:3]
        for each_class in res_classes:
            res_message = res_message + f"\n{each_class['class']}: {round(each_class['score'] * 100, 2)}%"
        print('喵')

    return res_message


def get_soutu_bot_image(img_url):
    image_data_content = requests.get(img_url).content
    encoder = MultipartEncoder(
        {
            'file': ('test.jpg', image_data_content, "image/jpeg"),
            'factor': '1.2',
        }
    )

    headers = {
        'Content-Type': encoder.content_type,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.47',
        'Referer': 'https://soutubot.moe/',
        'Origin': 'https://soutubot.moe',
        'X-Api-Key': '',
        'X-Requested-With': 'XMLHttpRequest',
    }

    # js的源码在这里，对时间戳和浏览器ua的长度分别求平方然后加起来，后来又改了又加了一个window.GLOBAL.m
    # 不知道这个是什么，这个过一段时间会刷新，但是需要手动刷新浏览器才能刷新，不刷新浏览器页面的话在网页上也不能用
    # 先写个常量放上去试试
    # 然后将上面得到的数字转换成字符串，进行base64编码，然后进行逆序，再把=等其他字符去掉，就得到了X-Api-Key
    # 方法参考https://www.cnblogs.com/znsbc-13/p/17437493.html
    # const RC = ()=>{
    #         const e = (Math.pow(Q().unix(), 2) + Math.pow(window.navigator.userAgent.length, 2) + window.GLOBAL.m).toString();
    #         return En.encode(e).split("").reverse().join("").replace(/=/g, "")
    #     }
    Q = str(int(pow(time.time(), 2)) + int(pow(len(headers["User-Agent"]), 2)) + 3008452091121)
    encoded_data = str(base64.b64encode(Q.encode()).decode())[::-1].replace("=", "")
    headers.update({"X-Api-Key": encoded_data})

    res = requests.post(f'https://soutubot.moe/api/search', headers=headers, data=encoder)
    if res.status_code != 200:
        if res.status_code == 401:
            res_msg = '接口坏掉了qwq你可以自己试着去搜：https://soutubot.moe'
        elif res.status_code == 403:
            if 'Just a moment...' in res.text:
                res_msg = '被cloudflare拦截了qwq你可以自己试着去搜：https://soutubot.moe'
            else:
                res_msg = f'未知错误HTTP{res.status_code} {res.text}'
        else:
            res_msg = f'未知错误HTTP{res.status_code} {res.text}'
    else:
        result_json = res.json()
        res_msg = 'soutubot.moe搜索结果如下：'

        ehentai_mirror_list = ['https://exhentai.org', 'https://e-hentai.org']
        nhentai_mirror_list = ['https://nhentai.net', 'https://nhentai.xxx']

        mirror_link = {
            'ehentai': ehentai_mirror_list[0],
            'nhentai': nhentai_mirror_list[0],
        }

        for result in result_json['data'][:MAX_FIND_IMAGE_COUNT]:
            res_msg = res_msg + '\n' + f'【相似度{result["similarity"]}%】\n[CQ:image,file={result["previewImageUrl"]}]\n' \
                                       f'{result["title"]}\n{mirror_link[result["source"]]}{result["subjectPath"]}'

    return res_msg


if __name__ == '__main__':
    # print(get_saucenao_image('https://blog.jixiaob.cn/content/uploadfile/202210/0b191665462315.jpg'))
    # get_anime_info_by_id(147864)
    # get_ascii2d_image('https://blog.jixiaob.cn/content/uploadfile/202210/0b191665462315.jpg')
    # print(get_trace_moe_image('https://azurlane-anime.jp/story/images/09-4.jpg'))
    print(get_animedb_info('https://azurlane-anime.jp/story/images/09-4.jpg'))
    # print(get_trace_moe_image('https://gchat.qpic.cn/gchatpic_new/1066168689/937972042-2195784184-0F05C3E5B3CDFEE87A68155A5C8276F1/0?term=2&amp;is_origin=0'))
    # print(get_animedb_info('https://myhkw.cn/openapi/img/acg/0072Vf1pgy1foxk6jltvsj31hc0u0kbm.jpg'))
    print(ai_detect('https://blog.jixiaob.cn/content/uploadfile/202210/0b191665462315.jpg'))
    print(get_soutu_bot_image('https://i7.nhentai.net/galleries/886703/14.jpg'))
    print('喵')

