from django.db import transaction

from transit.models.shipment import ShipmentDetails


class ShipmentAddCostsService:
    """
        Service allowing to add costs to the shipments
    """

    @transaction.atomic
    def add_cost_to_shipment(self, shipment):
        """
            Save costs to given shipment.

            :param shipment: shipment to which costs will be assigned.
        """
        shipment_id = shipment.pop('id')
        shipment_detail = ShipmentDetails.objects.get(id=shipment_id)
        for attr, value in shipment.items():
            setattr(shipment_detail, attr, value)
        shipment_detail.save()
