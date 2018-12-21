FROM registry.centos.org/centos/centos:7

# Install Python 3.6
RUN yum install -y epel-release https://centos7.iuscommunity.org/ius-release.rpm &&\
    yum install -y python36u python36u-devel python36u-pip gcc git which make &&\
    yum clean all

# Cache dependencies
COPY requirements.txt /tmp/
RUN python3.6 -m pip install -r /tmp/requirements.txt

# Copy the application itself
ENV APP_DIR=/ghmonitor
RUN mkdir -p ${APP_DIR}
WORKDIR ${APP_DIR}
COPY . .

# Run!
CMD ["python3.6", "run.py"]


