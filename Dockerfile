FROM node:12 AS node-builder

WORKDIR /usr/src/app

COPY package.json ./
COPY package-lock.json ./
RUN npm install

FROM python:3.8-alpine AS python-builder

WORKDIR /usr/src/app

RUN apk add --no-cache gcc g++ libc-dev libffi-dev postgresql-dev

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

FROM node-builder AS node-built

WORKDIR /usr/src/app

COPY . .
RUN npm run build -- --mode production --progress false

FROM python-builder

WORKDIR /usr/src/app

COPY --from=node-built /usr/src/app .
RUN SECRET_KEY=insecure python manage.py collectstatic

EXPOSE 8000

CMD [ "sh", "-c", "python manage.py migrate && gunicorn -b 0.0.0.0:8000 kinkgarden.wsgi --log-file -" ]
