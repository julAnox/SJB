from django.http import JsonResponse
from django.apps import apps


def get_field_limits(request):
    """
    API-эндпоинт для получения максимальных длин полей всех моделей
    """
    field_limits = {}

    # Получаем все модели из приложения
    models = apps.get_models()

    for model in models:
        model_name = model.__name__.lower()
        field_limits[model_name] = {}

        for field in model._meta.fields:
            if hasattr(field, 'max_length') and field.max_length:
                field_limits[model_name][field.name] = field.max_length

    return JsonResponse(field_limits)
