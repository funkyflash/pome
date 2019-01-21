FROM python:3

ADD __init__.py /root/
ADD dev_config.json /root/
ADD requirements.txt /root/

WORKDIR /root/

RUN pip install pycrypto
RUN pip install -r /root/requirements.txt

ENTRYPOINT python /root/__init__.py