import requests
import json
from time import sleep


class Discord:
    def __init__(self, *, url, retry: int = 3):
        self.url = url
        self.retry = retry

    def post(
        self,
        *,
        content=None,
        username=None,
        avatar_url=None,
        tts=False,
        file=None,
        embeds=None,
        allowed_mentions=None
    ):
        if content is None and file is None and embeds is None:
            raise ValueError("required one of content, file, embeds")
        data = {}
        if content is not None:
            data["content"] = content
        if username is not None:
            data["username"] = username
        if avatar_url is not None:
            data["avatar_url"] = avatar_url
        data["tts"] = tts
        if embeds is not None:
            data["embeds"] = embeds
        if allowed_mentions is not None:
            data["allowed_mentions"] = allowed_mentions

        if self.retry > 0:
            for _ in range(self.retry):
                try:
                    if file is not None:
                        return requests.post(
                            self.url, {"payload_json": json.dumps(data)}, files=file
                        )
                    else:
                        return requests.post(
                            self.url, json.dumps(data), headers={"Content-Type": "application/json"}
                        )
                except:
                    pass
                sleep(1)
            raise Exception("Failed to send message")
        else:
            if file is not None:
                return requests.post(
                    self.url, {"payload_json": json.dumps(data)}, files=file
                )
            else:
                return requests.post(
                    self.url, json.dumps(data), headers={"Content-Type": "application/json"}
                )
