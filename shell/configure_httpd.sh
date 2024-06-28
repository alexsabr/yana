#!/usr/bin/bash
set -eux


echo "
## Module to make django work with apache
LoadModule wsgi_module /usr/lib/apache2/modules/mod_wsgi.so

## Configuration to make backend's django use the  venv
WSGIPythonHome /root/django-yana/.venv/
WSGIPythonPath /root/django-yana
WSGIApplicationGroup %{GLOBAL}
## Set to global otherwise numpy will not work !



<VirtualHost *:80>
	DocumentRoot \"/root/yana-front/\"
	<Directory /root/yana-front>
		Header set Access-Control-Allow-Origin *
		AllowOverride all
		<Files *>
		Require all granted
		</Files>
		Options indexes FollowSymLinks Multiviews

		<IfModule mod_rewrite.c>
		  RewriteEngine On
		  RewriteBase /
		  RewriteRule ^index.html$ - [L]
		  RewriteCond %{REQUEST_FILENAME} !-f
		  RewriteCond %{REQUEST_FILENAME} !-d
		  RewriteRule . /index.html [L]
		</IfModule>
	</Directory>
</VirtualHost>

Listen 81
<VirtualHost *:81>
## put WSGIScriptAlias inside a virtual host else every virtualhost will be treated as backend !
WSGIScriptAlias / /root/django-yana/yana/wsgi.py

<Directory /root/django-yana/yana>


<Files wsgi.py>
Header set Access-Control-Allow-Origin *
Require all granted
</Files>
</Directory>
</VirtualHost>

" >> "/usr/local/apache2/conf/httpd.conf"
