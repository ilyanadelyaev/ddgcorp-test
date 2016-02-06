class _EnumMeta(type):
    """
    __metaclass__ for Enum
    """

    def __init__(cls, name, bases, dct):
        super(_EnumMeta, cls).__init__(name, bases, dct)
        cls._choices = dict(cls.__dict__['choices']) \
            if 'choices' in cls.__dict__ else dict()

    def __call__(cls, key):
        """
        Direct call: Enum(key)
        """
        return cls._to_str(key)

    def __iter__(cls):
        """
        Direct call: for e in Enum: pass
        """
        for key, _ in cls.__dict__['choices']:
            yield key


class Enum(object):
    """
    Enum with choices for Models
    """

    __metaclass__ = _EnumMeta

    @classmethod
    def _to_str(cls, key):
        """
        Convert emum value to human-readable string
        """
        try:
            key = int(key)
        except (ValueError, TypeError):
            return None
        # Declared in meta
        # pylint: disable=E1101
        return cls._choices.get(key, None)
