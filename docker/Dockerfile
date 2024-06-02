FROM httpd:2.4
RUN apt update
RUN apt-get install  --no-install-recommends --yes  \
python3.11/stable \
python3.11-venv \
libapache2-mod-wsgi-py3 \
nano \
less \
make

WORKDIR /root
## configuring apache 


## copying django project files 
RUN mkdir --parents django-yana/yana
WORKDIR /root/django-yana
COPY ./yana .
COPY requirements.txt .
COPY Makefile .
COPY LICENSE .
COPY README.md .
COPY shell ./shell
RUN make init
RUN chmod   755 /root/
RUN chmod   755 /root/django-yana
RUN chmod   755 /root/django-yana/.venv
RUN shell/configure_httpd.sh
RUN ls .
ENTRYPOINT [ "./shell/entrypoint.sh" ]