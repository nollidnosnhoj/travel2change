## Updating Project

### Use Git to Update Project

If you use the git method for pulling the project to the server, then it is highly recommended to use git to update your project. You can pull the project to your local computer by doing the same as pulling to the SSH server. 

After you are done updating the project, make sure you commit your changes and push it into your fork repository. Then when you login to the SSH server, you can pull your fork repo to the server just like you did before.

### Just Upload the Files using WinSCP

You can do the development in your local machine, and when you want to update the site, you can just upload the updated files in the project folder in WinSCP.

### Updating models.py

If you have updated a model and already created the migration file, you will need to migrate the migrations to the database. Enter this on the SSH server:

`python3 manage.py migrate` 

*assuming the current directory is the project folder*

### Collect Static Files Again

If you updated a style sheet, static image, or anything in the static folder, you will need to collect the static file again. Enter this on the SSH server:

`python3 manage.py collectstatic`

*assuming the current directory is the project folder*

### Restart the Server

When you update the project, and pull it to the server. The server will need to be reset, as well as the memcached.

`~/init/memcached restart`

`~/init/project-name restart`

