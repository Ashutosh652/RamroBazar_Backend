# from django_elasticsearch_dsl import Document, fields
# from django_elasticsearch_dsl.registries import registry
# from .models import User


# @registry.register_document
# class UserDocument(Document):

#     userprofile = fields.ObjectField(properties = {
#         "date_of_birth": fields.DateField()
#     })

#     class Index:
#         name = 'user'
    
#     class Django:
#         model = User
#         fields = ['id', 'first_name',]