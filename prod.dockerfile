ARG PYTHON_VERSION=3.8.7
FROM python:${PYTHON_VERSION}
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Tokyo
RUN echo $TZ > /etc/timezone

ARG WORKDIR=/project
WORKDIR ${WORKDIR}

# change default shell
SHELL ["/bin/bash", "-c"]
RUN chsh -s /bin/bash

# Configure apt and install packages
RUN rm -rf /var/lib/apt/lists/* \
    && apt-get update \
    && apt-get upgrade -y \
    && apt-get -y install locales \
    && sed -i -E 's/# (ja_JP.UTF-8)/\1/' /etc/locale.gen \
    && locale-gen \
    && update-locale LANG=ja_JP.UTF-8

# copy requirements files
COPY . /project

# library install
RUN pip install -U pip
RUN pip install -r ./requirements.txt

ENV DEBIAN_FRONTEND=
CMD ["python", "-m", "exercise_report_slack.main"]
