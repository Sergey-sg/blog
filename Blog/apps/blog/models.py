from django.db import models

from treebeard.mp_tree import MP_Node

from shared.mixins.model_utils import DragDropMixins


class Category(DragDropMixins, MP_Node):
    name = models.CharField(max_length=50)

    node_order_by = ['name']

    def __str__(self):
        return f'Category: {self.name}'
