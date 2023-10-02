"""
@FILE_NAME : search_image
-*- coding : utf-8 -*-
@Author : Zhaokugua
@Time : 2023/10/1 22:48
"""
import re
import requests
from requests_toolbelt import MultipartEncoder
#  以图搜图工具
# 采用saucenao、ascii2d和iqdb搜索
# 接口地址
API_URL_SAUCENAO = "https://saucenao.com/search.php"
API_URL_ASCII2D = "https://ascii2d.net/search/url/"
API_URL_IQDB = "https://iqdb.org/"   # 暂未支持
API_URL_TRACE_MOE = "https://api.trace.moe/search?cutBorders&url="
API_URL_ANIME_DB = "https://aiapiv2.animedb.cn/"

# SAUCENAO的APIKEY
# API KEY可以在SAUCENAO注册账号之后在用户中心-API处获取https://saucenao.com/user.php?page=search-api
SAUCENAO_API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
# 最多返回图片数量
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
    result_json = requests.post(f'{API_URL_ANIME_DB}ai/api/detect?force_one=1&model={model}&ai_detect=0', headers=headers, data=encoder).json()
    if not result_json:
        return 'animedb搜索失败！找不到高相似度的匹配。'
    face_num = len(result_json['data'])
    msg = f'animedb搜索成功！识别到{face_num}个角色。'
    count = 1
    for charactor in result_json["data"]:
        char_list = [f'{x["name"]}《{x["cartoonname"]}》' for x in charactor['char'][:MAX_FIND_IMAGE_COUNT]]
        msg = msg + '\n' + f'【角色{count}】\n' + '\n'.join(char_list)
        count += 1
    return msg


if __name__ == '__main__':
    # print(get_saucenao_image('https://blog.jixiaob.cn/content/uploadfile/202210/0b191665462315.jpg'))
    # get_anime_info_by_id(147864)
    # get_ascii2d_image('https://blog.jixiaob.cn/content/uploadfile/202210/0b191665462315.jpg')
    # print(get_trace_moe_image('https://azurlane-anime.jp/story/images/09-4.jpg'))
    print(get_animedb_info('https://azurlane-anime.jp/story/images/09-4.jpg'))
