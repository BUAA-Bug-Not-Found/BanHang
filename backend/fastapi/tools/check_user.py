from functools import wraps
import inspect
from fastapi import Request
from typing import Optional,Annotated
import jwt
import time
import inspect

from fastapi import Cookie

KEY = "ORANGE IS THE BEST PRODUCT MANAGER IN THE WORLD!!!!!!!!!"
AGING = 8640000
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
    
def decodeCookie(request:Request)-> tuple[int, str]:
    try:
        cookie = request.headers.get('Authorization')
        token = cookie.split(' ')[1]
        payload = decodeToken(token)
        return payload['uid'], payload['username']
    except:
        return None, None
    

def check_user(view_func):
    '''
    将这个装饰器应用在一个视图函数上，函数的参数中声明uid或username（可以只添加其中一个，也可以都添加），会自动检查cookie并注入到这两个参数上。
    如果cookie检测失败，参数中会被注入None，所以使用前记得检查None！
    '''
    @wraps(view_func)
    def sync_wrapped_view(request: Request, *args, **kwargs):
        cookies= request.cookies
        payload = None
        try:
            if "Auth" in cookies:
                token = cookies["Auth"]
                payload = decodeToken(token)
        except:
            pass
        if not payload:
            return view_func(*args, **kwargs)
        if 'uid' in view_func.__code__.co_varnames:
            kwargs['uid'] = payload.get('uid')
        if 'username' in view_func.__code__.co_varnames:
            kwargs['username'] = payload.get('username')
        return view_func(*args, **kwargs)
    
    wrapped_view = sync_wrapped_view
    params = inspect.signature(wrapped_view).parameters
    new_params = {}
    for key, value in params.items():
        if key not in {'uid', 'username'}:
            new_params[key] = value
    new_params = list(new_params.values()) + [inspect.Parameter('request', inspect.Parameter.POSITIONAL_OR_KEYWORD, default=None, annotation=Request)]
    wrapped_view.__signature__ = inspect.Signature(new_params)

    return wrapped_view

def authorize(Auth: Annotated[Optional[str], Cookie()] = None):
    none_ret = None
    if not Auth:
        return none_ret
    payload = decodeToken(Auth)
    if payload:
        return payload
    return none_ret


