from django.conf import settings
from django.core.checks import Error, register
from importlib.util import find_spec

@register()
def check_installed_apps(app_configs, **kwargs):
    errors = []
    required_apps = [
        'polymorphic',
        'sage_qrcode',
        'colorfield',
    ]

    for app in required_apps:
        if app not in settings.INSTALLED_APPS:
            errors.append(
                Error(
                    f"'{app}' is missing in INSTALLED_APPS.",
                    hint=f"Add '{app}' to INSTALLED_APPS in your settings.",
                    obj=settings,
                    id=f"sage_shop_warehouse.E00{required_apps.index(app) + 3}",
                )
            )

    return errors

@register()
def check_required_libraries(app_configs, **kwargs):
    errors = []
    required_libraries = [
        'polymorphic',
        'sage_qrcode',
        'colorfield',
    ]

    for library in required_libraries:
        if not find_spec(library):
            errors.append(
                Error(
                    f"The required library '{library}' is not installed.",
                    hint=f"Install '{library}' via pip: pip install {library}",
                    obj=settings,
                    id=f"sage_shop_warehouse.E00{required_libraries.index(library) + 6}",
                )
            )

    return errors