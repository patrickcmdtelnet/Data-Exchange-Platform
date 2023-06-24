from rest_framework import renderers


class UserRenderer(renderers.JSONRenderer):
    charset = "utf-8"

    def render(self, data, accepted_media_type=None, context=None):
        response = ""

        if "ErrorDetail" in str(data):
            response = {"errors": data}
        else:
            response = {"data": data}
        return super().render(response)
