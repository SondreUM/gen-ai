#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations
import json
from typing import Optional, List
from dataclasses import dataclass, asdict, field


@dataclass
class _BrregApiRequestParams:
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
    size: int = 2
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
    def deserialize(data: str) -> _BrregApiRequestParams:
        return _BrregApiRequestParams(**json.loads(data))


@dataclass
class _BrregResPage:
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
    def deserialize(data: str) -> _BrregResPage:
        return _BrregResPage(**json.loads(data))
