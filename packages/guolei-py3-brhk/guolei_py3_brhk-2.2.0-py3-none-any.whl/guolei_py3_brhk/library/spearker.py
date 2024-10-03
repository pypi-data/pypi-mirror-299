#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
=================================================
作者：[郭磊]
手机：[15210720528]
Email：[174000902@qq.com]
Github：https://github.com/guolei19850528/guolei_py3_brhk
=================================================
"""
from typing import Callable

import requests
from guolei_py3_requests.library import ResponseCallback, Request
from jsonschema.validators import Draft202012Validator
from requests import Response


class ResponseCallback(ResponseCallback):
    """
    Response Callable Class
    """

    @staticmethod
    def json_errcode_0(response: Response = None, status_code: int = 200):
        json_addict = ResponseCallback.json_addict(response=response, status_code=status_code)
        return Draft202012Validator({
            "type": "object",
            "properties": {
                "errcode": {
                    "oneOf": [
                        {"type": "integer", "const": 0},
                        {"type": "string", "const": "0"},
                    ]
                }
            },
            "required": ["errcode"]
        }).is_valid(json_addict)


class UrlSetting(object):
    NOTIFY = "/notify.php"


class Api(Request):
    """
    博瑞皓科 Speaker Api Class
    @see https://www.yuque.com/lingdutuandui/ugcpag/umbzsd#yG8IS
    """

    def __init__(
            self,
            base_url: str = "https://speaker.17laimai.cn/",
            token: str = "",
            id: str = "",
            version: str = "1"
    ):
        """
        @see https://www.yuque.com/lingdutuandui/ugcpag/umbzsd
        :param base_url:
        :param token:
        :param id:
        :param version:
        """
        self._base_url = base_url
        self._token = token
        self._id = id
        self._version = version

    @property
    def base_url(self):
        """
        base url
        :return:
        """
        return self._base_url[:-1] if self._base_url.endswith("/") else self._base_url

    @base_url.setter
    def base_url(self, value):
        self._base_url = value

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, value):
        self._token = value

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, value):
        self._version = value

    def notify(
            self,
            message: str = None,
    ):
        """
        notify

        @see https://www.yuque.com/lingdutuandui/ugcpag/umbzsd#yG8IS
        :param message:
        :return:
        """
        data = dict()
        data.setdefault("token", self.token)
        data.setdefault("id", self.id)
        data.setdefault("version", self.version)
        data.setdefault("message", message)
        return self.post(
            on_response_callback=ResponseCallback.json_errcode_0,
            url=f"{self.base_url}{UrlSetting.NOTIFY}",
            data=data
        )
