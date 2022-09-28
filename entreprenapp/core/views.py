from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseRedirect
from django.utils import timezone
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView


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

    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        elided_page_range = context["paginator"].get_elided_page_range(
            number=context["page_obj"].number, on_each_side=4, on_ends=0
        )
        context["elied_page_range"] = elided_page_range
        return context

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
