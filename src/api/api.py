#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod


class APIinterface(ABC):

    @abstractmethod
    def search(self, query: str, **kwargs) -> list[dict]:
        pass

    @abstractmethod
    def get(self, id: int, **kwargs) -> dict:
        pass
