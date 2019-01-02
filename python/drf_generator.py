import importlib
import inspect


def generate(models_module, header, template, footer):
    print(header)

    models = importlib.import_module(models_module)
    for name, obj in inspect.getmembers(models, inspect.isclass):
        if obj.__module__ == models_module:
            print(template.format(obj.__name__, obj.__name__.lower()))

    print(footer)


def generate_serializers(models_module):
    HEADER = """from .models import *
from rest_framework import serializers
    """
    TEMPLATE =  """class {0}Serializer(serializers.HyperlinkedModelSerializer):
        class Meta:
            model = {0}
            fields = "__all__"
    """
    FOOTER = """"""

    generate(models_module, HEADER, TEMPLATE, FOOTER)


def generate_views(models_module):
    HEADER = """from rest_framework import viewsets
from ..serializers import *
        """
    TEMPLATE = """class {0}ViewSet(viewsets.ModelViewSet):
    queryset = {0}.objects.all()
    serializer_class = {0}Serializer
"""
    FOOTER = """"""

    generate(models_module, HEADER, TEMPLATE, FOOTER)


def generate_url_routers(models_module):
    models = importlib.import_module(models_module)
    for name, obj in inspect.getmembers(models, inspect.isclass):
        if obj.__module__ == models_module:
            model_name = obj.__name__
            model_name_lower_plural = model_name.lower() + 's'
            print("router.register(r'{0}', views.{1}ViewSet)".format(model_name_lower_plural, model_name))

def generate_admin_entries(models_module):
    models = importlib.import_module(models_module)
    CLASS_TEMPLATE = """@admin.register({0})
class {0}Admin(admin.ModelAdmin):
    pass
    
"""

    # Header
    print("""from django.contrib import admin
from .models import *


""")

    for name, obj in inspect.getmembers(models, inspect.isclass):
        if obj.__module__ == models_module:
            model_name = obj.__name__
            print(CLASS_TEMPLATE.format(model_name))
