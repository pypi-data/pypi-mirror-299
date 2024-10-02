from django.http import HttpResponse
from django.conf import settings
from django.core.paginator import Paginator
from django.template import loader

from change_logs.models import ChangeLog



def change_logs_list(request):
    """Change Logs List View."""
    try:
        per_page = settings.CHANGE_LOGS_PER_PAGE
    except AttributeError:
        per_page = 10

    change_logs = ChangeLog.objects.all().order_by("-date")
    paginator = Paginator(change_logs, per_page)
    page = request.GET.get("page", 1)

    change_logs = paginator.get_page(page)

    context = {
        "change_logs": change_logs
    }
    template = loader.get_template("change_logs/list.html")
    return HttpResponse(template.render(context, request))


def change_logs_detail(request, version):
    """Change Logs Detail View."""
    try:
        change_log = ChangeLog.objects.get(version__iexact=version)
    except ChangeLog.DoesNotExist:
        return HttpResponse("Change Log not found")
    context = {
        "change_log": change_log
    }
    template = loader.get_template("change_logs/detail.html")
    return HttpResponse(template.render(context, request))
