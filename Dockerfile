FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY shared/ shared/
COPY agents/ agents/

ENV PORT=8080

# Set AGENT_MODULE per service:
#   agents.orchestrator.app:a2a_app
#   agents.pharmacy.app:a2a_app
#   agents.home_health.app:a2a_app
ENV AGENT_MODULE=agents.orchestrator.app:a2a_app

CMD ["sh", "-c", "exec uvicorn ${AGENT_MODULE} --host 0.0.0.0 --port ${PORT}"]
