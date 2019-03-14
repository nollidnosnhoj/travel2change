from django.http import JsonResponse


class AjaxFormMixin(object):
    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response
    
    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.is_ajax():
            data = {
                'message': "Successfully updated profile."
            }
            return JsonResponse(data)
        else:
            return response
