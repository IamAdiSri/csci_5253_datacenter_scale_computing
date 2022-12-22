FROM xserrat/facebook-demucs

COPY . /root/app
WORKDIR /root/app

RUN pip install minio redis requests

CMD ["python worker-server.py"]
# CMD ["sleep 1234m"]