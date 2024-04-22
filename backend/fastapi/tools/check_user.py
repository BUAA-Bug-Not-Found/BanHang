from functools import wraps
import inspect
from typing import Optional

import jwt
import time

from fastapi import Cookie

KEY = "ORANGE IS THE BEST PRODUCT MANAGER IN THE WORLD!!!!!!!!!"
AGING = 86400
def generate_jwt_token(uid:int, username:str):
    expiration_time = time.time() + AGING
    payload = {
        'uid': uid,
        'username': username,
        'exp': expiration_time
    }
    token = jwt.encode(payload, KEY, algorithm='HS256')

    return token

def decodeToken(token:str):
    try:
        payload = jwt.decode(token, KEY, algorithms=['HS256'])
        if 'exp' in payload and payload['exp'] >= time.time():
            return payload
        else:
            return None
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def authorize(Auth: Optional[str] = Cookie(None)):
    none_ret = None
    if not Auth:
        return none_ret
    payload = decodeToken(Auth)
    if payload:
        return payload
    return none_ret

# def check_user(view_func):
#     '''
#         验证用户身份
#         该装饰器修饰一个视图函数，其第一个参数必须是request，request后面可以跟uid和username两个参数。必须与@api_view装饰器同时使用且位于其下面。
#         如果失败，则返回Response
#     '''
#     @wraps(view_func)
#     def _wrapped_view( *args, **kwargs):
#         auth_header = request.META.get('HTTP_AUTHORIZATION')
#
#         if not auth_header:
#             return {'error': 'Token is missing'}
#
#         try:
#             token = auth_header.split(' ')[1]
#             payload = decodeToken(token)
#             if payload:
#                 if 'uid' in inspect.signature(view_func).parameters:
#                     kwargs['uid'] = payload.get('uid')
#                 if 'username' in inspect.signature(view_func).parameters:
#                     kwargs['username'] = payload.get('username')
#                 return view_func(request, *args, **kwargs)
#             return {'error': '无效token'}
#         except (IndexError, KeyError):
#             return {'error': 'Invalid token format or missing payload data'}
#
#     return _wrapped_view