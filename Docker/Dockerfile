FROM ubuntu:22.04 as base

ENV DEBIAN_FRONTEND=noninteractive

#Basic container env apt package install
RUN apt-get update && apt-get install -y vim nano curl git sudo nano

# Add user
ARG USERNAME=qtuser
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create the user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    #
    # [Optional] Add sudo support. Omit if you don't need to install software after connecting.
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# Set PATH for the user
USER $USERNAME
ENV PATH="/home/$USERNAME/.local/bin:$PATH"


FROM base as dev
# This fix: libGL error: No matching fbConfigs or visuals found
ENV LIBGL_ALWAYS_INDIRECT=1

# Install Python 3,pip3,  PyQt5
RUN sudo apt-get update && sudo apt-get install -y python3-pip python3-pyqt5

WORKDIR /home/qtuser

COPY hello.py /tmp/hello.py

