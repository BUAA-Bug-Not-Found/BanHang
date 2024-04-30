class UniException(Exception):
    def __init__(self, key,value, others=None):
        if not others:
            others = {"description":  "请求错误"}
        self.key = key
        self.value = value
        self.others = others