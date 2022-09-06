FROM alpine:latest

LABEL Author="Victor Fernandez III, @cyberphor"

RUN apk add --no-cache \
    python3 \
    py3-pip \
    openssl

RUN python3 -m pip install netmiko && \
    mkdir /opt/so2ban/

WORKDIR /opt/so2ban/
 
RUN openssl req -new -x509 -days 365 -nodes -subj \
    /CN="so2ban" \
    -keyout "private.key" \
    -out "public.key"

COPY so2ban.py so2ban.py 

ENTRYPOINT ["python3","so2ban.py","--start"]
