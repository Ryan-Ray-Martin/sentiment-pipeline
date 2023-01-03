FROM rayproject/ray:nightly

COPY *.py /opt/
COPY *.txt /opt/

RUN pip install --upgrade pip &&\
    pip install -r /opt/requirements.txt