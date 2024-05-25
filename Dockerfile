FROM python:3.10.11-buster

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

# RUN python manage.py collectstatic

# EXPOSE 8080

CMD ["sh", "-c", "python manage.py runserver 0.0.0.0:8080"]
