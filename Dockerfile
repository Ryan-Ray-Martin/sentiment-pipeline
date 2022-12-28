FROM rayproject/ray:nightly


# Working Directory
WORKDIR /app

# Copy source code to working directory
COPY *.py /app/
COPY *.txt /app/

RUN pip install --upgrade pip &&\
    pip install -r requirements.txt 





