from django.urls import path, include
from .views import RegisterView

urlpatterns = [
    path('auth/', include('dj_rest_auth.urls')),
    path('register/',RegisterView.as_view()),
]


#User' i blogapp'den komple alip(tüm applicationu) buraya yapistirabilirim. Tek yapmam gereken degisiklik oradaki ulr'de login ve logout silip yukardaki pathi kullanmak.