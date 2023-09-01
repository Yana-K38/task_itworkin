FROM python:3.10

RUN mkdir /sm_app

WORKDIR /sm_app

COPY requirements.txt .

COPY . .

RUN pip install --upgrade pip && pip install -r requirements.txt

RUN chmod a+x .docker/*.sh

ENTRYPOINT ["bash", ".docker/app.sh"]