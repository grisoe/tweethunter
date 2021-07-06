FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive

WORKDIR /code

COPY tweethunter.py /code
COPY requirements.txt /code

RUN apt-get -y update

RUN apt-get install wget -y
RUN apt-get install git -y
RUN apt-get install firefox -y
RUN apt-get install firefox-geckodriver -y
RUN apt-get install python3.8 -y
RUN apt-get -y install python3-pip

RUN pip3 install -r requirements.txt

RUN mkdir conf

COPY conf/srax_bt.json /code/conf/

CMD ["tweethunter.py"]
ENTRYPOINT ["python3"]
