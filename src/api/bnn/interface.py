#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations
import requests
import json
from typing import Optional, List
from dataclasses import dataclass, asdict, field
from api.api import APIinterface
from config import DATA_PATH

BNN_DATA_PATH = DATA_PATH.joinpath("bnn")

HTTP = "http://"
HTTPS = "https://"
BASE_API_URL = "data.brreg.no/enhetsregisteret/api"

FORMAT = "JSON"  # JSON or XML


@dataclass
class _BnnApiRequestParams:
    """Dataclass for request parameters
    ref: https://data.brreg.no/enhetsregisteret/api/docs/index.html#enheter-sok
    """

    navn: Optional[str] = field(default=None)
    organisasjonsnummer: Optional[str] = None
    overordnetEnhet: Optional[str] = None
    fraAntallAnsatte: Optional[int] = field(default=None)
    tilAntallAnsatte: Optional[int] = field(default=None)
    konkurs: Optional[bool] = None
    registrertIMvaregisteret: Optional[bool] = None
    registrertIForetaksregisteret: Optional[bool] = None
    registrertIStiftelsesregisteret: Optional[bool] = None
    registrertIFrivillighetsregisteret: Optional[bool] = None
    frivilligRegistrertIMvaregisteret: Optional[str] = None
    underTvangsavviklingEllerTvangsopplosning: Optional[bool] = None
    underAvvikling: Optional[bool] = None
    fraRegistreringsdatoEnhetsregisteret: Optional[str] = None
    tilRegistreringsdatoEnhetsregisteret: Optional[str] = None
    fraStiftelsesdato: Optional[str] = None
    tilStiftelsesdato: Optional[str] = None
    organisasjonsform: Optional[str] = None
    hjemmeside: Optional[str] = None
    institusjonellSektorkode: Optional[str] = None
    postadresse_kommunenummer: Optional[str] = None
    postadresse_postnummer: Optional[str] = None
    postadresse_poststed: Optional[str] = None
    postadresse_landkode: Optional[str] = None
    postadresse_adresse: Optional[str] = None
    kommunenummer: Optional[str] = None
    forretningsadresse_kommunenummer: Optional[str] = None
    forretningsadresse_postnummer: Optional[str] = None
    forretningsadresse_poststed: Optional[str] = None
    forretningsadresse_landkode: Optional[str] = None
    forretningsadresse_adresse: Optional[str] = None
    naeringskode: Optional[List[str]] = None
    sisteInnsendteAarsregnskap: Optional[str] = None
    sort: Optional[str] = None
    size: int = 20
    page: int = 0

    def __post_init__(self):
        assert self.size > 0, "Query size must be greater than 0"
        assert (
            self.size * (self.page + 1) <= 10000
        ), "Query size must be less than or equal to 10000"

    def to_dict(self) -> dict:
        new: dict[str, str | None] = {}
        for k, v in self.__dict__.items():
            if v is not None:
                new[k.replace("_", ".")] = v
        return new

    def serialize(self) -> str:
        return json.dumps(self.to_dict())

    @staticmethod
    def deserialize(data: str) -> _BnnApiRequestParams:
        return _BnnApiRequestParams(**json.loads(data))


@dataclass
class _BnnResPage:
    """Dataclass for response page
    ref: https://data.brreg.no/enhetsregisteret/api/docs/index.html#enheter-sok
    """

    totalElements: int
    totalPages: int
    size: int
    number: int

    def to_dict(self) -> dict:
        return asdict(self)

    def serialize(self) -> str:
        return json.dumps(self.to_dict())

    @staticmethod
    def deserialize(data: str) -> _BnnResPage:
        return _BnnResPage(**json.loads(data))


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
