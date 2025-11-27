import copy
from rest_framework import permissions


class CustomDjangoModelPermissions(permissions.DjangoModelPermissions):
    """
    Rozszerzona wersja DjangoModelPermissions.
    Dodaje obsługę uprawnienia 'view' dla żądań GET.

    Mapowanie:
    - GET: view_<model_name>
    - POST: add_<model_name>
    - PUT/PATCH: change_<model_name>
    - DELETE: delete_<model_name>
    """

    def __init__(self):
        super().__init__()
        self.perms_map = copy.deepcopy(self.perms_map)
        self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']
        self.perms_map['HEAD'] = []
        self.perms_map['OPTIONS'] = []