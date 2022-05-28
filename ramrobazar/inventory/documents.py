from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Product


@registry.register_document
class ProductDocument(Document):

    product = fields.ObjectField(properties = {
        "name": fields.TextField()
    })

    class Index:
        name = 'product'
    
    class Django:
        model = Product
        fields = ['id', 'price',]