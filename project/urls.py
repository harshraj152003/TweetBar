from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from tweet import views as tweet_views

urlpatterns = [
    path('', tweet_views.tweet_list, name='home'),

    path('admin/', admin.site.urls),
    path('tweet/', include('tweet.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)