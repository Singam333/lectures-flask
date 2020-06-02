from flask import Response
import json


def response(status, message, status_code=200, **kwargs):
    return Response(
        json.dumps({"status": status, "message": message, **kwargs}),
        mimetype="application/json",
        status=status_code,
    )
