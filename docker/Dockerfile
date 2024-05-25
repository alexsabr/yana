FROM httpd:2.4
RUN apt update
RUN apt-get install --yes  \
python3.11/stable \
python3.11-venv \
libapache2-mod-wsgi-py3 \
nano \
less \
make

WORKDIR /root
## configuring apache 
RUN echo "LoadModule wsgi_module modules/mod_wsgi.so" >> /usr/local/apache2/conf/httpd.conf

## copying django project files 
RUN mkdir --parents django-yana/yana
WORKDIR django-yana
COPY ./yana /root/django-yana/yana
COPY requirements.txt .
COPY Makefile .
COPY LICENSE .
COPY README.md .
RUN make .venv