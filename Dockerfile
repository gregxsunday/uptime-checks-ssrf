FROM python:3.7-slim-buster
RUN adduser --group hacker && adduser --ingroup hacker hacker && apt update && apt install gcc -y
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY add_host.c add_host.c
RUN gcc -o add_host add_host.c && chmod 4755 add_host
COPY . /gcp-ssrf
WORKDIR /gcp-ssrf
RUN chown -R hacker:hacker .
USER hacker
CMD ["./run.sh"]