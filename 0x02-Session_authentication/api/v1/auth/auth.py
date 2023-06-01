#!/usr/bin/env python3
""" Module to manage
    API Authentication
"""
import os
from flask import request
from typing import List, TypeVar
import re


class Auth:
    """Defines Auth class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """check if route need authentication"""
        if path is not None and excluded_paths is not None:
            for exclusion_path in map(lambda x: x.strip(), excluded_paths):
                pattern = ""
                if exclusion_path[-1] == "*":
                    pattern = "{}.*".format(exclusion_path[0:-1])
                elif exclusion_path[-1] == "/":
                    pattern = "{}/*".format(exclusion_path[0:-1])
                else:
                    pattern = "{}/*".format(exclusion_path)
                if re.match(pattern, path):
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """Handles request validation"""
        authorization_header = request.headers.get("Authorization", None)
        if request is not None:
            return authorization_header
        return None

    def current_user(self, request=None) -> TypeVar("User"):
        """Fetch current user"""
        return None

    def session_cookie(self, request=None) -> str:
        """Gets the value of the cookie named SESSION_NAME."""
        if request is not None:
            cookie_name = os.getenv("SESSION_NAME")
            return request.cookies.get(cookie_name)
