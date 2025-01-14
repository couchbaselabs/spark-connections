FROM bitnami/spark:3.3.2

# Set environment variables for Spark
ENV SPARK_HOME=/opt/bitnami/spark
ENV PATH="$SPARK_HOME/bin:$PATH"

# Switch to root for installing packages
USER root

# Install dependencies
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

# Install Python 3.7
RUN curl -O https://www.python.org/ftp/python/3.7.11/Python-3.7.11.tgz && \
    tar xzf Python-3.7.11.tgz && \
    cd Python-3.7.11 && \
    ./configure --enable-optimizations && \
    make -j$(nproc) && \
    make altinstall && \
    cd .. && \
    rm -rf Python-3.7.11 Python-3.7.11.tgz

# Update Python binary symlinks
RUN ln -sf /usr/local/bin/python3.7 /usr/bin/python && \
    ln -sf /usr/local/bin/pip3.7 /usr/bin/pip

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install redis pyspark

# Set environment variables for PySpark
ENV PYSPARK_PYTHON=/usr/bin/python \
    PYSPARK_DRIVER_PYTHON=/usr/bin/python

# Switch back to non-root user
USER 1001

# Set working directory
WORKDIR /app

# Copy necessary JAR files for Spark
COPY spark-connector-assembly-3.5.2.jar /opt/spark/jars/
COPY spark-redis_2.12-3.1.0-jar-with-dependencies.jar /opt/spark/jars/

# Copy the PySpark script to the container
COPY redis_to_couchbase.py /app/redis_to_couchbase.py

# Set the command to run the PySpark script with spark-submit
CMD ["spark-submit", "--jars", "/opt/spark/jars/spark-redis_2.12-3.1.0-jar-with-dependencies.jar,/opt/spark/jars/spark-connector-assembly-3.5.2.jar", "/app/redis_to_couchbase.py"]
