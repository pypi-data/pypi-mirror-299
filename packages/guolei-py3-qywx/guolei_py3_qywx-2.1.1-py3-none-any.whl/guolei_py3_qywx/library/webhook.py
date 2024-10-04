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

from guolei_py3_requests.library import ResponseCallback, Request
from jsonschema import validate, Draft202012Validator
import requests
from requests import Response


class ResponseCallback(ResponseCallback):
    """
    Response Callable
    """

    @staticmethod
    def json_errcode_0(response: Response = None, status_code: int = 200):
        json_addict = ResponseCallback.json_addict(response=response, status_code=status_code)
        if Draft202012Validator({
            "type": "object",
            "properties": {
                "errcode": {
                    "oneOf": [
                        {"type": "integer", "const": 0},
                        {"type": "string", "const": "0"},
                    ]
                }
            },
            "required": ["errcode"],
        }).is_valid(json_addict):
            return json_addict.get("media_id", True)
        return False


class UrlSetting:
    """
    Urls Settings
    """
    CGI_BIN__WEBHOOK__SEND = "/cgi-bin/webhook/send"
    CGI_BIN__WEBHOOK__UPLOAD_MEDIA = "/cgi-bin/webhook/upload_media"


class Api(Request):
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
        super().__init__()
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

    def send_text(
            self,
            content: str = None,
            mentioned_list: list[str] = [],
            mentioned_mobile_list: list[str] = []
    ):
        """
        @see https://developer.work.weixin.qq.com/document/path/91770#%E6%96%87%E6%9C%AC%E7%B1%BB%E5%9E%8B
        :param content:
        :param mentioned_list:
        :param mentioned_mobile_list:
        :return:
        """
        return self.post(
            on_response_callback=ResponseCallback.json_errcode_0,
            url=f"{self.base_url}{UrlSetting.CGI_BIN__WEBHOOK__SEND}",
            params={
                "key": self.key
            },
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
            on_response_callback=ResponseCallback.json_errcode_0,
            url=f"{self.base_url}{UrlSetting.CGI_BIN__WEBHOOK__SEND}",
            params={
                "key": self.key
            },
            json={
                "msgtype": "markdown",
                "markdown": {
                    "content": content
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
            on_response_callback=ResponseCallback.json_errcode_0,
            url=f"{self.base_url}{UrlSetting.CGI_BIN__WEBHOOK__SEND}",
            params={
                "key": self.key
            },
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
            on_response_callback=ResponseCallback.json_errcode_0,
            url=f"{self.base_url}{UrlSetting.CGI_BIN__WEBHOOK__SEND}",
            params={
                "key": self.key
            },
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
        return self.post(
            on_response_callback=ResponseCallback.json_errcode_0,
            url=f"{self.base_url}{UrlSetting.CGI_BIN__WEBHOOK__UPLOAD_MEDIA}",
            params={
                "key": self.key,
                "type": types,
            },
            files=files
        )
