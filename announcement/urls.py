from django.urls import path
from .views import (AnonsList, UserDetail, AnonsDetail, AnonsUpdate,
                    AnonsDelete, AnonsCreate, comment_create, comment_delete, comments_to_me)

urlpatterns = [
    path('', AnonsList.as_view(), name='all_anons'),
    path('my_list/', comments_to_me, name='my_list'),
    # path('my_list/choise', accept, name='accept'),
    path('user_profile/<int:pk>/', UserDetail.as_view(), name='user_profile'),
    path('anons/<int:pk>/', AnonsDetail.as_view(), name='anons_detail'),
    path('anons/<int:pk>/update/', AnonsUpdate.as_view(), name='anons_update'),
    path('anons/<int:pk>/delete/', AnonsDelete.as_view(), name='anons_delete'),
    path('anons/create/', AnonsCreate.as_view(), name='anons_create'),
    path('anons/<int:pk>/comment_create/', comment_create, name='comment_create'),
    path('anons/<int:anons_id>/comment_delete/<int:pk>/', comment_delete, name='comment_delete'),
]
