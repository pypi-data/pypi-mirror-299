from netbox.views import generic
from dcim.models import Device
from netbox_sync_status.filtersets import SyncStatusFilterForm, SyncStatusFilterSet
from .tables import SyncStatusListTable, SyncSystemListTable
from .models import SyncStatus, SyncSystem
from .forms import SyncSystemForm
from utilities.views import GetReturnURLMixin
from django.shortcuts import redirect
from django.views.generic import View
from django.contrib import messages
from extras.events import enqueue_event
from core.choices import ObjectChangeActionChoices
from netbox.context import events_queue


class SyncSystemView(generic.ObjectView):
    queryset = SyncSystem.objects.prefetch_related("tags")


class SyncSystemListView(generic.ObjectListView):
    queryset = SyncSystem.objects.prefetch_related("tags")
    table = SyncSystemListTable


class SyncSystemEditView(generic.ObjectEditView):
    queryset = SyncSystem.objects.all()
    form = SyncSystemForm


class SyncSystemDeleteView(generic.ObjectDeleteView):
    queryset = SyncSystem.objects.all()


class SyncStatusListView(generic.ObjectListView):
    queryset = SyncStatus.objects.order_by("-id")
    table = SyncStatusListTable
    filterset = SyncStatusFilterSet
    filterset_form = SyncStatusFilterForm
    actions = {
        "export": set()
    }


class DeviceSyncView(GetReturnURLMixin, View):
    queryset = Device.objects.all()

    def post(self, request, **kwargs):
        selected_objects = self.queryset.filter(
            pk=kwargs.get("pk"),
        )

        for obj in selected_objects:
            obj.snapshot()
            queue = events_queue.get()
            enqueue_event(queue, obj, request.user, request.id, ObjectChangeActionChoices.ACTION_UPDATE)
            events_queue.set(queue)

        messages.success(request, f"Manual sync started for {obj.name}")
        return redirect(self.get_return_url(request))
