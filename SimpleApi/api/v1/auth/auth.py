#!/usr/bin/python3
"""class AUth to secure the API"""


from flask import request
from typing import List, TypeVar

class Auth():
    """class auth"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        if path is None:
            return True
        if excluded_paths == [] or excluded_paths is None:
            return True
        if path in excluded_paths:
            return False
        for p in excluded_paths:
            if p.startswith(path):
                return False
            elif path.startswith(p):
                return False
        return True
    
    def authorization_header(self, request=None) -> str:
        if request is None:
            return None
        header = request.headers.get("Authorization")

        if header is None:
            return None
        return header
    
    def current_user(self, request=None) -> TypeVar('User'):
        return None