# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
import os
import sys

from typing import List

from alibabacloud_dm20151123.client import Client as Dm20151123Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dm20151123 import models as dm_20151123_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient
import email_validator

def is_valid_email(addr):
    try:
        return email_validator.validate_email(addr)
    except:
        return False

class MailSender:
    def __init__(self):
        pass

    @staticmethod
    def create_client() -> Dm20151123Client:
        """
        使用AK&SK初始化账号Client
        @return: Client
        @throws Exception
        """
        # 工程代码泄露可能会导致 AccessKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考。
        # 建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378659.html。
        config = open_api_models.Config(
            # 必填，请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_ID。,
            access_key_id=os.environ['ALIBABA_CLOUD_ACCESS_KEY_ID'],
            # 必填，请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_SECRET。,
            access_key_secret=os.environ['ALIBABA_CLOUD_ACCESS_KEY_SECRET']
        )
        # Endpoint 请参考 https://api.aliyun.com/product/Dm
        config.endpoint = f'dm.aliyuncs.com'
        return Dm20151123Client(config)

    @staticmethod
    def send(
        addr:str,checkcode:int
    ) -> None:
        client = MailSender.create_client()
        single_send_mail_request = dm_20151123_models.SingleSendMailRequest(
            account_name='banhang@lyhtool.com',
            address_type=1,
            reply_to_address=False,
            to_address=addr,
            subject='关于使用伴航平台有关事项的通知',
            text_body='欢迎使用本平台，请在页面上输入验证码{}。祝您有个美好的旅程。'.format(checkcode),
            tag_name='checkcode',
            from_alias='伴航团队',
            click_trace='1'
        )
        runtime = util_models.RuntimeOptions()
        try:
            # 复制代码运行请自行打印 API 的返回值
            client.single_send_mail_with_options(single_send_mail_request, runtime)
        except Exception as error:
            # 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
            # 错误 message
            print(error.message)
            # 诊断地址
            print(error.data.get("Recommend"))
            UtilClient.assert_as_string(error.message)

    @staticmethod
    async def send_async(
        args: List[str],
    ) -> None:
        client = MailSender.create_client()
        single_send_mail_request = dm_20151123_models.SingleSendMailRequest(
            account_name='banhang@mail.lyhtool.com',
            address_type=1,
            reply_to_address=False,
            to_address='luyuheng2002325@163.com',
            subject='伴航验证码',
            html_body='',
            text_body='验证码123456'
        )
        runtime = util_models.RuntimeOptions()
        try:
            # 复制代码运行请自行打印 API 的返回值
            await client.single_send_mail_with_options_async(single_send_mail_request, runtime)
        except Exception as error:
            # 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
            # 错误 message
            print(error.message)
            # 诊断地址
            print(error.data.get("Recommend"))
            UtilClient.assert_as_string(error.message)


if __name__ == '__main__':
    MailSender.main(sys.argv[1:])
