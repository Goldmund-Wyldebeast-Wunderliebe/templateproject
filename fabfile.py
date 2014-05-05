import sys

from django.conf import settings
from django.template.loader import render_to_string


def pick_settings(layer):
    settings.configure(TEMPLATE_DIRS=('.'))
    files = ['settings/__init__.py', ]
    for f in files:
        fh = open(f, 'wb')
        fh.write(render_to_string('{0}.dev'.format(f), {
            'layer': layer,
        }))
        fh.close()

def create_func(layer):
    def dec():
        pick_settings(layer)
    dec.__name__ = layer
    dec.func_name = layer
    return dec

for layer in ["prd", "dev", "acc", "tst"]:
    setattr(sys.modules[__name__], layer, create_func(layer))
