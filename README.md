# MOBHUB-ecommerce

An e-commerce app made using django 3, sqlite and bootstrap 5.
This app also uses several other packages like -

- django-crispy-forms
- django-filter
- pillow
- easy-thumbnails
- dj-database-url

In this app admin can manage products and orders and a customer can simply register, add items to cart and then place an order, customer can also generate an invoice of his order.

To run this app on your local machine you can simply follow the instructions given below.

Firstly create a virtual environment for this project by running this command:
```shell
pip install virtualenv
```
```shell
virtualenv env
```
```shell
env\Scripts\activate
```

Now To install dependencies you can run

```shell
pip install -r requirements.txt
```

To create superuser run this command:

```shell
python manage.py createsuperuser
```

and then enter your username, email and password.

To make migrations :

```shell
python manage.py migrate
```

To run server :

```shell
python manage.py runserver
```

After starting server go to your web browser and visit http://localhost:8000/store and for admin module visit http://localhost:8000/admin and login using superuser credentials.
