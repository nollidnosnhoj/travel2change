from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import reverse, get_object_or_404
from django.views.generic import DeleteView, UpdateView
from .forms import ReviewForm
from .models import Review


class UpdateReview(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    context_object_name = "review"
    template_name_suffix = "_update"
    success_message = "Review successfully updated."

    def get_object(self):
        return get_object_or_404(Review, pk=self.kwargs['pk'], user=self.request.user)

    def get_success_url(self):
        return reverse('user_reviews')


class DeleteReview(LoginRequiredMixin, DeleteView):
    model = Review
    success_message = "Review successfully removed."

    # ignore confirmation page. just delete the review
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, self.success_message)
        return super().delete(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse('user_reviews')
