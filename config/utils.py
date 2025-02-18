import json
import os
from django.http import JsonResponse
from django.conf import settings

LOG_FILE_DIR = os.path.join(settings.BASE_DIR, "django")


def read_logs(request, log_path):
    """JSON 로그 파일을 읽어서 반환하는 API"""
    try:
        with open(os.path.join(LOG_FILE_DIR, log_path), "r", encoding="utf-8") as file:
            logs = json.load(file)  # JSON 배열 읽기
        return JsonResponse(logs, safe=False)
    except (FileNotFoundError, json.JSONDecodeError):
        return JsonResponse({"error": "로그 파일을 찾을 수 없거나 JSON 형식이 아닙니다."}, status=500)
