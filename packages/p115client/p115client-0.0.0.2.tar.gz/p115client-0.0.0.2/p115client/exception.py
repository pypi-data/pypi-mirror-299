#!/usr/bin/env python3
# encoding: utf-8

__all__ = ["AuthenticationError", "LoginError", "MultipartUploadAbort"]


class LoginError(OSError):
    ...


class AuthenticationError(LoginError):
    ...


class MultipartUploadAbort(RuntimeError):
    def __init__(self, ticket: dict, /):
        self.ticket = ticket

