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

## setting up directories holding server files
RUN mkdir --parents django-yana/yana
RUN mkdir --parents yana-front
## copying frontend 
COPY ../yana-frontend/dist /root/yana-front
## copying backend (django project files)
WORKDIR /root/django-yana
COPY ./yana .
COPY requirements.txt .
COPY Makefile .
COPY LICENSE .
COPY README.md .
COPY shell ./shell
RUN make init
RUN chmod   755 /root/
RUN chmod --recursive  755 /root/django-yana
#RUN chmod   755 /root/django-yana/.venv
RUN chmod --recursive 755  /root/yana-front

## configuring apache 
RUN shell/configure_httpd.sh

RUN ls .
ENTRYPOINT [ "./shell/entrypoint.sh" ]
