from django.test import TestCase


class SSEAPITestCase(TestCase):
    def test_sse_api(self):
        """
        SSE API가 데이터를 스트리밍으로 전송하는지 확인
        """
        # API 요청 (StreamingHttpResponse)
        response = self.client.get("/sse/", stream=True)

        # 응답 상태 코드 확인
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/event-stream")

        # SSE 데이터 스트리밍 확인
        expected_messages = [
            'data: {"message": "Update 1", "id": 1}\n\n',
            'data: {"message": "Update 2", "id": 2}\n\n',
            'data: {"message": "Update 3", "id": 3}\n\n',
            'data: {"message": "Update 4", "id": 4}\n\n',
            'data: {"message": "Update 5", "id": 5}\n\n',
            'data: {"message": "Update 6", "id": 6}\n\n',
            'data: {"message": "Update 7", "id": 7}\n\n',
            'data: {"message": "Update 8", "id": 8}\n\n',
            'data: {"message": "Update 9", "id": 9}\n\n',
            'data: {"message": "Update 10", "id": 10}\n\n',
        ]

        # 스트리밍 데이터 읽기
        stream_data = []
        for chunk in response.streaming_content:
            stream_data.append(chunk.decode("utf-8"))  # 데이터를 UTF-8로 디코딩

        # 받은 스트리밍 데이터와 예상 데이터 비교
        for i, message in enumerate(expected_messages):
            self.assertIn(message, stream_data[i])

        # 데이터 개수 확인
        self.assertEqual(len(stream_data), len(expected_messages))
