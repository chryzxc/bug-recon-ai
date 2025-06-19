FROM python:3.9-alpine

WORKDIR /sublister
RUN apk add --no-cache git \
    && git clone https://github.com/aboul3la/Sublist3r.git . \
    && pip install -r requirements.txt

ENTRYPOINT ["python", "sublist3r.py"]