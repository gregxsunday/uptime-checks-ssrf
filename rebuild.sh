docker build -t gcp-ssrf .
docker run --rm -p 8000:8000 --name gcp-ssrf gcp-ssrf