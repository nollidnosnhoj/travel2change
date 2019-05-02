## Misc Settings

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

## Error Pages

If you encounter an error page (404, 500, etc.), you will encounter our custom error page. Of course you can change it in the templates folder. You should see template entitled `404.html`, `500.html`, etc.
