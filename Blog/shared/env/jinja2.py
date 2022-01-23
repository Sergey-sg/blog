from jinja2 import Environment


def environment(**options):
    """
    Provides default environment for jinja.
    """
    options['cache_size'] = 0
    env = Environment(**options)
    return env
