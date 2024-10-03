#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   http_client.py
@Time    :   2024-04-29 13:37:52
@Author  :   chakcy 
@Email   :   947105045@qq.com
@description   :   http/https请求工具类
'''

import requests 
from ..cache import cache 
from ..model import ResponseError, Response


class HttpClient:
    def __init__(self, base_url=""):
        self.base_url = base_url
        self.session = requests.Session()
  
    def set_token(self, token):
        cache.set("token", token)

    def request(self, method, endpoint, **kwargs):
        url = self.base_url + endpoint  
        # 在这里可以添加请求前的拦截逻辑，比如打印日志、修改请求参数等
        token = cache.get('token')
        if token != '':
            headers = {'Authorization': f'Bearer {token}'}
            kwargs.setdefault('headers', {}).update(headers)  # 确保headers中包含token  
        try:
            response = self.session.request(method, url, **kwargs)  
        # 判断网络是否连接异常
            if response.status_code == 401:
                return ResponseError(status_code=401, error="Unauthorized")
            if response.status_code == 403:
                return ResponseError(status_code=403, error="Forbidden")
            if response.status_code == 404:
                return ResponseError(status_code=404, error="Not Found")
            if response.status_code == 500:
                return ResponseError(status_code=500, error="Internal Server Error")
        except requests.exceptions.RequestException as e:  
            return ResponseError(status_code=500, error=str(e)) 
        # 在这里可以添加响应后的拦截逻辑，比如错误处理、数据转换等    
        return Response(response=response)

    def get(self, endpoint, **kwargs):  
        return self.request('GET', endpoint, **kwargs)  
  
    def post(self, endpoint, **kwargs):  
        return self.request('POST', endpoint, **kwargs)

    def put(self, endpoint, **kwargs):  
        return self.request('PUT', endpoint, **kwargs)
    
    def delete(self, endpoint, **kwargs):  
        return self.request('DELETE', endpoint, **kwargs)
  
    # 可以根据需要添加其他HTTP方法，如PUT, DELETE等  
  
# response = http_client.get("users/123", params={"include": "profile"})  
# if response.status_code == 200:  
#     data = response.json()  
#     print(data)  
# else:  
#     print(f"Request failed with status {response.status_code}: {response.text}")

# response = httpClient.post("users", json={"name": "John Doe", "email": "johndoe@example.com"})  
# if response.status_code == 201:  
#     data = response.json()  
#     print(data)  
# else:  
#     print(f"Request failed with status {response.status_code}: {response.text}")