#!/usr/bin/bash
set -eux


echo "
LoadModule wsgi_module /usr/lib/apache2/modules/mod_wsgi.so 
WSGIScriptAlias / /root/django-yana/yana/wsgi.py
WSGIPythonHome /root/django-yana/.venv/
WSGIPythonPath /root/django-yana

<Directory /root/django-yana/yana>
<Files wsgi.py>
Require all granted
</Files>
</Directory>" >> "/usr/local/apache2/conf/httpd.conf"
