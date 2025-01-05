from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from pprint import pprint


class RequestTestAPI(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        data = {
            # Django의 WSGI 환경 변수를 담고 있는 딕셔너리
            # HTTP 헤더뿐 아니라 서버와 관련된 다양한 환경 변수 정보도 포함
            "request_META": request.META,
            # 요청의 헤더만을 간단하게 출력
            "request_headers": request.headers,
            "request_method": request.method,
            "request_scheme": request.scheme,
            "request_content_type": request.content_type,
        }
        pprint(data)

        return Response({"data": "Request Test API"})
