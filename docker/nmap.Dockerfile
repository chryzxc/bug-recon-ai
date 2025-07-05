FROM instrumentisto/nmap

RUN apk update && apk add --no-cache ca-certificates
