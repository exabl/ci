FROM {{ image }}
MAINTAINER Ashwin Vishnu Mohanan <avmo@kth.se>

RUN apt-get update

{% for pkg in apt_requirements -%}
RUN apt-get install -y --no-install-recommends {{ pkg }}
{%- endfor %}

RUN rm -rf /var/lib/apt/lists/*

RUN groupadd -g 999 appuser && useradd -m -r -u 999 -g appuser -s /bin/bash appuser -s /bin/bash
USER appuser

ARG HOME=/home/appuser

RUN mkdir -p $HOME/opt
WORKDIR $HOME/opt
RUN echo $USER $HOME $PWD && whoami

RUN mkdir -p $HOME/.local/include $HOME/.local/lib

COPY requirements.txt $PWD
RUN {{ pip }} install --no-cache-dir --user -U -r requirements.txt

RUN mkdir -p $HOME/.config/matplotlib
RUN echo 'backend      : agg' > $HOME/.config/matplotlib/matplotlibrc
ENV LD_LIBRARY_PATH=$HOME/.local/lib
ENV PATH=$PATH:$HOME/.local/bin
ENV CPATH=$CPATH:$HOME/.local/include
