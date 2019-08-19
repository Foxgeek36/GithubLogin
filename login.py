# coding=utf-8
import requests
from lxml import html
etree = html.etree

'''
[模拟登陆github]
'''


class Login(object):
    def __init__(self):
        self.headers = {
            'Referer': 'https://github.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/57.0.2987.133 Safari/537.36',
            'Host': 'github.com'
        }
        self.login_url = 'https://github.com/login'  # 初始登录页面
        self.post_url = 'https://github.com/session'  # 输入账号密码之后的登录状态页面
        self.logined_url = 'https://github.com/settings/profile'  # 个人主页页面信息
        self.session = requests.Session()  # 维持会话,自动处理cookies
    
    def token(self):
        '''
        从登录之后的页面中提取出所需参数->authenticity_token
        :return:
        '''
        response = self.session.get(self.login_url, headers=self.headers)
        selector = etree.HTML(response.text)
        token = selector.xpath('//div//input[2]/@value')
        return token
    
    def login(self, email, password):
        '''
        模拟登录及后续操作
        :param email:
        :param password:
        :return:
        '''
        # 核心操作步骤:模拟登录 ++-
        post_data = {
            'commit': 'Sign in',
            'utf8': '✓',
            'authenticity_token': self.token()[0],  # 在登录账号之前随机产生
            'login': email,
            'password': password
        }
        response = self.session.post(self.post_url, data=post_data, headers=self.headers)
        # -----------------------
        if response.status_code == 200:
            self.dynamics(response.text)
        
        response = self.session.get(self.logined_url, headers=self.headers)
        if response.status_code == 200:
            self.profile(response.text)
    
    def dynamics(self, html):
        '''
        提取所有关注的动态信息
        :param html:
        :return:
        '''
        selector = etree.HTML(html)
        dynamics = selector.xpath('//div[contains(@class, "news")]//div[contains(@class, "alert")]')
        for item in dynamics:
            dynamic = ' '.join(item.xpath('.//div[@class="title"]//text()')).strip()
            print(dynamic)
    
    def profile(self, html):
        '''
        从user个人详情页中提取出昵称和邮箱
        :param html:
        :return:
        '''
        selector = etree.HTML(html)
        name = selector.xpath('//input[@id="user_profile_name"]/@value')[0]
        email = selector.xpath('//select[@id="user_profile_email"]/option[@value!=""]/text()')
        print(name, email)


if __name__ == "__main__":
    login = Login()
    login.login(email='2169927630@qq.com', password='123456')
