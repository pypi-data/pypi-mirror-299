# -*- coding: utf-8 -*-
from ..item import Item
import logging
import barcode
import os

logger = logging.getLogger(__name__)


class Product(Item):
    """
    This class describes an Product object child of Item class.
    """


    def get_barcode(self, path=None):
        """
        Generate barcode for this product

        :param      path:  The path to save the barcode
        :type       path:  string

        :returns:   Barcode object
        :rtype:     barcode object

        """
        code128 = barcode.get("CODE128", self._key)
        return code128

    def save_barcode(self, path, options=None):
        """
        Generate barcode for this product and save it to a file as a .svg file

        :param      path:  The path to save the barcode
        :type       path:  string

        """

        if path is None:
            raise ValueError("Path is required to save the barcode")
        if os.path.basename(path) == '':
            path = os.path.join(path, self.data.name or self._key)

        (filename, ext) = os.path.splitext(path)

        code128 = self.get_barcode()
        return code128.save(filename, options)