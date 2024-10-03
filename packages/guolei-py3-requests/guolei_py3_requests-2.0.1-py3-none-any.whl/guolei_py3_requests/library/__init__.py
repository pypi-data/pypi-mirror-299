#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from typing import Callable, Sequence, Union

import requests
from addict import Dict
from bs4 import BeautifulSoup
from requests import Response


class ResponseCallback(object):
    """
    Response Callback
    """
    @staticmethod
    def text(response: Response, status_code: int = 200):
        """
        response text
        :param response:
        :param status_code:
        :return:
        """
        if isinstance(response, Response) and response.status_code == status_code:
            return response.text
        return None

    def text_to_beautifulsoup(self, response: Response, status_code: int = 200,
                              features: Union[str, Sequence[str]] = None):
        """
        response text to beautifulsoup
        :param response:
        :param status_code:
        :param features:
        :return:
        """
        return BeautifulSoup(
            response.text,
            features=features
        )

    @staticmethod
    def json(response: Response, status_code: int = 200):
        """
        response.json()
        :param response:
        :param status_code:
        :return:
        """
        if isinstance(response, Response) and response.status_code == status_code:
            return response.json()
        return None

    @staticmethod
    def json_addict(response: Response, status_code: int = 200):
        """
        Dict(response.json())
        :param response:
        :param status_code:
        :return:
        """
        if isinstance(response, Response) and response.status_code == status_code:
            return Dict(response.json())
        return None


class Request(object):
    def __init__(self):
        pass

    def get(self, on_response_callback: Callable = None, *args, **kwargs):
        response = requests.get(*args, **kwargs)
        if isinstance(on_response_callback, Callable):
            return on_response_callback(response)
        return response

    def post(self, on_response_callback: Callable = None, *args, **kwargs):
        response = requests.post(*args, **kwargs)
        if isinstance(on_response_callback, Callable):
            return on_response_callback(response)
        return response

    def put(self, on_response_callback: Callable = None, *args, **kwargs):
        response = requests.put(*args, **kwargs)
        if isinstance(on_response_callback, Callable):
            return on_response_callback(response)
        return response

    def delete(self, on_response_callback: Callable = None, *args, **kwargs):
        response = requests.delete(*args, **kwargs)
        if isinstance(on_response_callback, Callable):
            return on_response_callback(response)
        return response

    def options(self, on_response_callback: Callable = None, *args, **kwargs):
        response = requests.options(*args, **kwargs)
        if isinstance(on_response_callback, Callable):
            return on_response_callback(response)
        return response

    def patch(self, on_response_callback: Callable = None, *args, **kwargs):
        response = requests.patch(*args, **kwargs)
        if isinstance(on_response_callback, Callable):
            return on_response_callback(response)
        return response

    def head(self, on_response_callback: Callable = None, *args, **kwargs):
        response = requests.head(*args, **kwargs)
        if isinstance(on_response_callback, Callable):
            return on_response_callback(response)
        return response

    def request(self, on_response_callback: Callable = None, *args, **kwargs):
        response = requests.request(*args, **kwargs)
        if isinstance(on_response_callback, Callable):
            return on_response_callback(response)
        return response
