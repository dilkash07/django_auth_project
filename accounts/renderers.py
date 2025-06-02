from rest_framework.renderers import JSONRenderer
from rest_framework.utils import json


class UserRenderer(JSONRenderer):
    charset = "utf-8"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        try:
            response = json.dumps(data, default=str)
        except Exception as exc:
            response = json.dumps({"error": "Serialization error", "details": str(exc)})
        return response.encode(self.charset)
