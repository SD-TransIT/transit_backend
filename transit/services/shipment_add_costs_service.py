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

        ShipmentDetails.objects.filter(id=shipment['id']).update(
            transporter_base_cost=shipment['transporter_base_cost'],
            transporter_additional_cost=shipment['transporter_additional_cost'],
            number_of_kilometers=shipment['number_of_kilometers']
        )
