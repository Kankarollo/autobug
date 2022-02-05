FROM python:3.8-slim-buster
WORKDIR /app
COPY --from=golang:1.13-alpine /usr/local/go/ /usr/local/go/
COPY . .

RUN pip3 install -r requirements.txt

ENV PATH="/usr/local/go/bin:${PATH}"

RUN go install -v github.com/OWASP/Amass/v3/...@master 

CMD ["python3", "autobug.py"]