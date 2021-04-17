FROM python:3.9-alpine3.12

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt -i  https://pypi.tuna.tsinghua.edu.cn/simple
COPY . .

CMD [ "python", "main.py"]