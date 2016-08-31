import collections
import pprint

__version__ = '${version}'

pp = pprint.PrettyPrinter(indent=1)


class UnexpectedConfigValues(Exception):
    pass


class MissingConfigValues(Exception):
    pass


class VoodooConfig(collections.MutableMapping):

    def __init__(self, **kwargs):
        for option, default in self.options.items():
            self[option] = (default()
                            if hasattr(default, '__call__')
                            else default)
        self._inject(kwargs)

    def __str__(self):
        return pp.pformat(dict(self))

    @property
    def _class_name(self):
        return type(self).__name__

    def __getitem__(self, key):
        if key not in self.options:
            raise KeyError('%s not in %s' % (key, self._class_name))
        return getattr(self, key)

    def __setitem__(self, key, value):
        if key not in self.options:
            raise KeyError('%s not in %s' % (key, self._class_name))
        setattr(self, key, value)

    def __delitem__(self, key):
        raise NotImplementedError(
            '%s does not support __delitem__ or derivatives'
            % self._class_name)

    def __delattr__(self, key):
        raise NotImplementedError(
            '%s does not support __delattr__ or derivatives'
            % self._class_name)

    def __len__(self):
        return len(self.options)

    def __iter__(self):
        return iter(self.options)

    def __contains__(self, value):
        return value.replace('-', '_') in self.options

    def update(self, new_options):
        self.validate_options(new_options)
        straightend = self.straighten(new_options)
        self.inject(straightend)

    def _inject(self, new_options):
        for option in self.options:
            if option in new_options and new_options[option] is not None:
                self[option] = new_options[option]

    @staticmethod
    def straighten(config):
        return dict(((k.replace('-', '_'), v)
                     for k, v in config.items()))

    def is_complete(self):
        if not all(self.values()):
            missing = dict(((k, v) for k, v in self.options.items() if not v))
            raise MissingConfigValues(
                'Some config values are missing:\n{0}'.format(missing))
        else:
            return True

    def validate_options(self, loaded_options):
        valid_values_hyphen = set((k.replace('_', '-')
                                   for k in self.options))
        valid_values_underscore = set(self.options)
        valid_values = valid_values_hyphen.union(valid_values_underscore)
        unexpected_values = set(loaded_options).difference(valid_values)
        if unexpected_values:
            raise UnexpectedConfigValues(
                'The following unexpected values were detected {0}'
                .format(list(unexpected_values)))
        else:
            return True
