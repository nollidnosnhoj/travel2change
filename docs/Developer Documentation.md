# travel2change Developer's Documentation

- Chad Fukumitsu
- Christopher Aranda
- Iokepa Lapera
- Kekoa Sanatana
- Randall Johnson
- Samantha Garcia

# Table of Contents

[TOC]

# Introduction

The purpose of the developer documentation is to assist the developers on the structure of the project, and go through step by step how to deploy the project using Django Europe. 

## Framework

This project uses two frameworks: Django and Django CMS.

Django is a web framework, developed in Python, that is designed to make creating website more structured and easy. A Django project is divided into applications, and within those applications are files that handles various functions, like handling request and responses (`views.py`) or data and behaviors (`models.py`). Django also comes with a nice admin dashboard for handling objects created by the project.

[Django Docs](https://docs.djangoproject.com/en/dev/)

Django CMS is a CMS solution for Django, and allow users (with permissions) to create pages seamlessly, and manage content in those pages. One attractive feature is their page builder. It allows the user to place plugins onto the page that handles dynamic content.

[Django CMS Docs](http://docs.django-cms.org/en/latest/)

## Database

We recommend using PostgreSQL as the choice of database management system, as it works very well with Django. Another suggestion would be MySQL, but this DBMS was not tested.

## Hosting

Django Europe is the recommended hosting, since it handle a lot of the heavy work in running a server for you. Also, the previous website is hosted on Django Europe.

## FareHarbor

FareHarbor is a third party software as a service (SaaS) that handles bookings and payments for events. Travel2change uses this software to handle the bookings for the activities hosted on their website.

The issue with implementing FareHarbor in our project is that FareHarbor does not give out their API to anyone, unless they are a reseller. This means some of the features like sorting by dates is near impossible without a connection to the FareHarbor data server. However, we could still obtain a FareHarbor item ID to display a widget.

# Setup Website

## Setup Hosting

This documentation assumes that the website will be hosted at [Django Europe](https://www.djangoeurope.com).

1. Login to the Django Europe control panel.

2. Click **Installer** on the left sidebar.

3. Click **Django**.

4. Fill out the information.

   1. **Choose a SSH User**. SSH is a protocol that allows a communication between the client and a server to be secured. When you created a Django Europe account, it should comes with a SSH user.

   2. **Database**. It is recommended to use PostgreSQL. Make sure you choose the Database user that has `- psql` on the end. This means that the user uses the PostgreSQL database management system. If you do not see it, on the left sidebar, click Database. Under Database users, click **Add User**. From there, choose your **System User (SSH User)**, choose **PostgreSQL** DBMS, choose whatever **name** and **password**. If the password field is left blank, the password will be auto-generated.

      **WE WILL NOT USE THE DATABASE CREATED BY THE AUTO-INSTALLER. The database will be auto-populated with data that we do not need.**

   3. **Project settings**.

      1. **Project Name** - This is the name of the project. For instance, `Travel 2 Change` .
      2. **Project Slug** - A slug is a human-readable name that is all lowercased, and replaces whitespace with dashes or underscores. This slug will be auto-generated based on the name of the project. For instance, Travel 2 Change to travel-2-change.
      3. **Django version** - Does not matter since we will be uploading our own project. But I would recommend **Django 2.1.X**.

      ![Project Settings](https://i.imgur.com/gxhRfqW.png)

   4. **Django admin**. Fill out the credentials for the admin user. This may not be necessary as we will create a new database.

   5. **Domain**. Choose what domain name you want the project to use. You can also choose a subdomain for this project.

5. Once the information is filled, click **Install**. This will begin the installation process of the Django project. It is okay to leave the window. You will receive an email when the installation is complete.

6. As mentioned before, we will need to create a brand new database for the website, instead of using the auto-created database, since it is populated. *Note, you can use the auto-created database, but you will need to drop all the tables in that database.*

   1. On the left sidebar, click Databases
   2. Under Database list, click Add database
   3. In the Add database modal window, choose the **PostgreSQL user**. Choose a **name**. In Database Type, choose **PostgreSQL**. A new section called **Extensions** will appear. You may not need any of them, but adding **Postgis** will be nice if you decide to add Geolocation to your project. Click **Create**.
      ![Add Database](<https://i.imgur.com/ZgD7UTb.png>)

**If you drop the tables in the database created by the installer, then you could use that database. IF NOT, you will need to create a database with a different name from the one created by the installer.**

Once the project installation is completed, we can now start accessing the server backend remotely either using SSH command-line or a GUI-client called [WinSCP](https://winscp.net/eng/index.php). I would highly recommend WinSCP, but there will be times where we will need to use both command-line and WinSCP.

##  Setting up WinSCP and SSH

In this section, we will walkthrough how to setup WinSCP and how to use SSH on the command line. We will use both of these tools to access and manage the files for our project.

### Setting up WinSCP

1. Download and install [WinSCP](https://winscp.net/eng/download.php).

2. When launching WinSCP, it will ask you to create a new session (login to a server).

   ![WinSCP](<https://i.imgur.com/5xXaV6G.png>)

   1. **File protocol:** SFTP (SSH File Transfer Protocol)

   2. **Host name:** This is where you type the name, or the IP address, of the server you want to connect to. To find out the host name, login to the Django Europe control panel, and click **SSH users**. Find your SSH user and look at the **Server** column.

      ![Host Name](<https://i.imgur.com/NzdiVEp.png>)

   3. **User name:** This is your Django Europe username.

   4. **Password:** This is your Django Europe password. If not, you may need to set it up. Go to the Django Europe control panel, click **SSH users**, click on the **Edit** button under **Actions** (second icon), under **Authentication** is where you can setup/change your account password.

   5. **Port number:** Leave it at **22**. This is the port number that you will be connected to on the server. It is rare to specify the port number, so leaving it as 22 is fine.

3. Once you fill out the session information, save it and login to that session. It may ask you to enter the password.

4. Once you are authenticated, you will have access to the files in the server `\home\your-username\` .

### Access server using SSH

Once the command prompt (Windows) or terminal (Mac or Linux), and enter `ssh username@hostname`. Replace the username with your account username and hostname with the host name or IP address of the server. Afterwards, you will be prompted to enter your account password.

## Pulling Project

Now we need to get the latest travel2change files to the server. But first, let's login to WinSCP. Once you are logged into the remote server, you should be able to see `home/username/` on the right hand side, while the left hand side is your local computer documents.

In `home/username/` , go the project folder. Ex. `home/username/travel2change/`

Next delete the following folders/files:

```
config/
dproject/
imprint/
requirements/
manage.py
```

Let's start pulling the project. There are two ways to do this: uploading using WinSCP, or pulling using Git.

### Upload using WinSCP

Go to [the Github repository](https://www.github.com/nollidnosnhoj/travel2change/)

Click the green button that says "Clone and download" then click "Download ZIP"

![Download Zip](https://i.imgur.com/XEPklBv.png)

Once downloaded, extract the zip file, and open the folder. Inside `travel2change-master` are the contents for the project. These contents need to be uploaded to the server `home/username/project-name/`

To upload these files, drag the files into WinSCP.

![Upload to WinSCP](https://i.imgur.com/G5IRd34.png)

Once it finishes uploading, you have successfully uploaded the project.

### Pull using Git

This may be more difficult, but this is a highly recommended way of uploading the project, as you will be setting up repository for your project

Login to SSH using the command-line. `ssh username@hostname`

![Login to SSH](https://i.imgur.com/N1M3lGo.png)

Type: `cd project-name` - *Note: project-name is the name of your project in slug form (project slug)*

Go to [the project repo](https://www.github.com/nollidnosnhoj/travel2change/) and create a Github account. Afterwards, go back to the repository, and Fork the repo (in the top-right). This will create a clone of the repository to your Github account.

![Fork](https://i.imgur.com/u5sFiBO.png)

Afterwards, go to your forked repo, and click on the Green button "Clone or download" and copy the HTTPS URL. Look something like this:

`https://github.com/your-github-username/travel2change.git`

![Copy repo link](https://i.imgur.com/sM9Kg2B.png)

Go back to your command-line and

Initialize git

```
git init
```

Set your remote URL

```
git remote add origin paste_repo_url
```

To verify that your remote URL is set

```
git remote -v
```

Pull your project

```
git pull origin master
```

You may need to add `--allow-unrelated-histories` at the end.

You have successfully pulled the project using Git

```
git init
git remote add origin your_fork_repo
git remove -v
git pull origin master --allow-unrelated-histories
```

## Configuring Server

Now that the project is in the server, we need to configure the server, so we can start running it.

Login to the server using WinSCP and let's get started.

### Configuring init script

Go to `/home/username/init/`

This directory contains scripts that will either stop or start our server, depending on the arguments. When creating a project through the auto-installer, it actually created these scripts with the project-name already filled in. However, we still need to do some edits to these files so it understands the structure of our project.

On WinSCP, **find the file** that has your `project-name`. **Right click**, and **click Edit**. The internal editor show open up. *The file should not have any file extension.*

```
/home/username/init/project-name
```

![Edit file](https://i.imgur.com/DDvp3cx.png)

*This script control whether the website should start or stop.*

On **line 15**, replace the line with:

```
PYTHONPATH="$HOME/$NAME/project-name:$PROJECT_DIR/project-name"
```

*replace `project-name` with the project slug, or the value of the $NAME variable*

On **line 22**, replace the line with:

```
OPTS="-D -b unix:///$SOCKET --worker-class gevent --workers $WORKERS --pid $PIDFILE config.wsgi:application"
```

### Configuring nginx conf

This is our web server configuration.

Edit `/home/nollidnosnhoj/nginx/conf/sites/project-name.conf`

On **line 20**, replace line with:

```
alias ../project-name/staticfiles/;
```

On **line 23**, replace line with:

```
alias ../project-name/media/;
```

These edits will redirect media and static files to the appropriate directory.

### Enabling Virtual Environment

Time to go to the command-line. Login to the SSH. Once you are logged in, **type**:

```
source ~/.virtualenvs/project-name/bin/activate
```

The virtual environment is a tool that keeps dependencies separate by isolating the environment. This is important when creating our Django project. When activating the virtual environment, the name of the environment `project-name` will be at the beginning of the line, surrounded by parentheses.

![activated virtual environment](https://i.imgur.com/7jUi2yW.png)

Last thing, **go to the project folder**. `cd project-name`

![go to project dir](https://i.imgur.com/m9klnQA.png)

### Installing Requirements

Now we need to install all the packages and dependencies that the project needs. **Enter**: 

```
pip3 install -r requirements/production.txt
```

The command-line should start installing a numerous packages, including Django and Django CMS.

base requirements

```
argon2-cffi==19.1.0
Babel==2.6.0
certifi==2018.11.29
cffi==1.12.2
chardet==3.0.4
defusedxml==0.5.0
Django==2.1.7
# https://django-allauth.readthedocs.io/en/latest/installation.html
django-allauth==0.38.0
django-appconf==1.0.3
# https://django-autoslug.readthedocs.io/en/latest/
django-autoslug==1.9.4
# https://django-axes.readthedocs.io/en/latest/
django-axes==4.5.4
django-classy-tags==0.8.0
# https://github.com/un1t/django-cleanup
django-cleanup==3.2.0
# http://docs.django-cms.org/en/latest/
django-cms==3.6.0
# https://django-crispy-forms.readthedocs.io/en/latest/
django-crispy-forms==1.7.2
# https://django-environ.readthedocs.io/en/latest/
django-environ==0.4.5
# https://django-filer.readthedocs.io/en/latest/
django-filer==1.4.4
# https://django-filter.readthedocs.io/en/master/
django-filter==2.1.0
# https://django-formtools.readthedocs.io/en/latest/
django-formtools==2.1
django-ipware==2.1.0
django-js-asset==1.2.1
# https://django-meta.readthedocs.io/en/latest/
django-meta==1.5.0
# https://django-model-utils.readthedocs.io/en/latest/
django-model-utils==3.1.2
django-mptt==0.9.1
# https://github.com/stefanfoulis/django-phonenumber-field
django-phonenumber-field==2.2.0
django-polymorphic==2.0.3
# https://django-sekizai.readthedocs.io/en/latest/
django-sekizai==0.10.0
# https://github.com/fcurella/django-social-share
django-social-share==1.3.2
django-treebeard==4.3
# https://github.com/divio/djangocms-admin-style
djangocms-admin-style==1.3.0
# https://github.com/divio/djangocms-attributes-field
djangocms-attributes-field==1.0.0
# https://github.com/divio/djangocms-bootstrap4
djangocms-bootstrap4==1.3.1
# https://github.com/divio/djangocms-column
djangocms-column==1.9.0
# https://github.com/divio/djangocms-file
djangocms-file==2.2.0
# https://github.com/divio/djangocms-googlemap
djangocms-googlemap==1.2.0
# https://github.com/divio/djangocms-history
djangocms-history==1.0.0
# https://github.com/divio/djangocms-icon
djangocms-icon==1.2.0
# https://github.com/divio/djangocms-link
djangocms-link==2.3.1
# https://github.com/divio/djangocms-modules
djangocms-modules==0.1.0
# https://djangocms-page-meta.readthedocs.io//en/latest/readme.html
djangocms-page-meta==0.8.5
# https://github.com/divio/djangocms-picture
djangocms-picture==2.1.3
# https://github.com/divio/djangocms-snippet
djangocms-snippet==2.1.0
# https://github.com/divio/djangocms-style
djangocms-style==2.1.0
# https://github.com/divio/djangocms-text-ckeditor
djangocms-text-ckeditor==3.7.0
# https://github.com/divio/djangocms-transfer
djangocms-transfer==0.1.0
# https://github.com/divio/djangocms-video
djangocms-video==2.1.1
# https://github.com/SmileyChris/easy-thumbnails
easy-thumbnails==2.6
entrypoints==0.3
html5lib==1.0.1
idna==2.8
mccabe==0.6.1
oauthlib==3.0.1
phonenumberslite==8.10.6
Pillow==6.0.0
psycopg2==2.7.7
pycodestyle==2.5.0
pycparser==2.19
python-dateutil==2.8.0
python3-openid==3.1.0
pytz==2018.9
requests==2.21.0
requests-oauthlib==1.2.0
six==1.12.0
# https://sorl-thumbnail.readthedocs.io/en/latest/index.html
sorl-thumbnail==12.5.0
sqlparse==0.3.0
Unidecode==1.0.23
urllib3==1.24.2
webencodings==0.5.1
```

local.txt

```
-r ./base.txt # this will add base.txt to this file

flake8==3.7.7
# https://django-debug-toolbar.readthedocs.io/
django-debug-toolbar==1.11
# https://django-extensions.readthedocs.io/en/latest/
django-extensions==2.1.6
pyflakes==2.1.1
```

production.txt

```
-r ./base.txt

# http://docs.celeryproject.org/en/latest/
celery==4.3.0
python-memcached==1.59
# http://docs.gunicorn.org/en/stable/
gunicorn==19.9.0
# https://django-storages.readthedocs.io/en/latest/
django-storages==1.7.1
```

## Configuring Environment Variables

The environment variables are information stored in a file for the virtual environment. This file also contains sensitive information like passwords.

In WinSCP, go to `/home/username/project-name/config/settings/` and **rename** the `.env.example` file to `.env`.

![.env](https://i.imgur.com/PVKyeFd.png)

**Start editing the file**.

There's a lot of variables, but don't worry, we will go through them. When inserting value, remove the brackets [ ].

- `POSTGRES_PASSWORD` - This is the password for the PostgreSQL database.

- `POSTGRES_USER` - This is the username for the PostgreSQL database.

- `POSTGRES_DB` - This is the name of the PostgreSQL database.

- `DATABASE_URL` - This is the URL of the database.
  `postgresql://[POSTGRES_USER]:[POSTGRES_PASSWORD]@127.0.0.1:5432/[POSTGRES_DB]`
  Replace the bracketed variable (don't include the brackets)

  ```
    POSTGRES_PASSWORD=password
    POSTGRES_USER=username
    POSTGRES_DB=username_dbname
    # DATABASE_URL=postgresql://username:password@127.0.0.1:5432/username_dbname
    CONN_MAX_AGE=
  ```

**IMPORTANT: REMOVE THE `#` BEFORE `DATABASE_URL`**

- `DJANGO_SETTINGS_MODULE` - The environment will choose which Django settings module to use.
  `config.settings.production` for production (default)
  `config.settings.local` for development
  `config.settings.tests` for testing
- `SECRET_KEY` - This is the Django secret key, which should be kept secret. You must generate a key [here](https://www.miniwebtool.com/django-secret-key-generator/).
- `DEBUG` - Enabling `DEBUG=True` means that whenever there is an error, it will show debugging information. It should not matter since `DEBUG` is hard coded to `False` in production settings. It would matter for development.
- `DJANGO_ALLOWED_HOSTS` - These are the domains or hosts that the Django project can server. Make sure you replace `[insert domain]` with the domain of your website. It is important to have the `.` in the beginning of the domain.
- `ACCOUNT_ALLOW_REGISTRATION` - Setting it to `True` allow users to register on the website.
- `DJANGO_ADMINS` - These are emails that will be sent emails if the website encountered any exceptions, especially 500 Internal Errors. We provided how to add emails for this variable in the `.env` file.
- `SITE_DOMAIN` - Enter the domain of the website (not including `http://, https://, www.`).
- `GOOGLE_MAPS_API` - Enter your Google Maps API here. This is required.

### Configuring Email

For this project, you will need to setup an email server. This server will be used to send notification emails, error emails, etc. For this instance, we are going to assume you are going to use the email server provided by Django Europe (wservices). You can read more about it [here](<https://panel.djangoeurope.com/faq/send-email>).

To setup an email account on Django Europe, go to the **Django Europe control panel**, and click **E-mails**. Then Click Add under **E-mail accounts**.

- `EMAIL_HOST` - The host name of the email server. `mail.wservices.ch`
- `EMAIL_PORT` - Enter `587`
- `EMAIL_HOST_USER` - Enter the username of the email account. `username@domain`
- `EMAIL_HOST_PASSWORD` - Enter the password for the email account.

**Once you have finished configuring the `.env` file, save it!**

### Example

```
# PostgreSQL Config
# ########################################################################
POSTGRES_PASSWORD=psql_password
POSTGRES_USER=psql_username
POSTGRES_DB=psql_username_dbname
CONN_MAX_AGE=

# DATABASE URLS
# ########################################################################
# Uncomment for Postgres URL (Production)
DATABASE_URL=postgresql://psql_username:psql_password@127.0.0.1:5432/psql_username_dbname

# To uncomment for an SQLite URL (Local/Development)
# DATABASE_URL=sqlite:///db.sqlite3
# URL to have SQLite example and to pass TravisCI
# DATABASE_URL=sqlite:////tmp/db.sqlite3

# General Settings
# ########################################################################
READ_DOT_ENV_FILE=True

# This will choose which setting modules to use.
# 'config.settings.production' for production (live) *default
# 'config.settings.local' for development (local)
# 'config.settings.tests' for testings
DJANGO_SETTINGS_MODULE=config.settings.production

# This is a must. You can generate a secret key here: https://www.miniwebtool.com/django-secret-key-generator/
SECRET_KEY=c^zhj%gg@l06ao0&3y)333#!osnf&zini8)ohgsxt=m4o%=br8
# dont use the secret key above

# This will show debug exception pages. It is recommended to put this as False for production
DEBUG=False

# This represents the host/domain names that the Django website can serve.
DJANGO_ALLOWED_HOSTS=*
DJANGO_ALLOWED_HOSTS=.project-domain.com

# This setting determines if registration is allowed.
ACCOUNT_ALLOW_REGISTRATION=True

# These are the lsit of people that will receive emails about server errors.
# Example:
# DJANGO_ADMINS=John Doe:johndoe@gmail.com, Michael Bay:mikebay@gmail.com, etc.
DJANGO_ADMINS=Johnathan Doeman: johndoe@hotmail.com, Christopher Waltz: chriswaltz@gmail.com

# This is the domain of your website. Needed for the configuration. Do not include http:// or https://
SITE_DOMAIN = project-domain.com

# Security Settings
# ########################################################################
# Security! Better to use DNS for this task, but you can use redirect
SECURE_SSL_REDIRECT=False

# EMAIL
# ########################################################################

# Insert the email host, port, username, and password
# You could use Gmail (not recommended for production), Mailgun, or Django Europe.
EMAIL_HOST=mail.wservices.ch
EMAIL_PORT=587
EMAIL_HOST_USER=admin@project-domain.com
EMAIL_HOST_PASSWORD=email_password

# GOOGLE MAPS API
# ########################################################################

# Insert Google Maps API for Google Maps to work in website
GOOGLE_MAPS_API=a_google_maps_api
```

## Migrating Database

The server is configured, the requirements are installed, and the environment variables are setup, it is now time to migrate the database. This process will create all the tables and structures for the database.

**First thing, ensure that the virtual environment is enabled, and the current directory is the project directory.**

**Enter**: `python3 manage.py migrate --settings=config.settings.production`

![migrate completed](https://i.imgur.com/4l3s9NX.png)

You should see a lot of "Applying" statements. This is currently migrating all the migrations to the database.

The script will begin migrating the database, and applying migrations to the database.

## Configuration Website

*Before you proceed:* Please make sure that the database has been migrated, and the server is up and running.

This section will begin configuring the website, and auto-populating the site with data, like categories, tags, and regions.

But first, a superuser need to be created so you could login to the website, since there is no user in the database.

`manage.py createsuperuser --settings=config.settings.production`

### Creating Sample Data

`setup_site.py`

This script will modify the site name (to travel2change) and site domain (to the SITE_DOMAIN specified in environment variable.)

To run this initial scripts: enter

`manage.py setup_site.py --settings=config.settings.production`

To run this script: enter

`manage.py create_pointvalue.py --settings=config.settings.production`  

### Collect Static Files

This script will collect all the static files (stylesheet, javascript, etc.) found on the project and its dependencies, and place them in the `STATIC_ROOT` specified in `settings` folder so that it could be served to the client when it goes live.

`python3 manage.py collectstatic --settings=config.settings.production`

When asked to overwrite files, type `yes`.

Once collecting the static files is completed, you need to restart the nginx server.

`~/init/nginx restart`

### Installing Memcached

Memcached is a distributed memory caching system that often used to speed up dynamic database-driven website, by caching data and objects in RAM. We will need to install this to boost the speed of the website.

You could also refer to this Django Europe Article: [Memcached Article](<https://panel.djangoeurope.com/faq/memcache>)

First, we need to create an UNIX socket file

`/usr/bin/memcached -s ~/memcached.sock`

Then navigate to `~/init/` and create a `memcached` file. You could do this in WinSCP.

Inside `memcached` , insert this:

```
#!/bin/bash

# Set this to your memcached port and PID file

PORT=XXXX
IP=127.0.0.1
PIDFILE=~/memcached.pid
```

```
# Do not change anything below unless you know what you do

DAEMON=/usr/bin/memcached
NAME="memcached"
PATH=/sbin:/bin:/usr/sbin:/usr/bin
OPTS="-s ~/memcached.sock -d -P $PIDFILE"
#OPTS="-l $IP -p $PORT -d -P $PIDFILE" # Uncomment this line that memcache lists on a TCP port

fail () {
    echo "failed!"
    exit 1
}

success () {
    echo "$NAME."
}

case "$1" in
  start)
      echo -n "Starting $NAME: "
      if start-stop-daemon --start --quiet --pidfile $PIDFILE --exec $DAEMON -- $OPTS ; then
        success
      else
        fail
      fi
    ;;
  stop)
      echo -n "Stopping $NAME: "
      if start-stop-daemon --stop --quiet --oknodo --retry 30 --pidfile $PIDFILE --exec $DAEMON ; then
        success
      else
        fail
      fi
    ;;
  reload)
      echo -n "Reloading $NAME configuration: "
      if ! eval "$DAEMON -t $OPTS" > /dev/null 2>&1; then
        eval "$DAEMON -t $OPTS"
        fail
      fi
      if start-stop-daemon --stop --signal 2 --oknodo --retry 30 --quiet --pidfile $PIDFILE --exec $DAEMON; then
        if start-stop-daemon --start --quiet --pidfile $PIDFILE --exec $DAEMON -- $OPTS ; then
          success
        else
          fail
        fi
      else
        fail
      fi
    ;;
  restart)
      $0 stop
      [ -r  $PIDFILE ] && while pidof memcached |\
          grep -q `cat $PIDFILE 2>/dev/null` 2>/dev/null ; do sleep 1; done
      $0 start
    ;;
  *)
      echo "Usage: $0 {start|stop|restart|reload}"
      exit 1
esac
```

In `PORT=XXXX` , replace `XXXX` with the nginx port. You can find it in the Django Europe Control Panel. Select Ports on the sidebar.

![Find that port number](https://i.imgur.com/4bL8xBM.png)

Save the file

Then enter: `chmod +x ~/init/memcached`

Now we can run memcache by entering:

`~/init/memcached start`

### Running the Server

Now we have setup everything, we can actually start running the server. In the command-line, enter:

`~/init/project-name restart`

This will restart the server, since it was running the whole time. You can now enter your website by entering your domain, and you should be treated with this:

![Django CMS Login](https://i.imgur.com/YbhfQUe.png)

Remember that superuser we created, use that to login.

We have now successfully logged in!

![Login Successful](https://i.imgur.com/rzZd3ew.png)

Now let's setup some pages, and an application.

### Setting Up Pages

The objective for this section is to create a homepage, and hook our activities application to Django CMS.

To create a homepage, click on **New Page**.

In **Title**, enter `Home` , and then click Create in the bottom right.

![Create Homepage](https://i.imgur.com/QEOu5DY.png)

Once you create the homepage, you will receive a server error. **This is normal**, because we need to create another page that hooks our activities application to Django CMS. And the homepage possesses contents that looks for the activities app.

In your web browser, go to `http://domain.name/admin` (Go to the Django admin)

You are now in the Django admin page. Under **Django CMS** click **Pages**.

![Pages](https://i.imgur.com/um2XDPl.png)

You are presented with the Django CMS Page Tree.

![Pages](https://i.imgur.com/SNnqqLz.png)

As you can see, the Home page we created is actually the homepage, as indicated by the Home icon next to View.

Let's get rid of that nasty server error on the homepage, and create a **New Page**.

For this page, title should be `Activities` . Also make sure the slug is `activities`

Click **Save and continue editing**.

On the bottom, click **Advanced Settings**

There should be a dropdown menu called **Application**. Choose `Activity Apphook`.

The activity application has a Django CMS apphook so that Django CMS knows that this application exists.

A new field called `Application Instance Name` should appear, but just leave it as is `activities`.

![Activity Apphook](https://i.imgur.com/Q4gyNv2.png)

Click **Save**

Now we need to publish the Activities page.

In the **Page Tree**, on the **Activities** Row, **EN** column, click the **gray circle**, and then click **Publish**.

![Activities Publish](https://i.imgur.com/pNyRaup.png)

We have successfully publish the activities page, but we are not done yet. We need to reset the server. Now, Django CMS states that it does it automatically, but we like to make sure.

In your command-line, enter:

`~/init/project-name restart`

Go back to the website, and you are now greeted with a nice homepage with a nice search bar.

![WOW HOMEPAGE](https://i.imgur.com/z3Rdd9H.jpg)

# Importing Data

In the project, we added a feature called `django-import-export` where it allow you to import spreadsheet that contains data that can be imported into a Django model. Export will allow you to export a Django model into a spreadsheet.

You can either import/export:

- Category
- Region
- Tag
- Activity

Catogory, Tag, and Region will import and export these fields:

- id *(unique)*
- name
- slug *(alphanumeric, no whitespace, dashes and underscores okay)*

Activity will import and export these fields:

- id *(unique)*
- title
- host *(host primary key, host must exist in db)*
- slug *(alphanumeric, no whitespace, dashes and underscores okay)*
- description
- highlights *(new line = new item)*
- requirements *(new line = new item)*
- region *(region name, region must exist in db)*
- tags *(tag name, separated by commas, tag must exist in db)*
- categories *(category name, separated by commas, category must exist in db)*
- address
- latitude *(must be 9 digits, and 6 decimals places)*
- longitude *(must be 9 digits, and 6 decimals places)*
- price *(must be positive number)*
- fh_item_id *(must be positive integer)*
- status *(either approved, unapproved, or inactive)*

Let's import Regions as an example

## Creating the Spreadsheet

Create the spreadsheet, and make sure the columns are in the exact order as the fields listed above.

![region spreadsheet](https://i.imgur.com/JfKr6V0.png)

Notice that the slug column, the data has no whitespaces, but instead replaced with hypens. You could also leave it blank, and it will auto-generate a slug.

Also, I added no data under the id column, because that will get auto-generated.

## Import Data

Go to the Region object in the Django admin. Click on Import left of the Add Region button.

Choose the spreadsheet, and select the format of the spreadsheet you are uploading.

![import](https://i.imgur.com/cW3CF2T.png)

Click Submit, and it will take you to a preview of the new data being imported. Click Submit, and your new regions should be created.

## Importing Activity Data

Importing activity data is a bit tricky because there are four relational keys: host, region, tags, and categories.

To add data in the host column, you need to enter the primary key (id) of the host. You can find the pk by viewing the Hosts in the Django admin, and the pk column should be the most left column.

For region, you need to enter the slug of the region. You can find that out in the Region section in Django admin.

For categories, you need to enter the slug of the region. If there's more than one, separate each with a whitespace.

Same with the tags.

**The host, region, categories, and tags data in the spreadsheet must exist in the website's database**

For requirements and highlights, you cannot add new line (unless maybe you could in Excel). If not, add some sort of separator to remember, and when you manual edit the activity, change the separator to a new line.

*We have not fully tested importing Activity data*

## Example spreadsheets

You can locate some example spreadsheets for tags, regions, and categories located in:

```
/spreadsheets/
```

## Customize Import-Export

All the import and exports are located in:

```
/travel2change/activities/admin.py
```

[Refer to the Django Import Export Documentation](https://django-import-export.readthedocs.io/en/latest/)

## Exporting Data

Now let's export the regions. Click Export next to the Add region button. Then choose a format for your spreadsheet. Click submit, and download the file.

# Development

You have set up the website. Congratulations!

Now, what if you want to make changes to the project. Well, you can!

You can setup a development environment on your local machine (computer) so you can setup a development server to do testing and updating.

## Prerequisites

- Python 3.6+
  - To install Python onto your local computer, [read here](https://tutorial.djangogirls.org/en/python_installation/).
- Git
  - <https://gitforwindows.org/>
  - Git should come installed with Mac or Linux
  - <https://desktop.github.com/> - GitHub GUI

Create a folder somewhere in your computer where the development should take place.  For instance: `C:\Development\`

## Create virtual environment

This tutorial does a very good job explaining how to setup virtual environment.

[](https://tutorial.djangogirls.org/en/django_installation/#virtual-environment)

Make sure you activate your virtual environment.

## Pull from Github

If you forked the project into your own Github account, copy the repository link of your forked repo.

In your development directory on your local machine, initialize git: `git init`. This will initialize your local git repository.

Add your repository to your remote URL: `git remote add origin <paste_here>`

You can verify if it added by: `git remote -v`

Pull the project: `git pull origin master`

What pull does is that brings all the files to your local repo and merge the existing files.

### Note, that this process is a lot easier using Github Desktop

<https://help.github.com/en/desktop/getting-started-with-github-desktop>

You could also just download the project from the project repository, and just place the files into your development directory.

## Install Requirements

Go to the directory that contains `manage.py` and enter:

`python -m pip install -r requirements/local.txt`

We are using local.txt because this is for local development, which this text file contains debugging packages.

## Setup ENV for Development

Rename `config/settings/.env.example` to `config/settings/.env`

Start editing the `.env` file.

Remove `#` in: `# DATABASE_URL=sqlite:///db.sqlite3`

In `DJANGO_SETTINGS_MODULE` , it should be

```
DJANGO_SETTINGS_MODULE=config.settings.local
```

Generate secret key for `SECRET_KEY`. [Generate key here.](​https://www.miniwebtool.com/django-secret-key-generator/)

Make sure `DEBUG=True`

Replace `DJANGO_ALLOWED_HOSTS=[insert domain]` with

```
DJANGO_ALLOWED_HOSTS=.127.0.0.1
```

`SITE_DOMAIN` should be `SITE_DOMAIN=127.0.0.1:8000`

Insert your Google Maps API in `GOOGLE_MAPS_API`

## Lastly

Migrate your database: `python manage.py migrate`

and create superuser: `python manage.py createsuperuser`

and create initial data: `python manage.py create_init_data`

You can now `python manage.py runserver` but you will need to setup website. Refer to **0.7 Configuring Website**

# Understanding the Project

The framework used in this project is called Django. Django is a web framework designed in Python. Django structures the project into applications, and within each applications are:

- `admin.py` - This is how you configure the admin site for the application. [Docs](https://docs.djangoproject.com/en/2.2/ref/contrib/admin/).
- `apps.py` - This is to help users to include application configuration for the application. [Docs](https://docs.djangoproject.com/en/2.2/ref/applications/#configuring-applications).
- `forms.py` - This is how forms are created. Think of this file as a helper for creating forms. We need helpers to create forms, especially form that accepts user input, as we cannot trust them as much as we want to. [Docs](https://docs.djangoproject.com/en/2.2/topics/forms/).
- `models.py` - Models are a single, definite source of information about your data. it contains essential fields and behaviors of the data you are storing. For instance, in the activities application, there is a `models.py` which contains data and behaviors for categories, regions, tags, and, of course, activities.
  However, when you make a change to a model, like the field types or options, you must make a migration by entering: `python manage.py makemigrations app-name`. `app-name` is the name of the application that has the modified `models.py`. Running this command will create a migration file in the application's migration folder. [Docs](https://docs.djangoproject.com/en/2.2/topics/db/models/). **It is important to not remove these migrations since they will depend on other migrations. Remove a migration that another migration depends on will break the migration.**
- `tests.py` - This is where you can do unit testing for your application. This is great for testing an individual component of the project, like applications. We have used this for testing, but removed it from the project. [Docs](https://docs.djangoproject.com/en/2.2/topics/testing/overview/).
- `urls.py` - This is where all the URL routing goes. The module will map a URL path expression (usually regex expression), to a function or class-based view. [Docs](https://docs.djangoproject.com/en/2.2/topics/http/urls/).
- `views.py` - These are classes or functions that takes a Web request and returns a Web response. This response can be a HTML page, redirect, error page, or an image. [Docs](https://docs.djangoproject.com/en/2.2/topics/http/views/). For this project, we primarily used class-based views since it is easier to configure, but may be difficult to follow. [Docs](https://docs.djangoproject.com/en/2.2/topics/class-based-views/).

Of course, you can add more files into the application folder, like `mixins.py` or `business-logic.py` .

## Config Folder

The config folder contains settings for the website. It contains a `urls.py` file that acts as a global URL dispatch, instead of an application based URL dispatcher. `wsgi.py` is the primary deployment platform for Django. [Docs](https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/).

Inside the config folder is the settings folder. This is where all the settings for the project are located. Most (if not all) of the settings in these files are commented to describe what they do. You can also import settings into another application by `from django.conf import settings`.

- `base.py` - The base settings for the project.
- `local.py` - Settings that should be used for development only.
- `production.py` - Settings that should be used for production only.
- `tests.py` - Settings that should be used for testing only.

In each file, most settings should be commented on what it does.

`.env` file is the environment variable file that contains sensitive information.

## Media and Static files

When a user uploads a media to the website, it will be stored in a folder called `media` in the root directory of the project. This is configured in the `base.py` file in the settings folder. [Docs](https://docs.djangoproject.com/en/2.2/topics/files/).

Static files are files that are not dynamic, like stylesheets, images, and Javascript. The static folder is located in the travel2change folder (not the root directory). [Docs](https://docs.djangoproject.com/en/2.2/howto/static-files/).

![Media and Static folders](https://i.imgur.com/Nc8kPga.png)

## Templates

Templates are HTML file that has templating syntax in them that will generate dynamic content for the page. This is how whenever you visit an activity, it contains that activity's information on the page.

The template should be structured by applications. So if you are creating a template for an activity, you should place that template in the application folder, that is in the templates folder.

![Templates folder](https://i.imgur.com/jrRdv11.png)

The naming convention for the template also matters. You should name the template `application_typeofview.html`

Replace `application` with the name of the application, and typeofview with the type of template it is. For instance, if you are creating a template for the activity detail page, the template name should be `activity_detail.html`.

Inside the templates, you can add context variables or built-in template tags that can truly make your webpages more dynamic.

To learn more about templates, click here: <https://docs.djangoproject.com/en/2.2/topics/templates/>

## travel2change Applications

**Activities** - Application that handles the activities in the project. This allows user to create, modify, view, and delete activities.

**Favorites** - Application that handles all the favoriting of activities. This allow users to favorite activities.

**Moderations** - Application that handles the moderation of the activities. This allows for users with permissions to moderate activities.

**Reviews** - Application that handles the reviews for each activity. This allows users to create a review for an activity.

**Points** - Application that handles the points system.

**Users** - Application that handles all the users and hosts. The user is a custom user model that only accepts an email address (not a username).

<https://docs.djangoproject.com/en/2.2/topics/auth/customizing/#specifying-a-custom-user-model>

**To create a new application, enter this in the command line:**

`python manage.py startapp app-name`

You may need to move the app folder from the root to travel2change folder.

## Updating models.py

If you modify an application's `models.py`, then you will need to make a migration of this change. Migrations are Django's way of propagating changes you made to the models into your database schema. In your local environment (assuming your virtual environment is enabled), enter:

`python manage.py makemigrations app-name`

*replacing app-name with the name of the application*

This will create a migration file in the application's migration folder. As mentioned before, do not remove any of the migration files since another migration may depend on it.

However, you will need to apply these migrations into the database, enter:

`python manage.py migrate`

To see all your migrations: `python manage.py showmigrations`

If you want to reset your migrations, you can refer to [this article](https://simpleisbetterthancomplex.com/tutorial/2016/07/26/how-to-reset-migrations.html).

<https://docs.djangoproject.com/en/2.2/topics/migrations/>

## Django CMS

Django CMS is a CMS framework for Django that allows for content management. While Django CMS is great for frontend work, it is also very developer friendly, allowing developers to customize Django CMS through code.

In this project, we implemented Django CMS apphook, plugin, and wizard to the activities application.

An apphook allows to attach a Django application (activities) to a Django CMS page.

A plugin is a convenient way to integrate content from another application (activities) into a Django CMS page. For example, there are three CMS plugins in the activities application: Featured Activities, Regions Plugin, and Latest Activities (you can read more in the user documentation). These are plugins you can attach to a Django CMS page using the drag-and-drop builder.

A wizard allows the content editors (those who can edit content in the Django CMS pages) to add new contents, like an activity. It just provides a simplified workflow.

If you want to learn more about Django CMS, please take a look at their documentation, as it is very well written.

<http://docs.django-cms.org/en/latest/>

# Updating Project

## Use Git to Update Project

If you use the git method for pulling the project to the server, then it is highly recommended to use git to update your project. You can pull the project to your local computer by doing the same as pulling to the SSH server.

After you are done updating the project, make sure you commit your changes and push it into your fork repository. Then when you login to the SSH server, you can pull your fork repo to the server just like you did before.

## Just Upload the Files using WinSCP

You can do the development in your local machine, and when you want to update the site, you can just upload the updated files in the project folder in WinSCP.

## Migrating

Ensure that the virtual environment is enabled.

If you have updated a model and already created the migration file, you will need to migrate the migrations to the database. Enter this on the SSH server:

`python3 manage.py migrate` - *assuming the current directory is the project folder*

## Collect Static Files Again

Ensure that the virtual environment is enabled.

If you updated a style sheet, static image, or anything in the static folder, you will need to collect the static file again. Enter this on the SSH server:

`python3 manage.py collectstatic` - *assuming the current directory is the project folder*

## Restart the Server

When you update the project, and pull it to the server. The server will need to be reset, as well as the memcached.

`~/init/memcached restart`

`~/init/project-name restart`

# Reward Points System

The reward point system is very simple, and does not have much complexity. The points app has two models: `PointValue` and `AwardedPoint`.

- **Point Value** stores a string key and an integer that represents points.
- **Awarded Point** stores data about the awarded points. It stores the targeted user instance, a point_value instance, a reason, a integer that represents points, and a timestamp.

## Helper Functions

`award_points(target, key, reason="")`

**Parameters**:

- target - must be an instance of the user model. This is who will be awarded the points.
- key - Can either be an integer or string. If it is an integer, then it will represent that amount of points the user is awarded. If it is a string, then the function will lookup keys in the Point Value table, and get the value that corresponds to the string as the points that will be awarded.
- reason - reasons for awarding points.

Call this function where you want to award points to a target user. For instance, if you want to award points to users who have favorited an activity, you would call this function after (or before) the user favorites the activity.

```python
def favorite_item(self, user, item):
    fav = Favorite(user=user, item=item)
    fav_reason = "{0} favorited {1}".format(user.name, item.title)
    award_points(user, 'favorite', reason=fav_reason)
    return fav
```

*Please do not use this example, as it is just an example*

Notice that in the key parameter we used a string. That means there has to be a Point Value record with the 'favorite' key. If there isn't a point value that does not have the key parameter, then no points will be awarded, and the reason will explain why.

`unaward_points(target, key)`

**Parameters**:

- target - must be an instance of the user model. This is who will be unawarded points.
- key - Can either be an integer or string. If it is an integer, then it will represent the amount of points the user is unawarded. If it is a string, then the function will lookup keys in the Point Value table, and get the value that corresponds to the string as the points that will be unawarded.

Call this function where you want to take away points from the target user. This should generally be used if an object that awarded the creator points was deleted by the user. Using the same example above, you would call this function when the user unfavorites an activity.

```python
def unfavorite_item(self, user, item):
    fav = Favorite.objects.get(user=user, item=item)
    fav.delete()
    unaward_points(user, 'favorite')
    return somewhere
```

Notice that we use 'favorite' as the key parameter. It is recommended to keep the key parameter consistent. If you award points for favoriting an item, and it uses the key 'favorite', then unawarding points should also use 'favorite'.

The admin/staff could create Point Value objects in the Django Admin.

## Show User's Points

```python
def points_awarded(target):
    """
    This will sum up points in all the AwardedPoint object that targets the target param.
    Paramters:
        target (AUTH_USER_MODEL)
    """
    if not isinstance(target, get_user_model()):
        raise ImproperlyConfigured("Target parameter needs to be a AUTH USER model")
    qs = AwardedPoint.objects.filter(target=target)
    p = qs.aggregate(models.Sum("points")).get("points__sum", 0)
    return 0 if p is None else p
```

The `points_awarded(target)` will return the amount of points the target user has. As shown, it will accumulate all the points in AwardedPoint object that has the target user. 

If you want to show this on a template, go to a view, and modify the context_data

```python
class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'users/user_update.html'
    # self.object is a current user instance
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from points.models import points_awarded
        context['user_points'] = points_awarded(self.object)
        return context
```

We imported `points_awarded` from `points.models` and return the function in the context dictionary.

So when we go to our templates, we can call the context key to call the function.

```html
<div class="card">
    <h5 class="card-header">{% trans "Reward Points" %}</h5>
    <div class="card-body">
        Points: {{ user_points }}
    </div>
</div>
```

We call `{{ user_points }}` to display the number of points. This will only work on templates that are linked to the view that has the `user_points` context.

**Please note that this is not in the project, you will have to implement this on your own.**

## Import Required PointValue data

In the project, we added `awarded_points` whenever the user created a review, and added a photo with it.

The keys used are `review_create` and `review_photo`. If the key does not link to a PointValue, the user will not receive any points, so we need to create two PointValue objects that keys `review_create` and `review_photo`.

Luckily, in the spreadsheet folder, we have created a spreadsheet that you can import to create the two objects. If you do not know what importing does, please refer to 07.1

## Example from the project

In the project, when a review is created or deleted, it will either add or remove points respectively from the target user. We done this using signals.

In /reviews/signals.py

```python
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from points.models import award_points, unaward_points
from .models import Review

@receiver(post_save, sender=Review)
def award_points_for_review(sender, instance, created, **kwargs):
    """ Award points when a review is created """
    if created:
        award_points(instance.user, 'review_create')
        # if the review has a photo when created, award points
        if instance.photo:
            award_points(instance.user, 'review_photo')


@receiver(pre_delete, sender=Review)
def unaward_points_for_review(sender, instance, using, **kwargs):
    """ Unaward points when a review is deleted """
    unaward_points(instance.user, 'review_create')

```

When a review is saved, it will send a signal to the `award_points_for_review` method to call. If the review was created, it will reward points to the user. When the review is created, it will also check if a photo was uploaded.

Same with deleting a review; however, we a signaling the function before it is deleted, so we can access the instance.

Read more about Django Signals:

<https://simpleisbetterthancomplex.com/tutorial/2016/07/28/how-to-create-django-signals.html>

<https://docs.djangoproject.com/en/2.2/topics/signals/>

# Miscellaneous

## Misc Settings

The `settings` folder contains all the settings for the project. These settings are commented on what it does.

### Error Pages

If you encounter an error page (404, 500, etc.), you will encounter our custom error page. Of course you can change it in the templates folder. You should see template entitled `404.html`, `500.html`, etc.

### Max File Size of Photos

Some image field has a validator that validates the size of the image.

Go to `activities/validators.py`

```python
def validate_image_size(image):
    # validate image size
    file_size = image.file.size
    limit_mb = 3  # change here
    if file_size > limit_mb * (1024 * 1024):
        raise ValidationError('File Size Must be below {0} MB'.format(limit_mb))
```

If you want to change the limit from 3 MB, change the `3` to whatever number. Just be aware of your storage space.

## Moderation Email Templates

When an activity is approved or disapproved, an email is sent to the host. You can edit the template at:

`templates/moderations/templates/`

## Backups

[Django supports backups.](https://panel.djangoeurope.com/faq/backup)

### Database Backup

Login to Django Europe control panel.

Go to the Database page.

Click Show All, and click on the database name.

![go to db](https://i.imgur.com/DVFU6eb.png)

This will take you to phpPgAdmin, a web control panel of PostgreSQL.

Click Servers, then click PostgreSQL on the table.

![login to postgres](https://i.imgur.com/ecyVRZO.png)

Login to using your database username and password.

Click on the database name, click Export, check Structure and data, check Download, and submit.

![export db](https://i.imgur.com/CagIFCD.png)

This will create a .sql file. You can import it back using the SQL link between Schemas and Find.

## Storages

Right now, all the static, media, and upload files are stored in the server. Although this is fine, when the site starts to scale, and more people are hosting activities, the server may slow down because of the amount of images and uploads.

If you want to upgrade your storage, you could invest in cloud storage. We have added `django-storages` to the requirements so you can get started.

<https://github.com/jschneier/django-storages>

## Celery

Celery is an asynchronous task queue based on distributed message passing. Celery could be used to do tasks asynchrounous, so the client can do other things instead of waiting for the task to finish.

We added added celery into the production.txt requirements. But celery also requires RabbitMQ, which Django Europe offers.

If you are interested, you can read more here: https://simpleisbetterthancomplex.com/tutorial/2017/08/20/how-to-use-celery-with-django.html

# Resources

Thank you for allowing us to create the website for you. We cannot fit a lot of the information about the tools and frameworks we used into this documentation, then it would be a lot to read. I tried by best to add information that is essential to the deployment of the project. So, I decided to add some links if you want to learn more. These articles and documentations are very high quality.

If you have any questions about the project, or found errors in the documentation, let us know!

## Django

<https://docs.djangoproject.com/en/2.2/> (Please note, this project uses Django 2.1)

## Django CMS

<http://docs.django-cms.org/en/latest/>

## Django Europe (Hosting)

<https://panel.djangoeurope.com/support>

<https://panel.djangoeurope.com/faq>

## Git and Github

<https://guides.github.com/>

## WinSCP

<https://winscp.net/eng/docs/start>