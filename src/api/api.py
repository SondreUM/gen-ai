#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod


class APIgetter(ABC):

    @abstractmethod
    def search(self, query: str, **kwargs) -> list[dict]:
        pass

    @abstractmethod
    def get(self, id: str, **kwargs) -> dict:
        pass
