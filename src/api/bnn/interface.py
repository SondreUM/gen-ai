#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations
import requests
import json
from typing import Optional, List
from dataclasses import dataclass, asdict, field
from api.api import APIinterface

from config import DATA_PATH
from api.bnn.req import _BnnApiRequestParams, _BnnResPage
from api.bnn.res import _OrganizationData, _BnnResLinks as _BnnResLink


HTTP = "http://"
HTTPS = "https://"
BASE_API_URL = "data.brreg.no/enhetsregisteret/api"
BNN_DATA_PATH = DATA_PATH.joinpath("bnn")

FORMAT = "JSON"  # JSON or XML


def write2file(data: str | bytes, file_name: str) -> None:
    """Write data to the api data path"""
    if isinstance(data, str):
        data = data.encode("utf-8")
    with open(BNN_DATA_PATH.joinpath(file_name), "wb") as f:
        f.write(data)


class BNN(APIinterface):
    def __init__(self) -> None:
        self._search_data: list = []
        self._search_link: _BnnResLink | None = None
        self._search_meta: _BnnResPage | None = None
        self._seach_url: str = f"{HTTPS}{BASE_API_URL}/enheter"
        self._search_header: dict[str, str] = {
            "Accept": "application/json;charset=UTF-8",
        }

    @property
    def search_data(self) -> list[dict]:
        return self._search_data

    def _res_parse(self, data: dict) -> None:
        self._search_data = data.get("_embedded", {}).get("enheter", [])
        self._search_meta = _BnnResPage(**data.get("page", None))
        self._search_link = _BnnResLink.res_parse(data.get("_links", {}))

    def search(self, query: str | None, **kwargs) -> list[dict]:
        """implements the search method for the BNN API

        Args:
            query (str | None): The search query

        Returns:
            list[dict]: The search results
        """
        # create request
        params = _BnnApiRequestParams(navn=query, **kwargs)

        req = requests.get(
            url=self._seach_url,
            params=params.to_dict() if params is not None else None,
            allow_redirects=False,
        )

        # handle respone, raise error if status code is not 200
        req.raise_for_status()

        # update internal state
        try:
            data: dict = req.json()
            self._res_parse(data)
        except json.JSONDecodeError:
            # bad response
            raise ValueError("Bad response from server")
        except Exception as e:
            print(e)

        return self._search_data

    def search_paginate(self):
        if self._search_link is None or self._search_meta is None:
            raise ValueError("No search data available, perform a query/search first.")
        elif self._search_link.next is None:
            raise ValueError("No next page available")

        self._seach_url = self._search_link.next
        if self._search_link.next == self._search_link.last:
            self._search_link.last = None
        return self.search(None)

    def get(self, id: int) -> dict:
        if self._search_data is None:
            raise ValueError("No search data available, perform a query/search first.")
        return self._search_data[id]

    @staticmethod
    def get_org(org_nr: str) -> dict:
        res = requests.get(
            f"{HTTPS}{BASE_API_URL}/enheter/{org_nr.strip().replace(' ', '')}",
            headers={"Accept": "application/json;charset=UTF-8"},
        )
        res.raise_for_status()
        return res.json()

    def serialize(self) -> str:
        return json.dumps(self.__dict__)

    @staticmethod
    def deserialize(data: str) -> BNN:
        return BNN(**json.loads(data))
