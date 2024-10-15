
#!/usr/bin/env python3
"""Basic auth class that inherits from Auth"""

from api.v1.auth.auth import Auth
import base64
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """basic auth class"""

    def extract_base64_authorization_header(self, authorization_header: str) -> str:  # Noqa
        """returns the BAse64 pasrt of authorization header"""
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None

        token = authorization_header.split(' ')[-1]
        return token

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:  # Noqa
        "returns the header"
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None

        try:
            item_to_decode = base64_authorization_header.encode('utf-8')
            decoded = base64.b64decode(item_to_decode)
            return decoded.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):  # Noqa
        """returns the user email and password from base64 decoded"""
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' in decoded_base64_authorization_header:
            email, password = decoded_base64_authorization_header.split(':')
            return email, password
        else:
            return None, None

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):  # Noqa
        """returns the user oject from email password"""
        if not isinstance(user_email, str) or user_email is None:
            return None
        if not isinstance(user_pwd, str) or user_pwd is None:
            return None

        try:
            users = User.search({"email": user_email})
            if not users or users == []:
                return None
            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
            return None
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """overloads AAuth and retrieves the user instance"""

        header = self.authorization_header(request)
        if header is not None:
            token = self.extract_base64_authorization_header(header)
            if token is not None:
                decoded = self.decode_base64_authorization_header(token)
                if decoded is not None:
                    email, password = self.extract_user_credentials(decoded)
                    if email is not None:
                        return self.user_object_from_credentials(email, password)  # Noqa
        return
