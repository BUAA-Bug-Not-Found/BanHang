from functools import wraps
import inspect
from fastapi import Request
import jwt
import time
import inspect


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
    async def _wrapped_view(request: Request, *args, **kwargs):
        cookie = request.headers.get('Authorization')
        uid = None
        username = None
        try:
            token = cookie.split(' ')[1]
            payload = decodeToken(token)  # 假设这里是解码token的函数
            if payload:
                uid = payload['uid']
                username = payload['username']
        except:
            pass
        if 'uid' in view_func.__code__.co_varnames:
            kwargs['uid'] = payload['uid']
        if 'username' in view_func.__code__.co_varnames:
            kwargs['username'] = payload['username']
        return await view_func(*args, **kwargs)
    
    params = inspect.signature(_wrapped_view).parameters
    new_params = {}
    for key, value in params.items():
        if key not in {'uid', 'username'}:
            new_params[key] = value
    new_params = list(new_params.values()) + [inspect.Parameter('request', inspect.Parameter.POSITIONAL_OR_KEYWORD, default=None, annotation=Request)]
    _wrapped_view.__signature__ = inspect.Signature(new_params)

    return _wrapped_view