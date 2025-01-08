import requests


def send_webhook(url, payload, headers=None):
    """웹훅 요청을 보내는 함수"""
    # 헤더 정의
    headers = headers or {"Content-Type": "application/json"}
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # HTTP 오류 발생 시 예외를 발생
        return response
    except requests.exceptions.RequestException as e:
        return None
