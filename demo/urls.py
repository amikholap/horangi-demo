# pylint: disable=invalid-name,line-too-long
from django.urls import include, path

from . import views


api_urlpatterns = (
    [
        path('actions/', views.ActionListAPIView.as_view(), name='action-list'),
        path('related-actions/', views.RelatedActionListAPIView.as_view(), name='related-action-list'),
        path('my-feed/', views.MyActionFeedAPIView.as_view(), name='my-feed'),
        path('friends-feed/', views.FriendsActionFeedAPIView.as_view(), name='friends-feed'),
        path('follow/', views.FollowApiView.as_view(), name='follow'),
        path('unfollow/', views.UnfollowApiView.as_view(), name='unfollow'),
        path('users/', views.UserListAPIView.as_view(), name='user-list'),
    ],
    'demo',
)

urlpatterns = [
    path('api/', include(api_urlpatterns, namespace='api')),
]
