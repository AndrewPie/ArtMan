from django.urls import path

from .views import MyListView, AddSpecificationView, ModifySpecificationView

app_name = 'cargo_spec'
urlpatterns = [
    path('my_lists/', MyListView.as_view(), name='my-lists'),
    path('add_specification/', AddSpecificationView.as_view(), name='add-spec'),
    path('modify_specification/<int:pk>', ModifySpecificationView.as_view(), name='modify-spec'),
]
