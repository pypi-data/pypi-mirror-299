from flask import request, json

from ...libs.json_lib import load_json


class AlphaRequest:
    @staticmethod
    def get_gets() -> dict[str, object]:
        """returns GET value as a dict.

        Returns:
            dict[str, object]: [description]
        """
        return {x: y for x, y in request.args.items()}

    @staticmethod
    def get_json():
        data = {}  # TODO: modify
        try:
            data = request.get_json()
        except:
            raw_data = request.data
            if isinstance(raw_data, bytes):
                if b"\x01\x8d" in raw_data:
                    raw_data = raw_data.replace(b"\x01\x8d", b"\n")
                raw_data = raw_data.decode()
            data = load_json(raw_data)
        if data is None or len(data) == 0:
            data = {}
        return data

    @staticmethod
    def get_uuid() -> str | None:
        request_uuid = None
        try:
            data = AlphaRequest.get_json()
            request_uuid = (
                request.method
                + " - "
                + request.full_path
                + "&"
                + "&".join("%s=%s" % (x, y) for x, y in data.items())
            )
        except:
            try:
                raw_data = request.data
            except:
                return None

            if isinstance(raw_data, bytes):
                if b"\x01\x8d" in raw_data:
                    raw_data = raw_data.replace(b"\x01\x8d", b"\n")
                raw_data = raw_data.decode()
            request_uuid = request.full_path + str(raw_data)  # TODO: update
        return request_uuid

    @staticmethod
    def get_token() -> str | None:
        token = None
        # Get token from authorization bearer
        try:
            auth = request.headers.get("Authorization", None)
        except:
            return None
        if auth is not None:
            if "bearer" in auth.lower():
                parts = auth.split()
                if len(parts) > 1:
                    token = parts[1]
            else:
                token = auth

        # Token from get have priority if present
        token_from_get = request.args.get("token", None)
        if token_from_get is not None:
            token = token_from_get

        # Token from post
        try:
            dataPost = AlphaRequest.get_json()
        except:
            dataPost = None
        if dataPost is not None and "token" in dataPost:
            token = dataPost["token"]
        return token
