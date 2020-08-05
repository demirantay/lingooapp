<img src="branding/logo.png" height="30" width="30"/>
# linguum
source code of linguum.com


```
# dev setup -- server starting
venv/bin/python manage.py runserver --settings=config.dev_settings

# dev setup -- makemigrations
venv/bin/python manage.py makemigrations --settings=config.dev_settings

# dev setup -- migrate
venv/bin/python manage.py migrate --settings=config.dev_settings

# testing
venv/bin/python manage.py test --settings=config.dev_settings

# show migrations
venv/bin/python manage.py showmigrations --settings=config.dev_settings
```
