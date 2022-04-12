# Softlab Django Blog

**Softlab Django Blog** is a ***blog web application*** built on top of the ***Django*** framework.
It has advanced functionalities such as:

 - Dynamically generated Table of Contents for each article (using JavaScript).
 - Integrated Image CDN for faster loading speeds (Boosts SEO). ([Uploadcare](https://uploadcare.com/)).
 - A beautiful WYSIWYG editor for writing articles in the admin panel. ([Ckeditor](https://ckeditor.com/)).
 - Authentication for people who want to become members.
 - Sign Up requires e-mail verification.
 - Password reset capability.
 - Newsletter subscription capability (with e-mail verification).
 - Searching bar for posts.
 - Infinite scrolling (instead of ordinary pagination).
 - Categories for each post. (each post can have multiple categories).
 - Comment section (including reply capability).
 - Donations using the [Stripe API](https://stripe.com/docs/api).
 - "Contact Us" form. (sends form data to email).
 - Administation Panel (requires authentication from a superuser).

**The site is on live display [here](https://djangoblogdisplay.pythonanywhere.com/).**


# Installation

Before you start using the web app you will need to configure a few things in the ***settings.py***.
Firstly, you need an Uploadcare **secret key** and **public key** which you can get by making an account in [here](https://uploadcare.com/) and going to the ***Upload API dashboard***. Secondly, you need a Stripe API key (for accepting donations), which you can get [here](https://stripe.com/docs/api). You also need to include your E-mail **username** ,**password** and **host** in order to be able to automatically send emails. Last but not least, it would be advisable to use [**PostgreSQL**](https://www.postgresql.org/) as your database (SQLite is not really meant to be used in production) .Before setting the blog live for production make sure you install the **[Whitenoise](http://whitenoise.evans.io/en/stable/)** middleware to serve your static files!


# Options

You can enable static files offline compression by going to setting.py and setting the **COMPRESS_ENABLED** field to **True** (*make sure you run **python manage.py compress** afterwards*). You can enable caching by tampering with the **CACHES** field in settings.py.
