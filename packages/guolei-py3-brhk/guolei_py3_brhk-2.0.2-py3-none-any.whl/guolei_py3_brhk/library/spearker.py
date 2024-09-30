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
from requests import Response


class ResponseCallable(object):
    """
    Response Callable Class
    """

    @staticmethod
    def json_errcode_0(response: Response = None, status_code: int = 200):
        json_data = response.json() if response.status_code == status_code else dict()
        if int(json_data.get("errcode", -1)) == 0:
            return True
        return False


class UrlSetting(object):
    NOTIFY = "/notify.php"


class Api(object):
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

    def post(self, on_response_callback: Callable = ResponseCallable.json_errcode_0, path: str = None, **kwargs):
        """
        execute post by requests.post

        :param on_response_callback: response callback
        :param path: if url is None: url=f"{self.base_url}{path}"
        :param kwargs: requests.get(**kwargs)
        :return: on_response_callback(response) or response
        """
        path = kwargs.get("url", None) or f"{self.base_url}{path}"
        kwargs.update([
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

        :param on_response_callback: response callback
        :param path: if url is None: url=f"{self.base_url}{path}"
        :param kwargs: requests.get(**kwargs)
        :return: on_response_callback(response) or response
        """
        path = kwargs.get("url", None) or f"{self.base_url}{path}"
        kwargs.update([
            ("url", path),
        ])
        response = requests.request(**kwargs)
        if isinstance(on_response_callback, Callable):
            return on_response_callback(response)
        return response

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
            path=UrlSetting.NOTIFY,
            data=data
        )
