from django.urls import path

from report.views import ReportContentView, NoteView

app_name = 'report'
urlpatterns = [
    path('', ReportContentView.as_view(), name='contents-page'),
    path('subsection/<int:pk>', NoteView.as_view(), name='note-list'),
]