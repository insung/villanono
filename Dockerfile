# --- 1. Builder Stage ---
# 패키지 설치를 위한 빌더 단계를 정의합니다.
# 최신 보안 패치가 적용된 버전을 사용하는 것이 좋습니다.
FROM python:3.11-slim-bullseye as builder

WORKDIR /app

# 가상 환경을 생성하여 의존성을 시스템과 격리합니다.
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# requirements.txt를 먼저 복사하여 Docker 레이어 캐시를 활용합니다.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# --- 2. Final Stage ---
# 애플리케이션 실행을 위한 최종 단계를 정의합니다.
# Distroless 이미지를 사용하여 공격 표면을 최소화합니다.
FROM gcr.io/distroless/python3-debian11

WORKDIR /app

# 빌더 단계에서 설치한 가상 환경과 소스 코드를 복사합니다.
COPY --from=builder /opt/venv /opt/venv
COPY . .

ENV PATH="/opt/venv/bin:$PATH"

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]