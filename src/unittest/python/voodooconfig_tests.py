import unittest

from voodooconfig import (VoodooConfig,
                          MissingConfigValues,
                          UnexpectedConfigValues,
                          )


class MyConfig(VoodooConfig):
    options = {'default_option': 'DEFAULT_VALUE',
               'lambda_option': lambda: 'CALLED_VALUE',
               'missing_option': None,
               }


class TestVoodooConfig(unittest.TestCase):

    def test_init_sets_up_defaults(self):
        config = MyConfig()
        self.assertEqual(config.lambda_option, 'CALLED_VALUE')
        self.assertEqual(config.default_option, 'DEFAULT_VALUE')
        self.assertEqual(config.missing_option, None)

    def test_init_processes_kwargs(self):
        config = MyConfig(missing_option='NEW_VALUE')
        self.assertEqual(config.missing_option, 'NEW_VALUE')

    def test_class_name(self):
        self.assertEqual(MyConfig()._class_name, 'MyConfig')

    def test_dictionary_access(self):
        self.assertEqual(MyConfig()['default_option'], 'DEFAULT_VALUE')

    def test_attribute_access(self):
        self.assertEqual(MyConfig().default_option, 'DEFAULT_VALUE')

    def test_dictionary_setting(self):
        config = MyConfig()
        config['default_option'] = 'NEW_VALUE'
        self.assertEqual(config.default_option, 'NEW_VALUE')

    def test_attribute_setting(self):
        config = MyConfig()
        config.default_option = 'NEW_VALUE'
        self.assertEqual(config.default_option, 'NEW_VALUE')

    def test_dictionary_deletion_raises(self):
        config = MyConfig()
        with self.assertRaises(NotImplementedError):
            del config['default_option']

    def test_attribute_deletion_raises(self):
        config = MyConfig()
        with self.assertRaises(NotImplementedError):
            del config.default_option

    def test_dictionary_access_raises_for_unknown(self):
        config = MyConfig()
        with self.assertRaises(KeyError):
            config['NO_SUCH_OPTION']

    def test_attribute_access_raises_for_unknown(self):
        config = MyConfig()
        with self.assertRaises(AttributeError):
            config.NO_SUCH_OPTION

    def test_len(self):
        self.assertEqual(len(MyConfig()), 3)

    def test_iter(self):
        self.assertEqual(sorted([i for i in MyConfig()]),
                         ['default_option', 'lambda_option', 'missing_option'])

    def test_contains(self):
        self.assertTrue('default_option' in MyConfig())

    def test_contains_straightens(self):
        self.assertTrue('default-option' in MyConfig())

    def test_update_succeeds_with_new_settings(self):
        config = MyConfig()
        new_options = {'missing_option': 'NEW_VALUE_FOR_MISSING'}
        config.update(new_options)
        self.assertEqual(config.missing_option, 'NEW_VALUE_FOR_MISSING')

    def test_inject(self):
        config = MyConfig()
        new_options = {'missing_option': 'NEW_VALUE_FOR_MISSING'}
        config._inject(new_options)
        self.assertEqual(config.missing_option, 'NEW_VALUE_FOR_MISSING')

    def test_is_complete_fails_if_incomplete(self):
        config = MyConfig()
        with self.assertRaises(MissingConfigValues):
            config.is_complete()

    def test_is_complete_succeeds_if_complete(self):
        config = MyConfig()
        config.missing_option = "NOW_NO_LONGER_MISSING"
        self.assertTrue(config.is_complete())

    def test_validate_options_fails_for_unknown_option(self):
        config = MyConfig()
        new_options = {'no_such_option': 'NO_SUCH_OPTION'}
        with self.assertRaises(UnexpectedConfigValues):
            config.validate_options(new_options)

    def test_validate_options_succeeds_for_option_with_hyphen(self):
        config = MyConfig()
        new_options = {'missing-option': 'WITH_HYPHEN'}
        self.assertTrue(config.validate_options(new_options))

    def test_validate_options_succeeds_for_known_option(self):
        config = MyConfig()
        new_options = {'default_option': 'NEW_VALUE',
                       'lambda_option': 'NEW_VALUE',
                       'missing_option': None,
                       }
        self.assertTrue(config.validate_options(new_options))
