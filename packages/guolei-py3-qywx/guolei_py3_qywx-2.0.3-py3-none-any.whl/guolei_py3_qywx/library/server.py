#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
=================================================
作者：[郭磊]
手机：[15210720528]
Email：[174000902@qq.com]
Github：https://github.com/guolei19850528/guolei_py3_qywx
=================================================
"""
from datetime import timedelta
from typing import Union, Callable

import diskcache
import redis
import requests
from jsonschema.validators import Draft202012Validator
from requests import Response


class ResponseCallable(object):
    """
    Response Callable
    """

    @staticmethod
    def json_errcode_0(response: Response = None, status_code: int = 200):
        json_data = response.json() if response.status_code == status_code else dict()
        if int(json_data.get("errcode", -1)) == 0:
            return json_data
        return None


class UrlSetting(object):
    CGI_BIN__GETTOKEN = "/cgi-bin/gettoken"
    CGI_BIN__GET_API_DOMAIN_IP = "/cgi-bin/get_api_domain_ip"
    CGI_BIN__MESSAGE__SEND = "/cgi-bin/message/send"
    CGI_BIN__MEDIA__UPLOAD = "/cgi-bin/media/upload"
    CGI_BIN__MEDIA__GET = "/cgi-bin/media/get"
    CGI_BIN__MEDIA__UPLOADIMG = "/cgi-bin/media/uploadimg"


class Api(object):
    """
    @see https://developer.work.weixin.qq.com/document/path/90664
    """

    def __init__(
            self,
            base_url: str = "https://qyapi.weixin.qq.com/",
            corpid: str = "",
            corpsecret: str = "",
            agentid: Union[int, str] = "",
            cache_instance: Union[diskcache.Cache, redis.Redis, redis.StrictRedis] = None,
    ):
        self._base_url = base_url
        self._corpid = corpid
        self._corpsecret = corpsecret
        self._agentid = agentid
        self._cache_instance = cache_instance
        self._access_token = ""

    @property
    def base_url(self):
        return self._base_url[:-1] if self._base_url.endswith("/") else self._base_url

    @base_url.setter
    def base_url(self, base_url):
        self._base_url = base_url

    @property
    def corpid(self):
        return self._corpid

    @corpid.setter
    def corpid(self, corpid):
        self._corpid = corpid

    @property
    def corpsecret(self):
        return self._corpsecret

    @corpsecret.setter
    def corpsecret(self, corpsecret):
        self._corpsecret = corpsecret

    @property
    def agentid(self):
        return self._agentid

    @agentid.setter
    def agentid(self, agentid):
        self._agentid = agentid

    @property
    def cache_instance(self):
        return self._cache_instance

    @cache_instance.setter
    def cache_instance(self, cache_instance):
        self._cache_instance = cache_instance

    def get_access_token_by_cache(self, name: str = None):
        name = name or f"guolei_py3_qywx_server_access_token__{self.corpid}_{self.agentid}"
        if isinstance(self.cache_instance, diskcache.Cache):
            self._access_token = self.cache_instance.get(name)
        if isinstance(self.cache_instance, (redis.Redis, redis.StrictRedis)):
            self._access_token = self.cache_instance.get(name)
        return self._access_token or ""

    def put_access_token_to_cache(
            self,
            name: str = None,
            expire: Union[float, int, timedelta] = None,
            access_token: str = None
    ):
        name = name or f"guolei_py3_qywx_server_access_token__{self.corpid}_{self.agentid}"
        access_token = access_token or self._access_token
        if isinstance(self.cache_instance, diskcache.Cache):
            return self.cache_instance.set(
                key=name,
                value=access_token,
                expire=expire or timedelta(seconds=7100).total_seconds()
            )
        if isinstance(self.cache_instance, (redis.Redis, redis.StrictRedis)):
            self.cache_instance.setex(
                name=name,
                value=access_token,
                time=expire or timedelta(seconds=7100),
            )
            return True
        return False

    def get(self, on_response_callback: Callable = ResponseCallable.json_errcode_0, path: str = None, **kwargs):
        """
        execute get by requests.get

        params.setdefault("access_token", self._access_token)

        :param on_response_callback: response callback
        :param path: if url is None: url=f"{self.base_url}{path}"
        :param kwargs: requests.get(**kwargs)
        :return: on_response_callback(response) or response
        """
        path = kwargs.get("url", None) or f"{self.base_url}{path}"
        params = kwargs.get("params", dict())
        params.setdefault("access_token", self._access_token)
        kwargs.update([
            ("params", params),
            ("url", path),
        ])
        response = requests.get(**kwargs)
        if isinstance(on_response_callback, Callable):
            return on_response_callback(response)
        return response

    def post(self, on_response_callback: Callable = ResponseCallable.json_errcode_0, path: str = None, **kwargs):
        """
        execute post by requests.post

        params.setdefault("access_token", self._access_token)

        :param on_response_callback: response callback
        :param path: if url is None: url=f"{self.base_url}{path}"
        :param kwargs: requests.get(**kwargs)
        :return: on_response_callback(response) or response
        """
        path = kwargs.get("url", None) or f"{self.base_url}{path}"
        params = kwargs.get("params", dict())
        params.setdefault("access_token", self._access_token)
        kwargs.update([
            ("params", params),
            ("url", path),
        ])
        response = requests.post(**kwargs)
        if isinstance(on_response_callback, Callable):
            return on_response_callback(response)
        return response

    def put(self, on_response_callback: Callable = ResponseCallable.json_errcode_0, path: str = None, **kwargs):
        """
        execute put by requests.put

        params.setdefault("access_token", self._access_token)

        :param on_response_callback: response callback
        :param path: if url is None: url=f"{self.base_url}{path}"
        :param kwargs: requests.get(**kwargs)
        :return: on_response_callback(response) or response
        """
        path = kwargs.get("url", None) or f"{self.base_url}{path}"
        params = kwargs.get("params", dict())
        params.setdefault("access_token", self._access_token)
        kwargs.update([
            ("params", params),
            ("url", path),
        ])
        response = requests.put(**kwargs)
        if isinstance(on_response_callback, Callable):
            return on_response_callback(response)
        return response

    def request(self, on_response_callback: Callable = ResponseCallable.json_errcode_0, path: str = None,
                **kwargs):
        """
        execute request by requests.request

        params.setdefault("access_token", self._access_token)

        :param on_response_callback: response callback
        :param path: if url is None: url=f"{self.base_url}{path}"
        :param kwargs: requests.get(**kwargs)
        :return: on_response_callback(response) or response
        """
        path = kwargs.get("url", None) or f"{self.base_url}{path}"
        params = kwargs.get("params", dict())
        params.setdefault("access_token", self._access_token)
        kwargs.update([
            ("params", params),
            ("url", path),
        ])
        response = requests.request(**kwargs)
        if isinstance(on_response_callback, Callable):
            return on_response_callback(response)
        return response

    def access_token(self):
        """
        access token
        :return:
        """
        self._access_token = self.get_access_token_by_cache()
        result = self.get(
            path=f"{UrlSetting.CGI_BIN__GET_API_DOMAIN_IP}",
            verify=False,
            timeout=(60, 60)
        )
        if Draft202012Validator({
            "type": "object",
            "properties": {
                "ip_list": {"type": "array", "minItem": 1},
            },
            "required": ["access_token"]
        }).is_valid(result):
            return self
        result = self.get(
            path=f"{UrlSetting.CGI_BIN__GETTOKEN}",
            params={
                "corpid": self.corpid,
                "corpsecret": self.corpsecret,
            },
            verify=False,
            timeout=(60, 60)
        )
        if Draft202012Validator({
            "type": "object",
            "properties": {
                "access_token": {"type": "string", "minLength": 1},
            },
            "required": ["access_token"]
        }).is_valid(result):
            self._access_token = result.get("access_token", None)
            self.put_access_token_to_cache()
        return self
