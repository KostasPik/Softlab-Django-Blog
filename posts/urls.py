from django.urls import path

from .views import (activate_newsletter_subscription, 
    buy_coffee,success,checkout, add_comment, 
     contact_us,  home,  
    new_subscriber,  coffee_success,
    post_details, posts,  search,
    )




urlpatterns = [
    path('', home, name="home"),
    path('posts/',posts,name="posts"),
    path('posts/<str:post_slug>', post_details, name="post_details"),
    
    
    
    path('tag/<str:tag_slug>', posts, name="tag_posts"),
    path('new_subscriber/', new_subscriber, name="new_subscriber"),
    path('activate/<str:email>/<str:token>/', activate_newsletter_subscription, name="activate_newsletter"),
    # path('populate/', populate_db, name="populate"),
    # path('populate-courses/', populate_courses, name="populate"),

    # path('delete/', delete_posts, name="delete_posts"),
    path('add_comment/<int:post_pk>/', add_comment, name="add_comment"),
    path('search/', search, name="search"),
    path('contact-us/', contact_us, name="contact_us"),



    #stripe begin
    # path('create_checkout_session', create_checkout_session, name="create_checkout_session"),
    path('buy_coffee/', buy_coffee, name="buy_coffee"),
    path('checkout/', checkout, name='checkout'),
    path('success/', success, name="success"),




    #coffee stripe begin

    path('buy_coffee/', buy_coffee, name="buy_coffee"),
    path('buy_coffee/success/', coffee_success, name="coffee_success"),
    #coffee stripe end
]
