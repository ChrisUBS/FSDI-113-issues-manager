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

# Helper function to check if a user is a Product Owner
def is_product_owner(user):
    return user.role and user.role.name.lower() == 'product owner'

class TeamRestrictedMixin:
    """Mixin to filter issues by user's team"""
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        
        # Only superusers can see all issues
        if user.is_superuser:
            return queryset
        
        # Filter by team for all users including staff and product owners
        if user.team:
            return queryset.filter(assignee__team=user.team)
        
        # If user has no team, only show their assigned issues
        return queryset.filter(assignee=user)

class BoardView(LoginRequiredMixin, TeamRestrictedMixin, ListView):
    template_name = "issues/board.html"
    model = Issue
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get filtered queryset based on team
        queryset = self.get_queryset()
        
        to_do = Status.objects.get(name="to do")
        in_progress = Status.objects.get(name="in progress")
        done = Status.objects.get(name="done")
        
        context["to_do_list"] = (
            queryset
            .filter(status=to_do)
            .order_by("created_on").reverse()
        )
        context["in_progress_list"] = (
            queryset
            .filter(status=in_progress)
            .order_by("created_on").reverse()
        )
        context["done_list"] = (
            queryset
            .filter(status=done)
            .order_by("created_on").reverse()
        )
        
        context["is_product_owner"] = is_product_owner(self.request.user)
        
        return context


class IssueDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    template_name = "issues/detail.html"
    model = Issue
    context_object_name = "issue"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_product_owner"] = is_product_owner(self.request.user)
        return context
    
    def test_func(self):
        issue = self.get_object()
        user = self.request.user
        
        # Superusers can view any issue
        if user.is_superuser:
            return True
        
        # All users (including staff and product owners) can only view issues:
        # 1. Assigned to their team
        if user.team and issue.assignee and issue.assignee.team == user.team:
            return True
        
        # 2. That they reported or are assigned to
        if issue.reporter == user or issue.assignee == user:
            return True
        
        # Otherwise, deny access
        return False


class IssueCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    template_name = "issues/new.html"
    model = Issue
    fields = ["name", "summary", "description", "status", "priority", "assignee"]
    
    def form_valid(self, form):
        form.instance.reporter = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        # Only Product Owners can create new issues
        return is_product_owner(self.request.user)
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # If user has a team, limit assignee choices to that team
        if self.request.user.team:
            form.fields['assignee'].queryset = form.fields['assignee'].queryset.filter(
                team=self.request.user.team
            )
        return form


class IssueUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = "issues/edit.html"
    model = Issue
    fields = ["name", "summary", "description", "status", "priority", "assignee"]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_product_owner"] = is_product_owner(self.request.user)
        return context
    
    def test_func(self):
        issue = self.get_object()
        user = self.request.user
        
        # Superusers can edit any issue
        if user.is_superuser:
            return True
        
        # Staff can edit any issue in their team
        if user.is_staff and user.team and issue.assignee and issue.assignee.team == user.team:
            return True
        
        # Product Owners can edit issues in their team
        if is_product_owner(user) and user.team and issue.assignee and issue.assignee.team == user.team:
            return True
        
        # Users can edit issues they reported or are assigned to
        if issue.reporter == user or issue.assignee == user:
            return True
        
        return False
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # If user has a team, limit assignee choices to that team
        if self.request.user.team:
            form.fields['assignee'].queryset = form.fields['assignee'].queryset.filter(
                team=self.request.user.team
            )
        return form


class IssueDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = "issues/delete.html"
    model = Issue
    success_url = reverse_lazy("board")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_product_owner"] = is_product_owner(self.request.user)
        return context
    
    def test_func(self):
        issue = self.get_object()
        user = self.request.user
        
        # Superusers can delete any issue
        if user.is_superuser:
            return True
        
        # Staff can delete any issue in their team
        if user.is_staff and user.team and issue.assignee and issue.assignee.team == user.team:
            return True
        
        # Product Owners can delete issues in their team
        if is_product_owner(user) and user.team and issue.assignee and issue.assignee.team == user.team:
            return True
        
        # Users can only delete issues they reported
        return issue.reporter == user


class IssueListView(LoginRequiredMixin, TeamRestrictedMixin, ListView):
    template_name = "issues/list.html"
    model = Issue
    context_object_name = "issues"
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by("-created_on")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_product_owner"] = is_product_owner(self.request.user)
        context["title"] = "All Issues"
        return context


class OpenIssuesView(LoginRequiredMixin, TeamRestrictedMixin, ListView):
    template_name = "issues/open_issues.html"
    model = Issue
    context_object_name = "issues"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        done = Status.objects.get(name="done")
        
        # Filter by team and status
        queryset = self.get_queryset()
        
        context["title"] = "Open Issues"
        context["issues"] = (
            queryset
            .exclude(status=done)
            .order_by("created_on").reverse()
        )
        context["is_product_owner"] = is_product_owner(self.request.user)
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
        context["is_product_owner"] = is_product_owner(self.request.user)
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
        context["is_product_owner"] = is_product_owner(self.request.user)
        return context