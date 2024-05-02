#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod


class APIinterface(ABC):

    @abstractmethod
    def search(self, query: str, **kwargs) -> list[dict]:
        """Search the API for items
        Args:
            query (str): The search query
        """
        ...

    @abstractmethod
    def get(self, id: int, **kwargs) -> dict:
        """Get a single item from the previous query
        Args:
            id (int): The index of the item to get
        """
        ...
