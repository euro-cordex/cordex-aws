FROM ubuntu:22.04
ENV PATH="/root/miniconda3/bin:${PATH}"
ARG PATH="/root/miniconda3/bin:${PATH}"

LABEL maintainer="lars.buntemeyer@hereon.de"

RUN apt-get update
RUN apt-get install -y software-properties-common
RUN apt-add-repository -y universe
RUN apt-get update

RUN apt-get -y install vim git
RUN apt-get -y install wget

WORKDIR /cordex-aws/

RUN wget \
    https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && mkdir /root/.conda \
    && bash Miniconda3-latest-Linux-x86_64.sh -b \
    && rm -f Miniconda3-latest-Linux-x86_64.sh
RUN conda --version
RUN conda config --add channels conda-forge
RUN conda config --set channel_priority strict

RUN conda create -n cordex-aws python=3.10 dynamic-chunks==0.0.2 \
    pangeo-forge-cordex==0.3.4 pangeo-forge-recipes==0.10.5 \
    aiohttp requests fsspec s3fs zarr boto3

RUN conda activate cordex-aws
