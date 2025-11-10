FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install pydantic-settings

COPY . .

ENV PYTHONUNBUFFERED=1

CMD ["python", "-m", "src.llm_agent"]
