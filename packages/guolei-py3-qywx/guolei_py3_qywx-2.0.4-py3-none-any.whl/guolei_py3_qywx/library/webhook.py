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
from typing import Callable, Any
from jsonschema import validate, Draft202012Validator
import requests
from requests import Response


class ResponseCallable(object):
    """
    Response Callable
    """

    @staticmethod
    def json_errcode_0(response: Response = None, status_code: int = 200):
        json_data = response.json() if response.status_code == status_code else dict()
        if int(json_data.get("errcode", -1)) == 0:
            return json_data.get("media_id", True)
        return False


class UrlSetting:
    """
    Urls Settings
    """
    CGI_BIN__WEBHOOK__SEND = "/cgi-bin/webhook/send"
    CGI_BIN__WEBHOOK__UPLOAD_MEDIA = "/cgi-bin/webhook/upload_media"


class Api(object):
    """
    企业微信 群机器人 Webhook Api Class
    @see https://developer.work.weixin.qq.com/document/path/91770
    """

    def __init__(
            self,
            base_url: str = "https://qyapi.weixin.qq.com/",
            key: str = "",
            mentioned_list: list = [],
            mentioned_mobile_list: list = []
    ):
        """
        @see https://developer.work.weixin.qq.com/document/path/91770
        :param base_url: base url
        :param key: key
        :param mentioned_list:
        :param mentioned_mobile_list:
        """
        self._base_url = base_url
        self._key = key
        self._mentioned_list = mentioned_list
        self._mentioned_mobile_list = mentioned_mobile_list

    @property
    def base_url(self):
        return self._base_url[:-1] if self._base_url.endswith("/") else self._base_url

    @base_url.setter
    def base_url(self, base_url):
        self._base_url = base_url

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, key):
        self._key = key

    @property
    def mentioned_list(self):
        return self._mentioned_list

    @mentioned_list.setter
    def mentioned_list(self, mentioned_list):
        self._mentioned_list = mentioned_list

    @property
    def mentioned_mobile_list(self):
        return self._mentioned_mobile_list

    @mentioned_mobile_list.setter
    def mentioned_mobile_list(self, mentioned_mobile_list):
        self._mentioned_mobile_list = mentioned_mobile_list

    def post(self, on_response_callback: Callable = ResponseCallable.json_errcode_0, path: str = None,
             **kwargs):
        """
        execute post by requests.post

        params.setdefault("key", self.key)

        :param on_response_callback: response callback
        :param path: if url is None: url=f"{self.base_url}{path}"
        :param kwargs: requests.get(**kwargs)
        :return: on_response_callback(response) or response
        """
        path = kwargs.get("url", None) or f"{self.base_url}{path}"
        params = kwargs.get("params", dict())
        params.setdefault("key", self.key)
        kwargs.update([
            ("params", params),
            ("url", path),
        ])
        response = requests.post(**kwargs)
        if isinstance(on_response_callback, Callable):
            return on_response_callback(response)
        return response

    def request(self, on_response_callback: Callable = ResponseCallable.json_errcode_0, path: str = None,
                **kwargs):
        """
        execute request by requests.request

        params.setdefault("key", self.key)

        :param on_response_callback: response callback
        :param path: if url is None: url=f"{self.base_url}{path}"
        :param kwargs: requests.get(**kwargs)
        :return: on_response_callback(response) or response
        """
        path = kwargs.get("url", None) or f"{self.base_url}{path}"
        params = kwargs.get("params", dict())
        params.setdefault("key", self.key)
        kwargs.update([
            ("params", params),
            ("url", path),
        ])
        response = requests.request(**kwargs)
        if isinstance(on_response_callback, Callable):
            return on_response_callback(response)
        return response

    def send_text(self, content: str = None, mentioned_list: list[str] = [], mentioned_mobile_list: list[str] = []):
        """
        @see https://developer.work.weixin.qq.com/document/path/91770#%E6%96%87%E6%9C%AC%E7%B1%BB%E5%9E%8B
        :param content:
        :param mentioned_list:
        :param mentioned_mobile_list:
        :return:
        """
        return self.post(
            path=UrlSetting.CGI_BIN__WEBHOOK__SEND,
            json={
                "msgtype": "text",
                "text": {
                    "content": f"{content}",
                    "mentioned_list": self.mentioned_list + mentioned_list,
                    "mentioned_mobile_list": self.mentioned_mobile_list + mentioned_mobile_list,
                }
            }
        )

    def send_markdown(self, content: str = None):
        """
        @see https://developer.work.weixin.qq.com/document/path/91770#markdown%E7%B1%BB%E5%9E%8B
        :param content:
        :return:
        """
        return self.post(
            path=UrlSetting.CGI_BIN__WEBHOOK__SEND,
            json={
                "msgtype": "markdown",
                "markdown": {
                    "content": ""
                }
            }
        )

    def send_file(self, media_id: str = None):
        """
        @see https://developer.work.weixin.qq.com/document/path/91770#%E6%96%87%E4%BB%B6%E7%B1%BB%E5%9E%8B
        :param media_id:
        :return:
        """
        return self.post(
            path=UrlSetting.CGI_BIN__WEBHOOK__SEND,
            json={
                "msgtype": "file",
                "file": {
                    "media_id": f"{media_id}"
                }
            }
        )

    def send_voice(self, media_id: str = None):
        """
        @see https://developer.work.weixin.qq.com/document/path/91770#%E8%AF%AD%E9%9F%B3%E7%B1%BB%E5%9E%8B
        :param media_id:
        :return:
        """
        return self.post(
            path=UrlSetting.CGI_BIN__WEBHOOK__SEND,
            json={
                "msgtype": "voice",
                "voice": {
                    "media_id": f"{media_id}"
                }
            }
        )

    def upload_media(self, types: str = "file", files: Any = None):
        """
        @see https://developer.work.weixin.qq.com/document/path/91770#%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0%E6%8E%A5%E5%8F%A3
        :param types:
        :param files:
        :return:
        """
        params = dict()
        params.setdefault("type", types)
        return self.post(
            path=UrlSetting.CGI_BIN__WEBHOOK__UPLOAD_MEDIA,
            params=params,
            files=files
        )
