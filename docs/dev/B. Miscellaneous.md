## Backups

Django supports backups.

https://panel.djangoeurope.com/faq/backup

### Database Backup

Login to Django Europe control panel.

Go to the Database page.

Click Show All, and click on the database name.

![](https://i.imgur.com/DVFU6eb.png)

This will take you to phpPgAdmin, a web control panel of PostgreSQL.

Click Servers, then click PostgreSQL on the table.

![](https://i.imgur.com/ecyVRZO.png)

Login to using your database username and password.

Click on the database name, click Export, check Structure and data, check Download, and submit.

![](https://i.imgur.com/CagIFCD.png)

This will create a .sql file. You can import it back using the SQL link between Schemas and Find.

