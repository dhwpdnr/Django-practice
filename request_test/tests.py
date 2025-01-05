from django.test import TestCase


class RequestTest(TestCase):
    def test_request(self):
        # request setting
        res = self.client.get(
            "/request/?param=test_param",
            HTTP_USER_AGENT="Mozilla/5.0",
            HTTP_ACCEPT="application/json",
            HTTP_ACCEPT_LANGUAGE="ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
            HTTP_ACCEPT_ENCODING="gzip, deflate, br",
            HTTP_CONNECTION="keep-alive",
            HTTP_UPGRADE_INSECURE_REQUESTS="1",
            HTTP_CACHE_CONTROL="max-age=0",
            HTTP_COOKIE="csrftoken=1b2fJgV7e5l7g",
            HTTP_REFERER="http://localhost:8000/request/",
            HTTP_SEC_FETCH_DEST="document",
            HTTP_SEC_FETCH_MODE="navigate",
            HTTP_SEC_FETCH_SITE="same-origin",
            HTTP_SEC_FETCH_USER="?1",
            HTTP_SEC_CH_UA='" Not A;Brand";v="99", "Chromium";v="90"',
            HTTP_SEC_CH_UA_MOBILE="?0",
            HTTP_SEC_CH_UA_PLATFORM='"Windows"',
        )
        # res = self.client.get("/request/")
        print(res.data)
