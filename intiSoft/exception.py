# -*- coding: utf-8 -*-


class StateError(Exception):
    def __init__(self, message, errors):
        self.errors = errors
        self.message = message