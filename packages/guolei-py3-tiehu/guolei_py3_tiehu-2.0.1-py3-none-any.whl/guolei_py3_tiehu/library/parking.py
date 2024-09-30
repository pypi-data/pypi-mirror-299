#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
=================================================
作者：[郭磊]
手机：[15210720528]
Email：[174000902@qq.com]
Github：https://github.com/guolei19850528/guolei_py3_tiehu
=================================================
"""
import hashlib
import json
from datetime import datetime
from typing import Callable

import requests
from requests import Response


class ResponseCallable(object):
    """
    Response Callable
    """

    @staticmethod
    def json_addict_status_1_data(response: Response = None, status_code: int = 200):
        json_data = response.json() if response.status_code == status_code else dict()
        if int(json_data.get("status", -1)) == 1:
            return json.loads(json_data.get("Data", ""))
        return None


class UrlSetting(object):
    CXZN__INTERFACE__QUERYPKLOT = "/cxzn/interface/queryPklot"
    CXZN__INTERFACE__GETPARKCARTYPE = "/cxzn/interface/getParkCarType"
    CXZN__INTERFACE__GETPARKCARMODEL = "/cxzn/interface/getParkCarModel"
    CXZN__INTERFACE__PAYMONTHLY = "/cxzn/interface/payMonthly"
    CXZN__INTERFACE__ADDVISIT = "/cxzn/interface/addVisit"
    CXZN__INTERFACE__LOCKCAR = "/cxzn/interface/lockCar"
    CXZN__INTERFACE__GETPARKINFO = "/cxzn/interface/getParkinfo"
    CXZN__INTERFACE__ADDPARKBLACK = "/cxzn/interface/addParkBlack"
    CXZN__INTERFACE__DELPARKBLACKLIST = "/cxzn/interface/delParkBlacklist"
    CXZN__INTERFACE__GETPARKGATE = "/cxzn/interface/getParkGate"
    CXZN__INTERFACE__OPENGATE = "/cxzn/interface/openGate"
    CXZN__INTERFACE__SAVEMONTHLYRENT = "/cxzn/interface/saveMonthlyRent"
    CXZN__INTERFACE__DELMONTHLYRENT = "/cxzn/interface/delMonthlyRent"
    CXZN__INTERFACE__GETMONTHLYRENT = "/cxzn/interface/getMonthlyRent"
    CXZN__INTERFACE__GETMONTHLYRENTLIST = "/cxzn/interface/getMonthlyRentList"
    CXZN__INTERFACE__DELMONTHLYRENTLIST = "/cxzn/interface/delMonthlyRentList"
    CXZN__INTERFACE__GETPARKDEVICESTATE = "/cxzn/interface/getParkDeviceState"
    CXZN__INTERFACE__UPATEPLATEINFO = "/cxzn/interface/upatePlateInfo"
    CXZN__INTERFACE__GETPARKBLACKLIST = "/cxzn/interface/getParkBlackList"
    CXZN__INTERFACE__DELETEVISITT = "/cxzn/interface/deleteVisit"


class Api(object):
    def __init__(
            self,
            base_url: str = "",
            parking_id: str = "",
            app_key: str = ""
    ):
        self._base_url = base_url
        self._parking_id = parking_id
        self._app_key = app_key

    @property
    def base_url(self):
        return self._base_url[:-1] if self._base_url.endswith("/") else self._base_url

    @base_url.setter
    def base_url(self, value):
        self._base_url = value

    @property
    def parking_id(self):
        return self._parking_id

    @parking_id.setter
    def parking_id(self, value):
        self._parking_id = value

    @property
    def app_key(self):
        return self._app_key

    @app_key.setter
    def app_key(self, value):
        self._app_key = value

    def signature(
            self,
            data: dict = None,
    ):
        temp_string = ""
        data = data or dict()
        if data.keys():
            data_sorted = sorted(data.keys())
            if isinstance(data_sorted, list):
                temp_string = "&".join([
                    f"{i}={data[i]}"
                    for i in
                    data_sorted if
                    i != "appKey"
                ]) + f"{hashlib.md5(self.app_key.encode('utf-8')).hexdigest().upper()}"
        return hashlib.md5(temp_string.encode('utf-8')).hexdigest().upper()

    def get(self, on_response_callback: Callable = ResponseCallable.json_addict_status_1_data, path: str = None,
            **kwargs):
        """
        execute get by requests.get

        headers.setdefault("Token", self.token_data.get("token", ""))

        headers.setdefault("Companycode", self.token_data.get("companyCode", ""))

        :param on_response_callback: response callback
        :param path: if url is None: url=f"{self.base_url}{path}"
        :param kwargs: requests.get(**kwargs)
        :return: on_response_callback(response) or response
        """
        path = kwargs.get("url", None) or f"{self.base_url}{path}"
        kwargs.update([
            ("url", path),
        ])
        response = requests.get(**kwargs)
        if isinstance(on_response_callback, Callable):
            return on_response_callback(response)
        return response

    def post(self, on_response_callback: Callable = ResponseCallable.json_addict_status_1_data, path: str = None,
             **kwargs):
        """
        execute post by requests.post

        headers.setdefault("Token", self.token_data.get("token", ""))

        headers.setdefault("Companycode", self.token_data.get("companyCode", ""))

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

    def put(self, on_response_callback: Callable = ResponseCallable.json_addict_status_1_data, path: str = None,
            **kwargs):
        """
        execute put by requests.put

        headers.setdefault("Token", self.token_data.get("token", ""))

        headers.setdefault("Companycode", self.token_data.get("companyCode", ""))

        :param on_response_callback: response callback
        :param path: if url is None: url=f"{self.base_url}{path}"
        :param kwargs: requests.get(**kwargs)
        :return: on_response_callback(response) or response
        """
        path = kwargs.get("url", None) or f"{self.base_url}{path}"
        kwargs.update([
            ("url", path),
        ])
        response = requests.put(**kwargs)
        if isinstance(on_response_callback, Callable):
            return on_response_callback(response)
        return response

    def request(self, on_response_callback: Callable = ResponseCallable.json_addict_status_1_data, path: str = None,
                **kwargs):
        """
        execute request by requests.request

        headers.setdefault("Token", self.token_data.get("token", ""))

        headers.setdefault("Companycode", self.token_data.get("companyCode", ""))

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

    def post_json(self, on_response_callback: Callable = ResponseCallable.json_addict_status_1_data, path: str = None,
                  **kwargs):
        """
        execute post by requests.post

        headers.setdefault("Token", self.token_data.get("token", ""))

        headers.setdefault("Companycode", self.token_data.get("companyCode", ""))

        :param on_response_callback: response callback
        :param path: if url is None: url=f"{self.base_url}{path}"
        :param kwargs: requests.get(**kwargs)
        :return: on_response_callback(response) or response
        """
        path = kwargs.get("url", None) or f"{self.base_url}{path}"
        json = kwargs.get("json", dict())
        json.setdefault("parkingId", self.parking_id)
        json.setdefault("timestamp", int(datetime.now().timestamp()))
        json.setdefault("sign", self.signature(json))
        kwargs.update([
            ("json", json),
            ("url", path),
        ])
        response = requests.post(**kwargs)
        if isinstance(on_response_callback, Callable):
            return on_response_callback(response)
        return response
