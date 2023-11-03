FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Install basic utility apt packages
RUN  apt-get update && apt-get install -y vim git tree htop nano sudo net-tools python3-pip 

# Add qtuser
RUN adduser --disabled-password --gecos "" qtuser  \
    && echo 'qtuser:qtuser' | chpasswd \
    && adduser qtuser sudo \
    && echo 'qtuser ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers


# Install Python 3, PyQt5
RUN apt-get update && apt-get install -y python3-pyqt5 pyqt5-dev-tools qttools5-dev-tools

COPY requirments.txt /tmp/requirments.txt
RUN pip3 install -r /tmp/requirments.txt

WORKDIR /home/qtuser

COPY hello.py /tmp/hello.py
