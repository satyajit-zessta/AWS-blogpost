from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views 
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from .auth import CustomAuthToken
urlpatterns = [
    path('auth/', include('rest_framework.urls',namespace= 'rest_framework' )),

    path('get-token/', views.obtain_auth_token),
    path('get-custom-token/', CustomAuthToken.as_view(), name='get-custom-token'),

    path('get-jwt-token/', TokenObtainPairView.as_view(),name="token_obtain_pair"),
    path('refresh-jwt-token/', TokenRefreshView.as_view(), name = "token_refresh"),
    path('verify-jwt-token/', TokenVerifyView.as_view(), name = "token_verify"),

    path('get-csrf-cookie/', GetCSRFToken.as_view(), name = 'get_csrf_cookie'),

]

router = DefaultRouter()


router.register(r'user-view-set', UserViewSet, basename='user')
router.register(r'post-view-set', PostViewSet, basename='post')
router.register(r'tag-view-set', TagViewSet, basename='tag')
router.register(r'comment-view-set', CommentViewSet, basename='comment')


urlpatterns.extend(router.urls)