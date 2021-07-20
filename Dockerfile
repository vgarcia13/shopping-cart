FROM python:3.8
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
ENV LANG es_MX.UFT-8
ENV LC_ALL es_MX.UFT-8
RUN pip install -r requirements.txt
ADD . /code/
COPY dockerutils/wait-for-postgres.sh /dockerutils/wait-for-postgres.sh
RUN chmod +x dockerutils/wait-for-postgres.sh
ENV TZ=America/Mexico_City
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
