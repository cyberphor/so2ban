FROM ghcr.io/security-onion-solutions/python:3-slim

RUN pip3 install netmiko

RUN mkdir /opt/so2ban/

WORKDIR /opt/so2ban/

RUN openssl req -new -x509 -days 365 -nodes -subj /CN="so2ban" -keyout "private.key" -out "public.key"

COPY so2ban.py so2ban.py 

ENTRYPOINT ["python3","so2ban.py","--start"]