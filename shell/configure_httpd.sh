#!/usr/bin/bash
set -eux


echo "




<VirtualHost *:80>
	DocumentRoot "/root/yana-front/"
	<Directory /root/yana-front>
		Header set Access-Control-Allow-Origin *
		AllowOverride all
		Require all granted

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

<VirtualHost *:81>
<Directory /root/django-yana/yana>
## Modules to make django work with apache
LoadModule wsgi_module /usr/lib/apache2/modules/mod_wsgi.so
WSGIScriptAlias / /root/django-yana/yana/wsgi.py
WSGIPythonHome /root/django-yana/.venv/
WSGIPythonPath /root/django-yana
WSGIApplicationGroup %{GLOBAL}

<Files wsgi.py>
Header set Access-Control-Allow-Origin *
Require all granted
</Files>
</Directory>
</VirtualHost>

" >> "/usr/local/apache2/conf/httpd.conf"
