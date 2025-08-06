from django.urls import path
from .views import ComplaintCreateView, ComplaintDetailView, ComplaintEditView, ComplaintListView,ComplaintView, ComplaintStatusView, ComplaintDeleteView, CurrentComplaintView, ResolvedComplaintView, ComplaintStatsView

urlpatterns = [
    path('create/', ComplaintCreateView.as_view(), name='create_complaint'),
    path('list/', ComplaintListView.as_view(), name='list_complaints'),
    path('<int:id>/', ComplaintView.as_view(), name='get_complaint'),
    path('<int:id>/edit/', ComplaintEditView.as_view(), name='edit-complaint'),
    path('<int:id>/status/', ComplaintStatusView.as_view(), name='complaint-status'),
    path('<int:id>/delete/',ComplaintDeleteView.as_view(), name='delete_complaint'),
    path('current-complaints/',CurrentComplaintView.as_view(),name = 'current_complaints'),
    path('resolved-complaints/',ResolvedComplaintView.as_view(),name = 'resolved_complaints'),
    path('<int:id>/detail/', ComplaintDetailView.as_view(), name='complaint-detail'),
    path('stats/', ComplaintStatsView.as_view(), name='complaint-stats')
]
