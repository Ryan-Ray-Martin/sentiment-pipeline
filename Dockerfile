FROM rayproject/ray:nightly

USER root

# Working Directory
WORKDIR /app

# Copy source code to working directory
COPY *.py /app/
COPY *.txt /app/

# Install packages from requirements.txt
# hadolint ignore=DL3013
RUN apt-get update -y && \
    apt-get install -y curl gnupg && \ 
    echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && \
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg  add - && \
    apt-get update -y &&\
    apt-get install google-cloud-sdk -y &&\
    apt-get install postgresql-client -y

RUN pip install --upgrade pip &&\
    pip install -r requirements.txt 

ENV PATH $PATH:~/gcloud/google-cloud-sdk/bin




