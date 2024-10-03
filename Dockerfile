FROM python:slim-bullseye@sha256:dbdf1a8e375131679547183a70bdb4f9c512946a4ae42de172d59b151c3da5b7

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app/

EXPOSE 8501

CMD ["streamlit", "run", "load_streamlit.py"]