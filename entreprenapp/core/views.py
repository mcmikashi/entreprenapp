from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.utils import timezone
from django.http import HttpResponseRedirect, Http404


class CoreCreateView(LoginRequiredMixin, CreateView):
    """Custom create view that set the  created by
    property when user create a new instance"""

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class CoreUpdateView(LoginRequiredMixin, UpdateView):
    """A custom update view that set the  created by
    property when user update an instance"""

    def form_valid(self, form):
        form.instance.modified_by = self.request.user
        return super().form_valid(form)


class CoreDeleteView(LoginRequiredMixin, DeleteView):
    """A custom delete view that soft delete an instance"""

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.deleted_date = timezone.now()
        self.object.deleted_by = self.request.user
        self.object.save()
        success_url = self.get_success_url()
        return HttpResponseRedirect(success_url)


class CoreListView(LoginRequiredMixin, ListView):
    """A custom list view that show instance to user admin
    and only show instance that is active for other user."""

    def get_queryset(self):
        query_set = super().get_queryset()
        if self.request.user.is_superuser:
            return query_set
        return query_set.filter(is_active=True)


class CoreDetailView(LoginRequiredMixin, DetailView):
    """A custom detail view that only show inactive instance to admin user
    and return 404 for inactive instance"""

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object.is_active:
            if self.request.user.is_superuser:
                return super().get(request)
            else:
                raise Http404("This data as been deleted")
