#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations
import json
from dataclasses import dataclass, asdict
from typing import List, Optional, Dict, Any


@dataclass
class _OrganizationData:
    # Organization Details
    organisasjonsnummer: str
    navn: str
    organisasjonsform: Dict[str, Any]
    hjemmeside: Optional[str]
    postadresse: Dict[str, Any]
    registreringsdatoEnhetsregisteret: Optional[str]
    registrertIMvaregisteret: Optional[bool]
    frivilligMvaRegistrertBeskrivelser: Optional[List[str]]
    naeringskode1: Optional[Dict[str, str]]
    naeringskode2: Optional[Dict[str, str]]
    naeringskode3: Optional[Dict[str, str]]
    hjelpeenhetskode: Optional[Dict[str, str]]
    antallAnsatte: Optional[int]
    harRegistrertAntallAnsatte: Optional[bool]
    overordnetEnhet: Optional[str]
    forretningsadresse: Optional[Dict[str, Any]]
    stiftelsesdato: Optional[str]
    institusjonellSektorkode: Optional[Dict[str, str]]
    registrertIForetaksregisteret: Optional[bool]
    registrertIStiftelsesregisteret: Optional[bool]
    registrertIFrivillighetsregisteret: Optional[bool]
    sisteInnsendteAarsregnskap: Optional[str]
    konkurs: Optional[bool]
    konkursdato: Optional[str]
    underAvvikling: Optional[bool]
    underAvviklingDato: Optional[str]
    underTvangsavviklingEllerTvangsopplosning: Optional[bool]
    tvangsavvikletPgaManglendeSlettingDato: Optional[str]
    tvangsopplostPgaManglendeDagligLederDato: Optional[str]
    tvangsopplostPgaManglendeRevisorDato: Optional[str]
    tvangsopplostPgaManglendeRegnskapDato: Optional[str]
    tvangsopplostPgaMangelfulltStyreDato: Optional[str]
    maalform: Optional[str]
    vedtektsdato: Optional[str]
    vedtektsfestetFormaal: Optional[List[str]]
    aktivitet: Optional[List[str]]
    href: Optional[str]

    @classmethod
    def deserialize(cls, data: dict) -> _OrganizationData:
        return cls(
            organisasjonsnummer=data.get("organisasjonsnummer", None),
            navn=data.get("navn", None),
            organisasjonsform=data.get("organisasjonsform", None),
            hjemmeside=data.get("hjemmeside", None),
            postadresse=data.get("postadresse", None),
            registreringsdatoEnhetsregisteret=data.get("registreringsdatoEnhetsregisteret", None),
            registrertIMvaregisteret=data.get("registrertIMvaregisteret", None),
            frivilligMvaRegistrertBeskrivelser=data.get("frivilligMvaRegistrertBeskrivelser", None),
            naeringskode1=data.get("naeringskode1", None),
            naeringskode2=data.get("naeringskode2", None),
            naeringskode3=data.get("naeringskode3", None),
            hjelpeenhetskode=data.get("hjelpeenhetskode", None),
            antallAnsatte=data.get("antallAnsatte", None),
            harRegistrertAntallAnsatte=data.get("harRegistrertAntallAnsatte", None),
            overordnetEnhet=data.get("overordnetEnhet", None),
            forretningsadresse=data.get("forretningsadresse", None),
            stiftelsesdato=data.get("stiftelsesdato", None),
            institusjonellSektorkode=data.get("institusjonellSektorkode", None),
            registrertIForetaksregisteret=data.get("registrertIForetaksregisteret", None),
            registrertIStiftelsesregisteret=data.get("registrertIStiftelsesregisteret", None),
            registrertIFrivillighetsregisteret=data.get("registrertIFrivillighetsregisteret", None),
            sisteInnsendteAarsregnskap=data.get("sisteInnsendteAarsregnskap", None),
            konkurs=data.get("konkurs", None),
            konkursdato=data.get("konkursdato", None),
            underAvvikling=data.get("underAvvikling", None),
            underAvviklingDato=data.get("underAvviklingDato", None),
            underTvangsavviklingEllerTvangsopplosning=data.get(
                "underTvangsavviklingEllerTvangsopplosning", None
            ),
            tvangsavvikletPgaManglendeSlettingDato=data.get(
                "tvangsavvikletPgaManglendeSlettingDato", None
            ),
            tvangsopplostPgaManglendeDagligLederDato=data.get(
                "tvangsopplostPgaManglendeDagligLederDato", None
            ),
            tvangsopplostPgaManglendeRevisorDato=data.get("tvangsopplostPgaManglendeRevisorDato"),
            tvangsopplostPgaManglendeRegnskapDato=data.get("tvangsopplostPgaManglendeRegnskapDato"),
            tvangsopplostPgaMangelfulltStyreDato=data.get("tvangsopplostPgaMangelfulltStyreDato"),
            maalform=data.get("maalform"),
            vedtektsdato=data.get("vedtektsdato"),
            vedtektsfestetFormaal=data.get("vedtektsfestetFormaal"),
            aktivitet=data.get("aktivitet", None),
            href=data.get("_links", {}).get("self", {}).get("href", None),
        )


@dataclass
class _BrregResLinks:
    """Dataclass for response links
    ref: https://data.brreg.no/enhetsregisteret/api/docs/index.html#enheter-sok
    """

    first: str
    self: str
    last: str | None = None
    next: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)

    def serialize(self) -> str:
        return json.dumps(self.to_dict())

    @staticmethod
    def res_parse(data: dict) -> _BrregResLinks:
        tmp = {}
        for k, v in data.items():
            if v is not None and isinstance(v, dict):
                tmp[k] = v.get("href", None)
        return _BrregResLinks(**tmp)

    @staticmethod
    def deserialize(data: str) -> _BrregResLinks:
        """
        Input:

            "first": {
                "href": "https://data.brreg.no/enhetsregisteret/api/enheter?navn=UiT&page=0&size=2"
            },
            "self": {
                "href": "https://data.brreg.no/enhetsregisteret/api/enheter?navn=UiT&size=2&page=0"
            },
            "next": {
                "href": "https://data.brreg.no/enhetsregisteret/api/enheter?navn=UiT&page=1&size=2"
            },
            "last": {
                "href": "https://data.brreg.no/enhetsregisteret/api/enheter?navn=UiT&page=16&size=2"
            }

        """
        return _BrregResLinks.res_parse(json.loads(data))
