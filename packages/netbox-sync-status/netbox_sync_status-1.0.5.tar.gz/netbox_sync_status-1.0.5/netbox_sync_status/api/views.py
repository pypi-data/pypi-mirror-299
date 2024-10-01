from netbox.api.viewsets import NetBoxModelViewSet, BaseViewSet
from netbox_sync_status.filtersets import SyncStatusFilterSet
from rest_framework.decorators import action
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from dcim.models import Device
from drf_spectacular.utils import extend_schema
from django.db.models import Prefetch
from extras.events import enqueue_event
from core.events import OBJECT_UPDATED
from netbox.context import events_queue
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import mixins as drf_mixins
from django.db.models import Q


from .. import models
from .serializers import SyncStatusSerializer, SyncSystemSerializer, SyncSystemDeviceStatusSerializer


class DeviceSyncView(APIView):
    queryset = models.Device.objects
    serializer_class = None

    @extend_schema(
        responses={status.HTTP_204_NO_CONTENT: None}
    )
    def post(self, request, pk, format=None):
        selected_objects = self.queryset.filter(
            pk=pk,
        )

        for obj in selected_objects:
            obj.snapshot()
            queue = events_queue.get()
            enqueue_event(queue, obj, request.user, request.id, OBJECT_UPDATED)
            events_queue.set(queue)

        return Response(None, status=status.HTTP_204_NO_CONTENT)


class SyncStatusViewSet(
    drf_mixins.CreateModelMixin,
    drf_mixins.RetrieveModelMixin,
    drf_mixins.ListModelMixin,
    BaseViewSet
):
    queryset = models.SyncStatus.objects
    serializer_class = SyncStatusSerializer
    filterset_class = SyncStatusFilterSet


class SyncSystemViewSet(NetBoxModelViewSet):
    queryset = models.SyncSystem.objects.prefetch_related("tags")
    serializer_class = SyncSystemSerializer

    @extend_schema(
        responses=SyncSystemDeviceStatusSerializer(many=True), 
        request=None
    )
    @action(
        detail=True,
        methods=["get"],
        url_path="sync-status",
        renderer_classes=[JSONRenderer]
    )
    def render_system_sync_staus(self, request, pk):
        """
        Resolve and render the sync status of all devices
        """
        system = self.get_object()
        devices = Device.objects.prefetch_related(
            Prefetch(
                "sync_status",
                queryset=models.SyncStatus.objects.filter(Q(system__id = system.id) & Q(is_latest=True)),
                to_attr="sync_events"
            )
        ).all()

        results = []
        for device in devices:
            if len(device.sync_events) > 0:
                results.append({
                    "device_name": device.name,
                    "status": device.sync_events[0].status
                })
            else:
                results.append({
                    "device_name": device.name,
                    "status": "not-started"
                })

        return Response(results)
