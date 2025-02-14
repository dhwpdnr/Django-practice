from django.test import TestCase
from django.db import connection
from django.test.utils import CaptureQueriesContext


class CommonTest(TestCase):
    def print_captured_queries(self, func, *args, **kwargs):
        """실행된 쿼리 개수와 SQL 출력"""
        with CaptureQueriesContext(connection) as ctx:
            response = func(*args, **kwargs)

        print(f"\n[쿼리 개수] {len(ctx.captured_queries)}")

        for i, query in enumerate(ctx.captured_queries, start=1):
            print(f"[Query {i}] {query['sql']}")

        return response
