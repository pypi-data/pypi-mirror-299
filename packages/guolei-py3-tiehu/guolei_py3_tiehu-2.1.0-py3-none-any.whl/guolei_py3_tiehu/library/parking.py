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
from addict import Dict
from guolei_py3_requests.library import ResponseCallback, Request
from jsonschema.validators import Draft202012Validator
from requests import Response


class ResponseCallback(ResponseCallback):
    """
    Response Callable
    """

    @staticmethod
    def json_addict_status_1_data(response: Response = None, status_code: int = 200):
        json_addict = ResponseCallback.json_addict(response=response, status_code=status_code)
        if Draft202012Validator({
            "type": "object",
            "properties": {
                "status": {
                    "oneOf": [
                        {"type": "integer", "const": 1},
                        {"type": "string", "const": "1"},
                    ]
                },
            },
            "required": ["status", "Data"]
        }).is_valid(json_addict):
            return json.loads(json_addict.get("Data", ""))
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


class Api(Request):
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

    def post(self, on_response_callback: Callable = ResponseCallback.json_addict_status_1_data, path: str = None,
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
        kwargs = Dict(kwargs)
        url = f"{self.base_url}{path}"
        kwargs.json = Dict({
            **{
                "parkingId": self.parking_id,
                "timestamp": int(datetime.now().timestamp()),
                "sign": self.signature({
                    "parkingId": self.parking_id,
                    "timestamp": int(datetime.now().timestamp()),
                })
            },
            **kwargs.json
        })
        return super().post(on_response_callback=on_response_callback, url=url, **kwargs.to_dict())
