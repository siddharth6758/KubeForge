FROM python:3.13
WORKDIR /worker

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8675

CMD ["python", "worker.py"]