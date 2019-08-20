from django.urls import resolve

def appname(request):
    return{'appname': resolve(request.path).app_name}

# funkcja daje nazwę aplikacji (np. 'cargo_spec') i po zarejestrowaniu jej w settings/TEMPLATES/'context_processors'/'arct_man.contexts.appname' uzyskujemy do niej dostęp w template poprzez {{appname}}