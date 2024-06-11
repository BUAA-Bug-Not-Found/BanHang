# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
import os
import json
from tools.check_environment import in_pytest

from typing import List

from alibabacloud_green20220302.client import Client as Green20220302Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_green20220302 import models as green_20220302_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient
ENABLE = True
if ENABLE and (not in_pytest()):
    config = open_api_models.Config(
        access_key_id=os.environ['REVIEW_ACCESS_KEY_ID'],
        access_key_secret=os.environ['REVIEW_ACCESS_KEY_SECRET']
    )
    config.endpoint = f'green-cip.cn-beijing.aliyuncs.com'


def review_text(content: str, service: str = "comment_detection_pro"):
    if (not ENABLE) or in_pytest():
        return []
    client = Green20220302Client(config)
    text_moderation_plus_request = green_20220302_models.TextModerationPlusRequest(
        service=service,
        service_parameters=json.dumps({"content": content}, ensure_ascii=False)
    )
    runtime = util_models.RuntimeOptions()
    try:
        labels = []
        result = client.text_moderation_plus_with_options(text_moderation_plus_request, runtime)
        for res in result.body.data.result:
            if (res.label == "nonLabel"):
                continue
            if res.confidence == None or res.confidence >= 60:
                labels.append(res.label)
        return labels
    except Exception as error:
        return ["review_error"]
