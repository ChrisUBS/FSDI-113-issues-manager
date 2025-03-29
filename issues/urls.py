from django.urls import path
from issues import views

urlpatterns = [
    path("", views.BoardView.as_view(), name="board"),
    
    path("list/", views.IssueListView.as_view(), name="list"),
    path("open/", views.OpenIssuesView.as_view(), name="open_issues"),
    path("my-issues/", views.MyAssignedIssuesView.as_view(), name="my_issues"),
    path("reported/", views.MyReportedIssuesView.as_view(), name="reported_issues"),
    
    path("new/", views.IssueCreateView.as_view(), name="new"),
    path("<int:pk>/", views.IssueDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", views.IssueUpdateView.as_view(), name="edit"),
    path("<int:pk>/delete/", views.IssueDeleteView.as_view(), name="delete"),
]