# Project_lab

This repository has two main code parts - The notebook ( model.ipynb ) is built to work in the Databricks environment. This notebook contains all the loading, cleaning, training, and saving of our chosen models.
The second part is the scraping code. It uses selenium to navigate the web
 
 in save_israeli_companies_id.py, it finds the id cof comoanies in number_of_pages of linedin, based number_of_pages in the PARAMETERS.py
 
 in profiles, it scrapes the companies for their employees in Israel.
 
 in cleaning, it cleans the URL of the employees.
 

In all parts, the login to LinkedIn is done by the password, and username found in PARAMETERS.py.
