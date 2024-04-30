#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations
import requests
import json
from typing import Optional, List
from dataclasses import dataclass, asdict, field
from api.api import APIinterface
from config import DATA_PATH

from .req import _BnnApiRequestParams, _BnnResPage
from .res import _OrganizationData

BNN_DATA_PATH = DATA_PATH.joinpath("bnn")

HTTP = "http://"
HTTPS = "https://"
BASE_API_URL = "data.brreg.no/enhetsregisteret/api"

FORMAT = "JSON"  # JSON or XML


class BNN(APIinterface):
    def __init__(self) -> None:
        self._search_data = None
        self._search_link: str | None = None
        self._search_meta: _BnnResPage | None = None
        self._seach_url: str = f"{HTTPS}{BASE_API_URL}/enheter"
        self._search_header: dict[str, str] = {
            "Accept": "application/json;charset=UTF-8",
        }

    @property
    def search_data(self) -> list[dict]:
        return self._search_data if self._search_data is not None else []

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
            params=params.to_dict(),
            allow_redirects=False,
        )

        # handle respone, raise error if status code is not 200
        req.raise_for_status()

        # update internal state
        data: dict = req.json()
        self._search_data = data.get("_embedded", {}).get("enheter", [])
        self._search_meta = _BnnResPage(**data.get("page", None))
        self._search_link = data.get("_links", {}).get("self", {}).get("href", None)

        return self._search_data

    def _search_paginate(self):
        if self._search_link is None or self._search_meta is None:
            raise ValueError("No search data available, perform a query/search first.")
        elif self._search_meta.number + 1 >= self._search_meta.totalPages:
            raise IndexError("No more pages to fetch.")
        self._search_meta.number += 1

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
