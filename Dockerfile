FROM rayproject/ray:nightly

WORKDIR /app

COPY *.py /app/
COPY *.txt /app/

RUN pip install --upgrade pip &&\
    pip install -r /app/requirements.txt