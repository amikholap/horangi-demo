from django.urls import include, path

from . import views


api_urlpatterns = (
    [
        path('users/', views.UserListAPIView.as_view(), name='user-list'),
        path('follow/', views.FollowApiView.as_view(), name='follow'),
        path('unfollow/', views.UnfollowApiView.as_view(), name='unfollow'),
    ],
    'demo',
)

urlpatterns = [
    path('api/', include(api_urlpatterns, namespace='api')),
]
