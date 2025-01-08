from rest_framework.views import APIView
from django.http import StreamingHttpResponse
import time


class SSEAPIView(APIView):
    """SSE API TEST"""

    def get(self, request, *args, **kwargs):
        # 데이터 스트림 생성기
        def event_stream():
            for i in range(1, 11):  # 10개의 메시지를 전송
                yield f'data: {{"message": "Update {i}", "id": {i}}}\n\n'  # JSON 데이터 포맷
                time.sleep(1)  # 1초 간격으로 메시지 전송

        # StreamingHttpResponse 생성
        response = StreamingHttpResponse(
            event_stream(), content_type="text/event-stream"
        )
        response["Cache-Control"] = "no-cache"  # 캐시 비활성화
        response["Transfer-Encoding"] = "chunked"  # 데이터 청크 방식
        return response
