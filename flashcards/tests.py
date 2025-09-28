from django.test import TestCase

print("=== URLs загружены ===")
for url in urlpatterns:
    print(f'Path: {url.pattern} -> {url.name}')


