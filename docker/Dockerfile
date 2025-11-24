# ==============================================================================
# 1단계: 빌더 스테이지 (의존성 설치 및 가상 환경 준비)
# ==============================================================================
FROM python:3.13-slim AS builder

WORKDIR /usr/src/app/

# 시스템 의존성 설치 (PostgreSQL 클라이언트 등)
# libpq-dev : PostgreSQL 드라이버(psycopg2) 컴파일에 필수
# 마지막줄 apt 캐시 정리
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    netcat-openbsd \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Poetry 환경 변수 설정
# 도커의 VIRTUAL_ENV 경로를 명시적으로 고정하여 다단계 빌드에서 정확히 복사하도록 합니다.
ENV POETRY_HOME="/opt/poetry"
ENV PATH="$POETRY_HOME/bin:$PATH"

# Poetry가 프로젝트 내부에 .venv를 만들도록 환경 변수를 주입합니다.
# Poetry는 이 환경 변수를 보면 자동으로 프로젝트 폴더 내에 .venv를 생성합니다.
ENV POETRY_VIRTUALENVS_IN_PROJECT=true

# Install Poetry
RUN pip install poetry

# 프로젝트 메타데이터 파일 복사
COPY pyproject.toml poetry.lock ./

# 의존성 설치: /usr/src/app/.venv에 가상 환경이 생성됩니다.
# 프로젝트 루트는 설치하지 않고(최종 스테이지에서 설치, dependency main group)
RUN poetry install --no-root --only main

# ==============================================================================
# 2단계: 최종 스테이지 (애플리케이션 실행환경 구성)
# ==============================================================================
FROM python:3.13-slim AS final

WORKDIR /usr/src/app/

# run.sh에서 사용하는 netcat을 여기서 다시 설치해야 합니다.
RUN apt-get update \
    && apt-get install -y --no-install-recommends netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# 1단계 빌더에서 생성된 가상 환경(.venv) 복사 및 PATH 설정
# 경로를 /usr/src/app/.venv로 유지합니다. (1단계에서 생성된 실제 경로)
COPY --from=builder /usr/src/app/.venv /usr/src/app/.venv

# VIRTUAL_ENV 경로와 PATH를 설정합니다.
ENV VIRTUAL_ENV="/usr/src/app/.venv"
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# 프로젝트 코드 복사
COPY . .

# Django port runs on
EXPOSE 8000

#CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
COPY ./scripts /scripts
RUN chmod +x /scripts/run.sh
CMD ["/scripts/run.sh"]