class _EnumMeta(type):
    def __init__(cls, name, bases, dct):
        super(_EnumMeta, cls).__init__(name, bases, dct)
        cls._choices = dict(cls.__dict__['choices']) \
            if 'choices' in cls.__dict__ else dict()

    def __call__(cls, key):
        return cls._to_str(key)

    def __iter__(cls):
        for s, _ in cls.__dict__['choices']:
            yield s


class Enum(object):
    __metaclass__ = _EnumMeta

    @classmethod
    def _to_str(cls, key):
        try:
            key = int(key)
        except (ValueError, TypeError):
            return None
        return cls._choices.get(key, None)
