import json
import logging
import os
import socket


class JsonArrayFileHandler(logging.FileHandler):
    """
    로그를 JSON 배열 형식으로 저장하는 핸들러.
    기존 로그를 유지하면서 새로운 로그를 추가.
    """

    def emit(self, record):
        # 로그 파일이 존재하는지 확인
        if os.path.exists(self.baseFilename):
            try:
                # 기존 로그 파일을 읽어오기
                with open(self.baseFilename, "r", encoding="utf-8") as f:
                    try:
                        logs = json.load(f)  # JSON 배열 읽기
                    except json.JSONDecodeError:
                        logs = []  # JSON 파싱 실패 시 빈 배열로 초기화
            except FileNotFoundError:
                logs = []
        else:
            logs = []

        # 새 로그 추가
        log_entry = self.format(record)
        logs.append(json.loads(log_entry))  # 로그 추가

        # 새로운 JSON 배열로 파일 덮어쓰기
        with open(self.baseFilename, "w", encoding="utf-8") as f:
            json.dump(logs, f, ensure_ascii=False, indent=4)  # 포맷팅


class CustomJsonFormatter(logging.Formatter):
    """App Log 를 JSON 형식으로 로그를 변환하는 커스텀 포맷터"""

    def format(self, record):
        log_record = {}

        for key, value in record.__dict__.items():
            serialized_value = self._safe_serialize(value)
            if serialized_value not in [None, "", "null"]:
                log_record[key] = serialized_value

        log_record["message"] = record.getMessage()

        log_record["original_msg"] = record.msg
        log_record["args"] = record.args

        return json.dumps(log_record, ensure_ascii=False)

    def _safe_serialize(self, value):
        """JSON 직렬화가 불가능한 객체를 문자열로 변환"""
        try:
            json.dumps(value)  # JSON 직렬화 테스트
            return value
        except (TypeError, OverflowError):
            if isinstance(value, socket.socket):
                try:
                    return f"{value.getsockname()} → {value.getpeername()}"
                except OSError:
                    return "Closed Socket"
            return str(value)  # 변환이 불가능하면 문자열로 변환


class ExcludeLogFilter(logging.Filter):
    """특정 URL 패턴(`/log/`)에 대한 로그를 모든 로거에서 무시하는 필터"""

    def filter(self, record):
        msg_list = list(record.getMessage().split(" "))

        if msg_list[1].startswith("/log/"):
            return False  # `/log/` 경로의 로그는 기록하지 않음

        return True  # `/log/` 경로가 아닌 로그는 기록함
