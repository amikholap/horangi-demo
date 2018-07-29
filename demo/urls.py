from django.urls import include, path

from . import views


api_urlpatterns = (
    [
        path('users/', views.UserListAPIView.as_view(), name='user-list'),
    ],
    'demo',
)

urlpatterns = [
    path('api/', include(api_urlpatterns, namespace='api')),
]
