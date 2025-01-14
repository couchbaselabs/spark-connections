FROM bitnami/spark:3.3.2


ENV SPARK_HOME=/opt/bitnami/spark
ENV PATH="$SPARK_HOME/bin:$PATH"


USER root


RUN apt-get update && apt-get install -y \
    software-properties-common \
    curl \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    wget \
    llvm \
    libncurses5-dev \
    libncursesw5-dev \
    xz-utils \
    tk-dev \
    libffi-dev \
    liblzma-dev \
    && rm -rf /var/lib/apt/lists/*


RUN curl -O https://www.python.org/ftp/python/3.7.11/Python-3.7.11.tgz && \
    tar xzf Python-3.7.11.tgz && \
    cd Python-3.7.11 && \
    ./configure --enable-optimizations && \
    make -j$(nproc) && \
    make altinstall && \
    cd .. && \
    rm -rf Python-3.7.11 Python-3.7.11.tgz


RUN ln -sf /usr/local/bin/python3.7 /usr/bin/python && \
    ln -sf /usr/local/bin/pip3.7 /usr/bin/pip

RUN pip install --upgrade pip

ENV PYSPARK_PYTHON=/usr/bin/python \
    PYSPARK_DRIVER_PYTHON=/usr/bin/python

USER 1001

WORKDIR /app
COPY spark-connector-assembly-3.5.2.jar /opt/spark/jars/
COPY migrate_hdfs_to_couchbase.py /app/migrate_hdfs_to_couchbase.py

CMD ["spark-submit", "/app/migrate_hdfs_to_couchbase.py"]
