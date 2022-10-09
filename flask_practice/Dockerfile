FROM ubuntu
RUN apt update
RUN apt install -y python3
RUN apt install -y python3-pip
ENV DEBIAN_FRONTEND noninteractive
RUN apt install -y ffmpeg
RUN pip3 install flask
RUN pip3 install bcrypt
RUN pip3 install dataset
RUN pip3 install selenium
WORKDIR /home/service
ENTRYPOINT python3 site.py
