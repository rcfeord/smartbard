# backend/Dockerfile

FROM python:3.10-slim

EXPOSE 8000

WORKDIR /myapp

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8000" , "--reload"]
