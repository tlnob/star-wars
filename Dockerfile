FROM alpine:3.8
WORKDIR /star-wars
ADD . /star-wars

RUN apk add --no-cache ca-certificates python3 py3-pip openssl libffi libxml2 libxslt

RUN apk update && apk add --no-cache --virtual build-deps \
	linux-headers \
	gcc \
	g++ \
	build-base \
    py3-pip \
	python3-dev \
	tzdata \
	curl \
	libxml2-dev \
	libxslt-dev 
RUN pip3 install --upgrade pip

# ENV VIRTUAL_ENV=/opt/venv
# RUN python3 -m venv $VIRTUAL_ENV
# ENV PATH="$VIRTUAL_ENV/bin:$PATH"
# RUN . venv/bin/activate
RUN cat requirements.txt
RUN pip3 install -r requirements.txt

# RUN pip3 install -r requirements.txt

# CMD ["python3","app.py"]