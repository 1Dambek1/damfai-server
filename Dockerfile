FROM python:3.10

WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && curl https://sh.rustup.rs -sSf | sh -s -- -y \
    && export PATH="$HOME/.cargo/bin:$PATH" \
    && echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> /etc/environment

COPY req.txt .

RUN pip install --no-dependencies transformers

RUN pip install filelock huggingface-hub numpy packaging pyyaml regex requests tqdm sacremoses

RUN pip install -r req.txt

COPY . .

# RUN apt-get update && apt-get install -y supervisor
# Копируем скрипт-обертку
COPY go.sh .


# Запускаем скрипт-обертку
CMD ["./go.sh"]


# CMD ["supervisord", "-c", "/app/supervisord.conf"]

