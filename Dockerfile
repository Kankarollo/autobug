FROM python:3.8-slim-buster
WORKDIR /app
COPY --from=golang:1.16.13-buster /usr/local/go/ /usr/local/go/
COPY . .

ENV PATH="/usr/local/go/bin:${PATH}"
ENV GOPATH="/usr/local/go"

RUN pip3 install -r requirements.txt
RUN go install -v github.com/OWASP/Amass/v3/...@master 

RUN git clone https://github.com/gwen001/github-subdomains && \
    cd github-subdomains && \
    go build main.go && \
    sudo ln -s $(pwd)/main /usr/bin/github-subdomain

CMD ["python3", "autobug.py"]