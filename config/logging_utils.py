import json
import logging
import os


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
        log_record = {
            "level": record.levelname,
            "timestamp": self.formatTime(record, self.datefmt),
            "module": record.module,
            "log_source": record.name,  # 로그 출처 (django.request, django.server 등)
            "filename": record.filename,
            "funcName": record.funcName,
            "lineno": record.lineno,
            "threadName": record.threadName,
            "processName": record.processName,
        }

        # msg와 args를 적용하여 최종 message 생성
        try:
            if record.args:
                formatted_message = record.msg % record.args  # %s 포맷팅 적용
            else:
                formatted_message = record.msg
        except TypeError:  # 혹시라도 args와 msg가 일치하지 않는 경우 대비
            formatted_message = record.getMessage()

        # 이중 따옴표를 제거하여 JSON 깨짐 방지
        if isinstance(formatted_message, str):
            formatted_message = formatted_message.strip('"')

        log_record["message"] = formatted_message

        # 원본 msg도 이중 따옴표 제거해서 저장
        if isinstance(record.msg, str):
            log_record["original_msg"] = record.msg.strip('"')
        else:
            log_record["original_msg"] = record.msg

        # 추가적인 정보 저장
        extra_fields = ["status_code", "request", "server_time"]
        for field in extra_fields:
            if hasattr(record, field):
                log_record[field] = str(getattr(record, field))  # JSON 직렬화 가능하도록 변환

        return json.dumps(log_record, ensure_ascii=False)  # 한글 깨짐 방지
