from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI
from auth.view import router as auth_router
from todo_app.views import router as api_router
from configs import settings
from django.conf.urls.static import static

api = NinjaAPI()
api.add_router('auth/', auth_router, tags=['auth'])
api.add_router('api/', api_router, tags=['api'])


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', api.urls)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
