# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
import os
import json

from typing import List

from alibabacloud_green20220302.client import Client as Green20220302Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_green20220302 import models as green_20220302_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient

config = open_api_models.Config(
	access_key_id=os.environ['REVIEW_ACCESS_KEY_ID'],
	access_key_secret=os.environ['REVIEW_ACCESS_KEY_SECRET']
)
config.endpoint = f'green-cip.cn-beijing.aliyuncs.com'

def review_text(content: str, service: str = "comment_detection"):
	client = Green20220302Client(config)
	text_moderation_request = green_20220302_models.TextModerationPlusRequest(
		service=service,
		service_parameters=json.dumps({"content": content}, ensure_ascii=False)
	)
	runtime = util_models.RuntimeOptions()
	try:
		return client.text_moderation_with_options(text_moderation_request, runtime)
	except Exception as error:
		print(error.message)
		print(error.data.get("Recommend"))
		UtilClient.assert_as_string(error.message)

