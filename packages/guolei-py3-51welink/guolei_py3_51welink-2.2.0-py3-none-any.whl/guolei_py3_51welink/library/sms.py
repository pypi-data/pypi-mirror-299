#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
=================================================
作者：[郭磊]
手机：[15210720528]
Email：[174000902@qq.com]
Github：https://github.com/guolei19850528/guolei_py3_51welink
=================================================
"""

import hashlib
import random
import string
from datetime import datetime
from typing import Callable

import requests
from addict import Dict
from guolei_py3_requests.library import ResponseCallback, Request
from jsonschema.validators import Draft202012Validator
from requests import Response


class ResponseCallback(ResponseCallback):
    """
    Response Callback
    """

    @staticmethod
    def json_result_succ(response: Response = None, status_code: int = 200):
        json_addict = ResponseCallback.json_addict(response=response, status_code=status_code)
        return Draft202012Validator({
            "type": "object",
            "properties": {
                "Result": {"type": "string", "const": "succ"},
            },
            "required": ["Result"]
        }).is_valid(json_addict)


class UrlSetting(object):
    ENCRYPTIONSUBMIT_SENDSMS = "/EncryptionSubmit/SendSms.ashx"


class Api(Request):
    """
    微网通联短息API Class

    @see https://www.lmobile.cn/ApiPages/index.html
    """

    def __init__(
            self,
            base_url: str = "https://api.51welink.com/",
            account_id: str = "",
            password: str = "",
            product_id: int = 0,
            smms_encrypt_key: str = "SMmsEncryptKey",
    ):
        self._base_url = base_url
        self._account_id = account_id
        self._password = password
        self._product_id = product_id
        self._smms_encrypt_key = smms_encrypt_key

    @property
    def base_url(self):
        return self._base_url[:-1] if self._base_url.endswith("/") else self._base_url

    @base_url.setter
    def base_url(self, base_url):
        self._base_url = base_url

    @property
    def account_id(self):
        return self._account_id

    @account_id.setter
    def account_id(self, account_id):
        self._account_id = account_id

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = password

    @property
    def product_id(self):
        return self._product_id

    @product_id.setter
    def product_id(self, product_id):
        self._product_id = product_id

    @property
    def smms_encrypt_key(self):
        return self._smms_encrypt_key

    @smms_encrypt_key.setter
    def smms_encrypt_key(self, smms_encrypt_key):
        self._smms_encrypt_key = smms_encrypt_key

    def timestamp(self):
        return int(datetime.now().timestamp())

    def random_digits(self, length=10):
        return int("".join(random.sample(string.digits, length)))

    def password_md5(self):
        return hashlib.md5(f"{self.password}{self.smms_encrypt_key}".encode('utf-8')).hexdigest()

    def sha256_signature(self, data: dict = {}):
        data = data or dict()
        data.setdefault("AccountId", self.account_id)
        data.setdefault("Timestamp", self.timestamp())
        data.setdefault("Random", self.random_digits())
        data.setdefault("ProductId", self.product_id)
        data.setdefault("PhoneNos", "")
        data.setdefault("Content", "")
        temp_string = "&".join([
            f"AccountId={data.get("AccountId", "")}",
            f"PhoneNos={str(data.get("PhoneNos", "")).split(",")[0]}",
            f"Password={self.password_md5().upper()}",
            f"Random={data.get('Random', "")}",
            f"Timestamp={data.get('Timestamp', "")}",
        ])
        return hashlib.sha256(temp_string.encode("utf-8")).hexdigest()

    def send_sms(
            self,
            phone_nos: str = None,
            content: str = None,
    ):
        """
        发送短信

        @see https://www.lmobile.cn/ApiPages/index.html
        :param phone_nos: 接收号码间用英文半角逗号“,”隔开，触发产品一次只能提交一个,其他产品一次不能超过10万个号码
        :param content: 短信内容：不超过1000字符
        :return:
        """
        data = dict()
        data.setdefault("AccountId", self.account_id)
        data.setdefault("Timestamp", self.timestamp())
        data.setdefault("Random", self.random_digits())
        data.setdefault("ProductId", self.product_id)
        data.setdefault("PhoneNos", phone_nos)
        data.setdefault("Content", content)
        data.setdefault("AccessKey", self.sha256_signature(data))
        return self.post(
            on_response_callback=ResponseCallback.json_result_succ,
            url=f"{self.base_url}{UrlSetting.ENCRYPTIONSUBMIT_SENDSMS}",
            json=data
        )
