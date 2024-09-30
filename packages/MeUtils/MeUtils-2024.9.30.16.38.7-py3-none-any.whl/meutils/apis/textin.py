#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : textin
# @Time         : 2024/6/26 08:22
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : todo: 重构 https://tools.textin.com/
# https://www.textin.com/console/recognition/robot_enhance?service=watermark-remove
from meutils.pipe import *
from meutils.io.files_utils import to_url


@alru_cache(ttl=3600 * 24)
async def textin_fileparser(data: bytes, page_count: int = 1000, service: str = "pdf_to_markdown"):
    params = {
        "service": service,
        "page_count": page_count,
        # "get_image": "objects"
        "apply_document_tree": 0
    }

    base_url = f"https://api.textin.com/home/user_trial_ocr?service={service}&page_count={page_count}"
    async with httpx.AsyncClient(base_url=base_url, timeout=120) as client:
        response = await client.post('/', content=data)
        response.raise_for_status()

        # logger.info(response.json())

        if response.is_success:
            return response.json()


if __name__ == '__main__':
    # data = open("/Users/betterme/PycharmProjects/AI/11.jpg", 'rb').read()
    # # data = open("/Users/betterme/PycharmProjects/AI/蚂蚁集团招股书.pdf", 'rb').read()
    # with timer("解析"):
    #     # arun(textin_fileparser(data))
    #     print(arun(textin_fileparser(data, service="pdf_to_markdown")))

    # response = requests.request("POST", url, data=data)
    data = open("/Users/betterme/PycharmProjects/AI/MeUtils/meutils/io/x.png", 'rb').read()

    from meutils.schemas.task_types import Purpose

    service = Purpose.watermark_remove
    with timer("解析"):
        # arun(textin_fileparser(data))
        data = arun(textin_fileparser(data, service=service))

        b64 = data['data']['result']['image']

        # base64_to_file(b64, "demo.png")

        data['data']['result']['image'] = arun(to_url(b64))

        logger.debug(data)

        # {'msg': 'success',
        #  'data': {
        #      'result': {
        #          'image': 'https://sfile.chatglm.cn/chatglm-videoserver/image/e5/e5d4011c.png'
        #      },
        #      'file_type': '', 'file_data': ''
        #  }, 'code': 200
        #  }
