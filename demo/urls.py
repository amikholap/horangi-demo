# pylint: disable=invalid-name
from django.urls import include, path

from . import views


api_urlpatterns = (
    [
        path('actions/', views.ActionListAPIView.as_view(), name='action-list'),
        path('my-feed/', views.MyActionFeedAPIView.as_view(), name='my-feed'),
        path('users/', views.UserListAPIView.as_view(), name='user-list'),
        path('follow/', views.FollowApiView.as_view(), name='follow'),
        path('unfollow/', views.UnfollowApiView.as_view(), name='unfollow'),
    ],
    'demo',
)

urlpatterns = [
    path('api/', include(api_urlpatterns, namespace='api')),
]
