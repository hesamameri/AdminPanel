from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import MultipleObjectsReturned

def get_object_or_none(model, **kwargs):
    queryset = model.objects.filter(**kwargs)
    if queryset.count() == 0:
        return None
    elif queryset.count() > 1:
        return queryset.last()
    else:
        return queryset.first()
    


