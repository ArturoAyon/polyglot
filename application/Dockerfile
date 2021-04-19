FROM python:3.6
COPY . /app
WORKDIR /app
RUN apt-get install bash 
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["/bin/bash", "entrypoint.sh"]