FROM python:3.8-slim-buster
COPY --from=golang:1.16.13-buster /usr/local/go/ /usr/local/go/
WORKDIR /app
COPY . .

RUN apt update && apt install git -y

ENV PATH="/usr/local/go/bin:${PATH}"
ENV GOPATH="/usr/local/go"
RUN pip3 install -r requirements.txt
RUN go install -v github.com/OWASP/Amass/v3/...@master 
RUN go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest 

RUN git clone https://github.com/gwen001/github-subdomains && \
    cd github-subdomains && \
    go build main.go && \
    ln -s $(pwd)/main /usr/bin/github-subdomains

RUN groupadd --gid 8443 app_user \ 
    && useradd --home-dir /home/app_user --create-home --uid 8443 \
    --gid 8443 --shell /bin/bash app_user

RUN chown -R app_user:app_user .
USER app_user

RUN mkdir -p database
CMD ["python3", "autobug.py", "-s", "costco.com"]