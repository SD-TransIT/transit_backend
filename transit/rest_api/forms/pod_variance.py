import django_filters
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from transit.models import PODVariance, PODVarianceDetails
from transit.rest_api.abstract import BaseModelFormViewSet


class PODVarianceFilter(django_filters.FilterSet):
    class Meta:
        model = PODVariance
        fields = {
            'dso_type': ['exact', 'iexact', 'startswith']
        }


class PODVarianceDetailsFilter(django_filters.FilterSet):
    class Meta:
        model = PODVarianceDetails
        fields = {
            'order_line_details': ['exact'],
            'quantity': ['exact', 'lte', 'gte']
        }


class PODVarianceDetailsSerializer(serializers.ModelSerializer):
    pod_variance = serializers.ModelField(
        model_field=PODVariance()._meta.get_field('id'), required=False)
    serializers.IntegerField(required=False)

    class Meta:
        model = PODVarianceDetails
        fields = ['id', 'pod_variance', 'order_line_details', 'quantity']
        read_only_fields = ['id']

    def create(self, validated_data):
        validated_data['pod_variance'] = PODVariance.objects.get(pk=validated_data['pod_variance'])
        return super(PODVarianceDetailsSerializer, self).create(validated_data)


class PODVarianceSerializer(serializers.ModelSerializer):
    pod_variance_details = PODVarianceDetailsSerializer(many=True, required=False)

    class Meta:
        model = PODVariance
        fields = ['id', 'dso_type', 'shipment', 'pod_variance_details']
        read_only_fields = ['id']

    def create(self, validated_data):
        line_items = validated_data.pop('pod_variance_details', [])
        pod_variance = PODVariance.objects.create(**validated_data)
        for details_dict in line_items:
            details_dict['pod_variance'] = pod_variance
            PODVarianceDetails(**details_dict).save()
        return pod_variance  # noqa: R504

    def validate(self, data): # noqa: WPS-122
        """
        Update of line items directly through OrderDetails is forbidden.
        """
        validated = super(PODVarianceSerializer, self).validate(data)
        if self.instance and validated.get('line_items'):
            raise serializers.ValidationError(
                _("Pod Variance Details have to be updated using pod_variance_details endpoint.")
            )
        return validated


class PODVarianceViewSet(BaseModelFormViewSet):
    filterset_class = PODVarianceFilter
    queryset = PODVariance.objects.all().order_by('-id')

    def get_serializer_class(self):
        return PODVarianceSerializer


class PODVarianceDetailsViewSet(BaseModelFormViewSet):
    filterset_class = PODVarianceDetailsFilter
    queryset = PODVarianceDetails.objects.all().order_by('-id')

    def get_serializer_class(self):
        return PODVarianceDetailsSerializer
