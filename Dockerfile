FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get -y update
RUN apt-get install -y wget git firefox firefox-geckodriver python3.8 python3-pip && \
    rm -rf /var/lib/apt/lists/* && \
    apt clean

WORKDIR /th

RUN mkdir conf

COPY tweethunter.py requirements.txt /th/
COPY conf/test.json /th/conf

RUN mv /th/conf/test.json /th/conf/conf.json
RUN pip3 install -r requirements.txt

#CMD ["tweethunter.py"]
#ENTRYPOINT ["python3"]
