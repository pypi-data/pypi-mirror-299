# -*- coding: utf-8 -*-
from ..item import Item
import logging

logger = logging.getLogger(__name__)


class Hardware(Item):
    """
    This class describes an Hardware object child of Item class.
    """

    def get_products(self, offset = 0, limit = 200):
        """
        Get products linked to this hardware

        :param      offset:  Number of skipped hardware. Used for pagination
        :type       offset:  integer
        :param      limit:   Maximum limit number of returned hardware
        :type       limit:   integer
        """

        meshql = f"# -($Child)> {offset},{limit} $Product VIEW item"
        products = self.traverse(meshql)
        products = [self.parent.cast(product) for product in products]
        return products