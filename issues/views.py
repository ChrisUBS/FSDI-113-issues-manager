from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

from .models import Issue, Status
from django.urls import reverse_lazy
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)

class BoardView(LoginRequiredMixin, ListView):
    template_name = "issues/board.html"
    model = Issue
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        to_do = Status.objects.get(name="to do")
        in_progress = Status.objects.get(name="in progress")
        done = Status.objects.get(name="done")
        context["to_do_list"] = (
            Issue.objects
            .filter(status=to_do)
            .order_by("created_on").reverse()
        )
        context["in_progress_list"] = (
            Issue.objects
            .filter(status=in_progress)
            .order_by("created_on").reverse()
        )
        context["done_list"] = (
            Issue.objects
            .filter(status=done)
            .order_by("created_on").reverse()
        )
        return context


class IssueDetailView(UserPassesTestMixin, DetailView):
    template_name = "issues/detail.html"
    model = Issue
    context_object_name = "issue"
    
    def test_func(self):
        return True


class IssueCreateView(LoginRequiredMixin, CreateView):
    template_name = "issues/new.html"
    model = Issue
    fields = ["name", "summary", "description", "status", "priority", "assignee"]
    
    def form_valid(self, form):
        form.instance.reporter = self.request.user
        return super().form_valid(form)


class IssueUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = "issues/edit.html"
    model = Issue
    fields = ["name", "summary", "description", "status", "priority", "assignee"]
    
    def test_func(self):
        issue = self.get_object()
        return (
            self.request.user == issue.reporter or 
            self.request.user == issue.assignee or
            self.request.user.is_staff
        )


class IssueDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = "issues/delete.html"
    model = Issue
    success_url = reverse_lazy("board")
    
    def test_func(self):
        issue = self.get_object()
        return self.request.user == issue.reporter or self.request.user.is_staff


class IssueListView(LoginRequiredMixin, ListView):
    template_name = "issues/list.html"
    model = Issue
    context_object_name = "issues"
    
    def get_queryset(self):
        return Issue.objects.all().order_by("-created_on")


class OpenIssuesView(LoginRequiredMixin, ListView):
    template_name = "issues/open_issues.html"
    model = Issue
    context_object_name = "issues"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        done = Status.objects.get(name="done")
        context["title"] = "Open Issues"
        context["issues"] = (
            Issue.objects
            .exclude(status=done)
            .order_by("created_on").reverse()
        )
        return context


class MyAssignedIssuesView(LoginRequiredMixin, ListView):
    template_name = "issues/my_issues.html"
    model = Issue
    context_object_name = "issues"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "My Assigned Issues"
        context["issues"] = (
            Issue.objects
            .filter(assignee=self.request.user)
            .order_by("created_on").reverse()
        )
        return context


class MyReportedIssuesView(LoginRequiredMixin, ListView):
    template_name = "issues/reported_issues.html"
    model = Issue
    context_object_name = "issues"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Issues I Reported"
        context["issues"] = (
            Issue.objects
            .filter(reporter=self.request.user)
            .order_by("created_on").reverse()
        )
        return context