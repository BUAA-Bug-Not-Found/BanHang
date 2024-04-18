from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import User

class UserAPITestCase(TestCase):
    '''
        这是一个单元测试样例
        单元测试会在一个临时数据库中进行，所以需要什么数据要在setUp函数里面造
        使用python manage.py test运行测试，测试会依次实例化tests.py文件夹下的所有继承自TestCase的类，先执行setUp函数进行初始化
        然后执行所有以test_为开头的函数
    '''
    def setUp(self):
        User.objects.create(username='test',password='123456')
        self.client = APIClient()

    def test_get_user_info(self):
        url = '/banhang/login/'
        response = self.client.post(url, data={'username': 'test', 'password':'123456'}, format='json')
        print(response.content)