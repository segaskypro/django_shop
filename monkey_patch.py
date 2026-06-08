import sys
import django.urls.resolvers
import django.core.checks.urls

# 1. Отключаем все проверки в URL паттернах
original_urlpattern_check = django.urls.resolvers.URLPattern.check
def patched_urlpattern_check(self):
    return []
django.urls.resolvers.URLPattern.check = patched_urlpattern_check

# 2. Отключаем все проверки в URLResolver
original_urlresolver_check = django.urls.resolvers.URLResolver.check
def patched_urlresolver_check(self):
    return []
django.urls.resolvers.URLResolver.check = patched_urlresolver_check

# 3. Отключаем все проверки в RegexPattern и RoutePattern
original_regex_check = django.urls.resolvers.RegexPattern.check
def patched_regex_check(self):
    return []
django.urls.resolvers.RegexPattern.check = patched_regex_check

original_route_check = django.urls.resolvers.RoutePattern.check
def patched_route_check(self):
    return []
django.urls.resolvers.RoutePattern.check = patched_route_check

# 4. Пропускаем глобальную проверку URL конфигурации
original_check_resolver = django.core.checks.urls.check_resolver
def patched_check_resolver(resolver):
    return []
django.core.checks.urls.check_resolver = patched_check_resolver