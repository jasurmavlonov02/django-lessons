from django.urls import path

from app.views import index, product_details, order_list, customers, order_details, add_product, customer_details, \
    customer_add, customer_delete, customer_update, category
from app.views.auth import ForgotPassword, LogoutPage, RegisterPage, LoginPage, ActivateEmailView

urlpatterns = [
    path('', index, name='index'),
    path('add-product/', add_product, name='add_product'),
    # path('test/<int:year>/<int:month>/<int:day>', testing, name='testing'),
    path('product-details/<int:product_id>', product_details, name='product_details'),
    path('order-list/', order_list),
    path('order-details/', order_details),

    path('customers/', customers, name='customers'),

    path('customer-details/<int:customer_id>',customer_details,name='customer_details'),
    path('customer-delete/<int:customer_id>',customer_delete,name='customer_delete'),
    path('customer-update/<int:customer_id>', customer_update, name='customer_update'),
    path('customer-add/',customer_add,name='customer_add'),

    path('category/',category,name = "category"),
    path('category/<str:category_slug>', index, name='category_by_slug'),

    path('login/',LoginPage.as_view(),name = "login_page"),
    path('register/',RegisterPage.as_view(),name = "register_page"),
    path('logout/',LogoutPage.as_view(),name = "logout_page"),
    path('forgot-password/',ForgotPassword.as_view(),name = "forgot_password"),
    path('activate/<str:uid>/<str:token>',ActivateEmailView.as_view(),name = "confirm_mail")
]
