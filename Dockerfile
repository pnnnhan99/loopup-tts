# Stage 1: Build Vue app
FROM node:20-slim AS builder
WORKDIR /app
COPY package.json package-lock.json ./
COPY phonemizer-1.2.2.tgz ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: Python server
FROM python:3.12-slim
WORKDIR /app

COPY --from=builder /app/dist ./dist
COPY hf-server/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY hf-server/app.py ./

ENV PORT=7860
EXPOSE 7860

CMD ["gunicorn", "-b", "0.0.0.0:7860", "-w", "2", "--timeout", "120", "app:app"]
