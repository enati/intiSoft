from django.http import HttpResponse
from django.views.generic.base import TemplateView
from django.template.loader import render_to_string
from .models import ActivityLog


class ActivityLogView(TemplateView):
    template_name = "activity_log/activity_log.html"

    def get_context_data(self, **kwargs):
        context = super(ActivityLogView, self).get_context_data(**kwargs)
        context['recent_activity'] = ActivityLog.objects.all()
        return context

    def get(self, request, *args, **kwargs):
        res = super(ActivityLogView, self).get(request, *args, **kwargs)
        content_type_id = request.GET.get('content_type_id')
        object_id = request.GET.get('object_id')
        activity_records = ActivityLog.objects.filter(content_type_id=content_type_id, object_id=object_id)
        if self.request.is_ajax():
            html = render_to_string(self.template_name, {'recent_activity': activity_records})
            return HttpResponse(html)
        return res
