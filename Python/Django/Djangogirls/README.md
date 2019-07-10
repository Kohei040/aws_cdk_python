Django学習用
============

# Operating environment
- Amazon Linux 2
- Python 3.7.0rc1
- Django 2.1.4
※When using Django 1 system with python3.7,the following error appeared
```
Generator expression must be parenthesized
```

# Django Installation procedure for Linux(Mac)
```
# Crete Working directory
mkdir djangogirls
cd djangogirls

# Create virtual environment
python3 -m venv myvenv
source myvenv/bin/activate
---
(myvenv) [user@server djangogirls]$
---

# Django installation
pip install --upgrade pip
pip install django
```

# Django's project crteation
```
# Create project
django-admin startproject mysite .
tree mysite/
---
mysite/
├── __init__.py
├── settings.py
├── urls.py
└── wsgi.py
---

# Changing Settings
vi mysite/settings.py
---
#LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'ja-JP'
#TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Tokyo'
#USE_TZ = True
USE_TZ = False
---

# Setup a database
---
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying sessions.0001_initial... OK
---

# Running Web Server
python manage.py runserver
---
Performing system checks...
System check identified no issues (0 silenced).
December 10, 2018 - 12:58:37
Django version 2.1.4, using settings 'mysite.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
---
```

# Memo
- When starting up in a non-local environment, specify the IP address at startup.
```
python manage.py runserver xx.xx.xx.xx:8000
```
- If an error 'DisallowedHost at/ Invalid HTTP_HOST header:~',
  add the IP address to 'ALLOWED_HOSTS' of 'mysite/settings.py'.
```
## mysite/settings.py
ALLOWED_HOSTS = ['xx.xx.xx.xx']
```

# Reference
- workshop_tutorialJP
https://djangogirlsjapan.gitbook.io/workshop_tutorialjp/

