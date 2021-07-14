docker build . -f Dockerfile -t antispam
docker run -d -p 5000:5000 antispam
