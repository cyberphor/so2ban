FROM ghcr.io/security-onion-solutions/python:3-slim

RUN pip3 install netmiko

RUN mkdir /opt/so2ban/

RUN openssl req -new -x509 -days 365 -nodes \
    -subj /C="US"/ST="Washington"/L="Tacoma"/O="cyberphor"/OU="NETDEF"/CN="so2ban" \
    -keyout "/opt/so2ban/private.key" \
    -out "/opt/so2ban/public.key"

COPY so2ban.py /opt/so2ban/so2ban.py 

WORKDIR /opt/so2ban/

ENTRYPOINT ["python3","so2ban.py","--start"]
