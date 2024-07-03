FROM python:3.12.3

COPY app.py /app/

WORKDIR /app

COPY requirements.txt /tmp/
RUN pip3 install -r /tmp/requirements.txt

EXPOSE 8501

HEALTHCHECK CMD curl  --fail http://localhost:8501/_stcore/health

ENTRYPOINT [ "streamlit","run", "app.py", "--server.port=8501", "--server.address=0.0.0.0" ]