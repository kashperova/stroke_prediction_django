FROM python:3.7

WORKDIR /stroke

COPY requirements.txt ./
RUN pip3 install -r requirements.txt

RUN export PYTHONPATH='${PYTHONPATH}:/stroke'

COPY . .

CMD ["python", "./manage.py"]