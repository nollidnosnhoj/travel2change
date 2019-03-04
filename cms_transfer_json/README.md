## Exporting and Importing Django CMS Content

### Please backup your files before doing this. This is not a 100% gurantee.

If you are creating a page in Django CMS, you will need to know how to save the state of your page when using a different version of the repo.

**Prerequisites:**
- Make sure you have the LATEST version of the github repository.
- To ensure you have the latest version, open the requirements.txt and
make sure you have `djangocms-transfer==0.1.0` listed.
- Afterwards, make sure you have djangocms-transfer install.
In your terminal, activate your virtual environment, and type in this
command: `python -m pip install -r requirements.txt` (python3 for mac/linux)
This will install all the packages in the requirements.txt, including
djangocms-transfer

**Procedure:**
- Migrate your database: `python manage.py migrate`
- Run the server: `python manage.py runserver`
- Go to the page and edit the page.
- Left of the placeholder label, there should be a three-bar icon. Click, and the select **Export Plugins**.

![how to export](https://i.imgur.com/yqNfNBL.png)

- A save dialog box should appear. If you have the latest version of the git repo, then there should be a folder called *cms_transfer_json*, alongside the *src* folder.
- To keep the json files organized, use this naming convention: `page_placeholder_plugin.json`.

	- *page* is the name of the page.
	- *placeholder* is the name of the placeholder.
	- *plugin* (optional) is the name of the plugin.
	- For example: If I was to save all the plugins for an about page that has a content placeholder, then I would name the json file: *about_content.json*

- Once saved, then you can import the plugins back by clicking the Import plugins and uploading the json file. 
- Remember to commit your files and changes into your branch.