## Understanding the Project

The framework used in this project is called Django. Django is a web framework designed in Python. Django structures the project into applications, and within each applications are:

- `admin.py` - This is how you configure the admin site for the application. [Docs](https://docs.djangoproject.com/en/2.2/ref/contrib/admin/). 
- `apps.py` - This is to help users to include application configuration for the application. [Docs](https://docs.djangoproject.com/en/2.2/ref/applications/#configuring-applications).
- `forms.py` - This is how forms are created. Think of this file as a helper for creating forms. We need helpers to create forms, especially form that accepts user input, as we cannot trust them as much as we want to. [Docs](https://docs.djangoproject.com/en/2.2/topics/forms/).
- `models.py` - Models are a single, definite source of information about your data. it contains essential fields and behaviors of the data you are storing. [Docs](https://docs.djangoproject.com/en/2.2/topics/db/models/).
- `tests.py` - This is where you can do unit testing for your application. [Docs](https://docs.djangoproject.com/en/2.2/topics/testing/overview/). 
- `urls.py` - This is where the URL dispatcher is stored. This is how a URL is routed to a view. [Docs](https://docs.djangoproject.com/en/2.2/topics/http/urls/). 
- `views.py` - Classes or functions are stored here that takes a web request and returns a web response. [Docs](https://docs.djangoproject.com/en/2.2/topics/http/views/). 

Of course, you can add more files into the application folder, like `mixins.py` or `business-logic.py` .

### Config Folder

The config folder contains settings for the website. It contains a `urls.py` file that acts as a global URL dispatch, instead of an application based URL dispatcher. `wsgi.py` is the primary deployment platform for Django. [Docs](https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/). 

Inside the config folder is the settings folder. This is where all the settings for the project are located.

- `base.py` - The base settings for the project.
- `local.py` - Settings that should be used for development only.
- `production.py` - Settings that should be used for production only.
- `tests.py` - Settings that should be used for testing only.

In each file, most settings should be commented on what it does.

`.env` file is the environment variable file that contains sensitive information.

### Media and Static files

When a user uploads a media to the website, it will be stored in a folder called `media` in the root directory of the project. This is configured in the `base.py` file in the settings folder. [Docs](https://docs.djangoproject.com/en/2.2/topics/files/). 

Static files are files that are not dynamic, like stylesheets, images, and Javascript. The static folder is located in the travel2change folder (not the root directory). [Docs](https://docs.djangoproject.com/en/2.2/howto/static-files/).

![](https://i.imgur.com/Nc8kPga.png)

### Templates

Templates are HTML file that has templating syntax in them that will generate dynamic content for the page. This is how whenever you visit an activity, it contains that activity's information on the page. 

The template should be structured by applications. So if you are creating a template for an activity, you should place that template in the application folder, that is in the templates folder.

![](https://i.imgur.com/jrRdv11.png)

The naming convention for the template also matters. You should name the template `application_typeofview.html` 

Replace `application` with the name of the application, and typeofview with the type of template it is. For instance, if you are creating a template for the activity detail page, the template name should be `activity_detail.html`. 

To learn more about templates, click here: <https://docs.djangoproject.com/en/2.2/topics/templates/>

