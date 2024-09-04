
# Django Practice Repository

이 레포지토리는 Django 프레임워크를 학습하며 다양한 기능들을 실험하고 테스트한 내용을 담고 있습니다. 쿼리 최적화, API 문서 자동화, 테스트 코드 작성, 커스텀 매니저, 로깅, 커스텀 커맨드, 동적 Serializer 필드 등 Django에서 자주 사용되는 기능들을 학습하는 데 중점을 두었습니다.

## 학습 및 테스트한 기능

- **쿼리 최적화**: 데이터베이스 쿼리의 성능을 향상시키기 위한 최적화 기법을 학습 및 적용하였습니다.
- **API 문서 자동화**: Swagger와 같은 도구를 사용하여 API 문서를 자동으로 생성하는 기능을 구현하였습니다.
- **테스트 코드 작성**: Django 애플리케이션의 단위 테스트와 통합 테스트를 작성하여 안정성을 확인하였습니다.
- **커스텀 매니저**: Django의 커스텀 매니저를 활용하여 QuerySet을 확장하고 커스터마이징하는 방법을 익혔습니다.
- **로깅 (Logger)**: 디버깅과 모니터링을 개선하기 위해 로깅을 설정하고 구성하는 방법을 학습하였습니다.
- **Django Command**: Django의 커스텀 커맨드를 작성하고 이를 활용하여 관리 작업을 자동화하는 방법을 실습하였습니다.
- **Serializer 동적 필드**: Django REST Framework의 Serializer에서 동적 필드를 처리하는 방법을 학습하였습니다.

## 실행 방법

1. 저장소 클론:
    ```bash
    git clone https://github.com/dhwpdnr/Django-practice.git
    ```

2. 의존성 설치:
    ```bash
    pip install -r requirements.txt
    ```

3. 마이그레이션 적용:
    ```bash
    python manage.py migrate
    ```

4. 로컬 서버 실행:
    ```bash
    python manage.py runserver
    ```

## Notion 정리

더 자세한 학습 내용은 [Notion](https://www.notion.so/Django-213282c789934d66845283a988da1f5c) , [Velog](https://velog.io/@dhwpdnr)에서 확인할 수 있습니다.

---

