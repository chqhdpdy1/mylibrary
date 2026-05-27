# mylibrary — Django Book Service

Django 모델에 `@classmethod` 데코레이터와 함수 리턴 타입 힌트를 적용한 간단한 책 조회 서비스입니다.

## 프로젝트 구조

```
mylibrary/
├── manage.py                          ← Django 명령 진입점
├── requirements.txt                   ← 필요 패키지 (Django)
├── shell_demo.py                      ← Django shell 데모 스크립트
├── mylibrary/                         ← 프로젝트 설정 패키지
│   ├── __init__.py
│   ├── settings.py                    ← INSTALLED_APPS 에 'books' 등록
│   ├── urls.py
│   └── wsgi.py
└── books/                             ← 앱 패키지
    ├── __init__.py
    ├── apps.py
    ├── admin.py
    ├── models.py                      ← Book 모델 + 4개 classmethod 정의
    ├── views.py
    ├── tests.py
    ├── migrations/
    └── management/
        └── commands/
            └── seed_books.py          ← 샘플 데이터 등록 커맨드
```

## 주요 모듈 설명

### `books/models.py`

`Book` 모델은 `title`, `author` 두 개의 CharField 를 가지며, 책 조회를 위한 4개의 클래스 메서드를 제공합니다.

| 메서드 | 리턴 타입 | 기능 |
| --- | --- | --- |
| `get_all_books()` | `QuerySet['Book']` | DB 의 모든 Book 객체를 반환 |
| `get_books_by_author(author_name)` | `QuerySet['Book']` | 저자명으로 필터링 (대소문자 무시, 정확 일치 — `__iexact`) |
| `get_books_by_title_keyword(keyword)` | `QuerySet['Book']` | 제목에 키워드 포함 여부로 필터링 (대소문자 무시, 부분 일치 — `__icontains`) |
| `get_books_ordered_by_title()` | `QuerySet['Book']` | 모든 책을 제목 오름차순으로 정렬 후 반환 |

모든 메서드는 `@classmethod` 데코레이터를 사용하여 인스턴스가 아닌 클래스 단위로 호출됩니다. 리턴 타입은 `QuerySet['Book']` 으로 명시되어 있으며, 클래스 본문 내에서는 `Book` 클래스가 아직 정의 중이기 때문에 forward reference 로 문자열 처리하였습니다.

#### `__iexact` vs `__icontains`

| 필터 | 매칭 방식 | 대소문자 |
| --- | --- | --- |
| `__exact` | 정확 일치 | 구분함 |
| `__iexact` | 정확 일치 | 구분 안 함 |
| `__contains` | 부분 일치 | 구분함 |
| `__icontains` | 부분 일치 | 구분 안 함 |

### `shell_demo.py`

Django shell 환경에서 위 4개 메서드를 호출하여 결과를 출력하는 데모 스크립트입니다. 각 섹션은 호출 → for 루프로 결과 순회 → 출력의 패턴을 따릅니다.

### `books/management/commands/seed_books.py`

`python manage.py seed_books` 명령으로 실행되며, 다음 3권의 샘플 책을 DB 에 등록합니다.

- `1984` by George Orwell
- `Brave New World` by Aldous Huxley
- `Fahrenheit 451` by Ray Bradbury

> ⚠️ 명령을 두 번 이상 실행하면 같은 책이 중복 등록됩니다. 리셋하려면 `db.sqlite3` 삭제 후 마이그레이션부터 다시 실행하거나, shell 에서 `Book.objects.all().delete()` 후 재실행하세요.

## 실행 방법

### 1. 환경 준비

```bash
# (선택) 가상환경 생성
python -m venv venv
venv\Scripts\activate              # Windows
# source venv/bin/activate         # macOS / Linux

# 의존성 설치
pip install -r requirements.txt
```

### 2. 마이그레이션

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. 샘플 데이터 등록

```bash
python manage.py seed_books
```

### 4. Shell 데모 실행

파일 전체를 한 번에 실행:

```bash
python manage.py shell -c "exec(open('shell_demo.py', encoding='utf-8').read())"
```

또는 한 줄씩 직접 입력:

```bash
python manage.py shell
# 그리고 shell_demo.py 내용을 한 줄씩 복사해 붙여넣기
```

## 정상 출력 예시

```
📚 전체 책 목록:
1984 by George Orwell
Brave New World by Aldous Huxley
Fahrenheit 451 by Ray Bradbury

✍️ George Orwell 책 목록:
1984 by George Orwell

🔍 제목에 'new'가 포함된 책 목록:
Brave New World by Aldous Huxley

🔠 제목순 정렬:
1984 by George Orwell
Brave New World by Aldous Huxley
Fahrenheit 451 by Ray Bradbury
```
