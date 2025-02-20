import json
import os
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import render

LOG_FILE_PATH = os.path.join(settings.BASE_DIR, "django/app_log.json")


def read_logs(request):
    """JSON 로그 파일을 읽어서 반환하는 API"""
    try:
        with open(LOG_FILE_PATH, "r", encoding="utf-8") as file:
            logs = json.load(file)
        return JsonResponse(logs, safe=False)
    except (FileNotFoundError, json.JSONDecodeError):
        return JsonResponse({"error": "로그 파일을 찾을 수 없거나 JSON 형식이 아닙니다."}, status=500)


def log_monitoring_page(request):
    """로그 모니터링 페이지"""
    return render(request, "log_view.html")
