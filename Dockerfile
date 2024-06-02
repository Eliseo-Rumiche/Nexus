FROM python:3.10.11-buster

ENV SECRET_KEY=$SECRET_KEY
ENV DEBUG=$DEBUG
ENV EMAIL_HOST_USER=$EMAIL_HOST_USER
ENV EMAIL_HOST_PASSWORD=$EMAIL_HOST_PASSWORD
ENV ALLOWED_HOSTS=$ALLOWED_HOSTS
ENV CSRF_TRUSTED_ORIGINS=$CSRF_TRUSTED_ORIGINS
ENV DATABASE_URL=$DATABASE_URL
 

RUN ln -fs /usr/share/zoneinfo/America/Lima /etc/localtime && \
    echo "America/Lima" > /etc/timezone

RUN apt-get update && apt-get install -y python3 python3-pip python3-dev\
    default-libmysqlclient-dev postgresql-client build-essential\
    libgl1-mesa-glx libglib2.0-dev wait-for-it\
    fontconfig libjpeg62-turbo libpng16-16 libx11-6\
    libxcb1 libxext6 libxrender1 xfonts-75dpi xfonts-base wget


WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=Nexus.settings

RUN python3 manage.py collectstatic

CMD ["sh", "-c", "python manage.py runserver 0.0.0.0:8080"]
