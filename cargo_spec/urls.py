from django.urls import path

from .views import MyListView, AddSpecificationView, ModifySpecificationView, DeleteSpecificationView, AcceptSpecificationView, SpecificationDetailView, SpecificationDocumentUploadView

app_name = 'cargo_spec'
urlpatterns = [
    path('my_lists/', MyListView.as_view(), name='my-lists'),
    path('specification/add', AddSpecificationView.as_view(), name='add-spec'),
    path('specification/<int:pk>/modify', ModifySpecificationView.as_view(), name='modify-spec'),
    path('specification/<int:pk>/delete', DeleteSpecificationView.as_view(), name='delete-spec'),
    path('specification/<int:pk>/accept', AcceptSpecificationView.as_view(), name='accept-spec'),
    path('specification/<int:pk>/detail', SpecificationDetailView.as_view(), name='spec-detail'),
    path('specification/<int:pk>/upload_scan', SpecificationDocumentUploadView.as_view(), name='scan-upload'),
    path('specification/<int:pk>/upload_photo', SpecificationDocumentUploadView.as_view(), name='photo-upload'),
]
