# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8
# =============================================================================
# $Id: test_utils.py 69 2007-01-31 23:41:59Z s0undt3ch $
# =============================================================================
# $URL: http://i18ntoolbox.ufsoft.org/svn/branches/fresh-start/tests/test_utils.py $
# $LastChangedDate: 2007-01-31 23:41:59 +0000 (Wed, 31 Jan 2007) $
# $Rev: 69 $
# $LastChangedBy: s0undt3ch $
# =============================================================================
# Copyright (C) 2006 Ufsoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# Please view LICENSE for additional licensing information.
# =============================================================================

import unittest
from i18ntoolbox import utils
from nose.tools import raises

class TestAttrsDict(unittest.TestCase):

    def setUp(self):
        self.ad = utils.AttrsDict()

    def test_AddValueByAttribute(self):
        """utils.AttrsDict: Add a value to dict by attribute"""
        self.ad.foo = 'bar'
        assert hasattr(self.ad, 'foo')

    def test_GetValueByAttribute(self):
        """utils.AttrsDict: Get a value from dict by attribute"""
        self.ad.foo = 'bar'
        assert getattr(self.ad, 'foo') == 'bar'

    def test_AddValueByKey(self):
        """utils.AttrsDict: Add a value to dict by key"""
        self.ad['foo'] = 'bar'
        assert self.ad.has_key('foo')

    def test_GetValueByKey(self):
        """utils.AttrsDict: Get a value from dict by key"""
        self.ad['foo'] = 'bar'
        assert self.ad['foo'] == 'bar'

    def test_AttrsDictKeys(self):
        """utils.AttrsDict: Assure we have the 2 keys we've set"""
        self.ad.foo = 'bar'
        self.ad.bar = 'foo'
        assert 'bar' and 'foo' in self.ad.keys()

    def test_AttrsDictValues(self):
        """utils.AttrsDict: Assure we have the 2 values we've set"""
        self.ad.foo = 'bar'
        self.ad.bar = 'foo'
        assert 'bar' and 'foo' in self.ad.values()

    @raises(AttributeError)
    def test_AttrsDictRaiseAttributeError(self):
        "utils.AttrsDict: make sure that on KeyError we raise an AttributeError"
        assert self.ad.bar


class TestGetOptsHelpers(unittest.TestCase):

    def setUp(self):
        # Options parsed from cfgparser are always strings, so,
        # that's the options dictionary we build
        self.options = {}
        self.options['true'] = 'True'
        self.options['True'] = True
        self.options['false'] = 'False'
        self.options['False'] = False
        self.options['on'] = 'on'
        self.options['off'] = 'off'
        self.options['enabled'] = 'enabled'
        self.options['disabled'] = 'disabled'
        self.options['one'] = '1'
        self.options['two'] = '2'
        self.options['three'] = 3
        self.options['list'] = ['one', 'two']
        self.options['string'] = 'a random string'

    def test_GetBoolOpt(self):
        "utils.get_bool_opt: make sure we get a bool value"
        assert isinstance(utils.get_bool_opt(self.options, 'true'), bool)
        assert isinstance(utils.get_bool_opt(self.options, 'True'), bool)
        assert isinstance(utils.get_bool_opt(self.options, 'false'), bool)
        assert isinstance(utils.get_bool_opt(self.options, 'False'), bool)
        assert isinstance(utils.get_bool_opt(self.options, 'one'), bool)
        assert isinstance(utils.get_bool_opt(self.options, 'on'), bool)
        assert isinstance(utils.get_bool_opt(self.options, 'off'), bool)
        assert isinstance(utils.get_bool_opt(self.options, 'enabled'), bool)
        assert isinstance(utils.get_bool_opt(self.options, 'disabled'), bool)

    @raises(utils.OptionError)
    def test_GetBoolOptRaisesOptionErrorOnIntsBiggerThanOne(self):
        "utils.get_bool_opt: raises OptionError when trying to cast an int >1 to boolean"
        assert isinstance(utils.get_bool_opt(self.options, 'two'), bool)

    @raises(AttributeError)
    def test_GetBoolOptRaisesOptionErrorOnLists(self):
        "utils.get_bool_opt: raises AttributeError when trying to cast a list to boolean"
        assert isinstance(utils.get_bool_opt(self.options, 'list'), bool)

    @raises(utils.OptionError)
    def test_GetBoolOptRaisesOptionErrorOnRandomString(self):
        "utils.get_bool_opt: raises OptionError when trying to cast a random string to boolean"
        assert isinstance(utils.get_bool_opt(self.options, 'string'), bool)


    def test_GetIntOpt(self):
        "utils.get_int_opt: make sure we get an int value"
        assert isinstance(utils.get_int_opt(self.options, 'one'), int)
        assert isinstance(utils.get_int_opt(self.options, 'two'), int)
        assert isinstance(utils.get_int_opt(self.options, 'three'), int)

    @raises(utils.OptionError)
    def test_GetIntOptRaisesOptionErrorOnValuesOtherThanInts(self):
        "utils.get_int_opt: raises OptionError when trying to cast to int anything besides ints"
        assert isinstance(utils.get_int_opt(self.options, 'true'), int)
        assert isinstance(utils.get_int_opt(self.options, 'false'), int)
        assert isinstance(utils.get_int_opt(self.options, 'on'), int)
        assert isinstance(utils.get_int_opt(self.options, 'off'), int)
        assert isinstance(utils.get_int_opt(self.options, 'enabled'), int)
        assert isinstance(utils.get_int_opt(self.options, 'disabled'), int)
        assert isinstance(utils.get_int_opt(self.options, 'list'), int)
        assert isinstance(utils.get_int_opt(self.options, 'string'), int)


    def test_GetListOpt(self):
        "utils.get_list_opt: make sure we get a list"
        assert isinstance(utils.get_list_opt(self.options, 'list'), list)
        assert isinstance(utils.get_list_opt(self.options, 'string'), list)
        assert isinstance(utils.get_list_opt(self.options, 'true'), list)

    @raises(utils.OptionError)
    def test_GetListOptRaisesOptionErrorOnOtherThenListsTuplesStrings(self):
        "utils.get_list_opt: raises OptionError on values other than lists, tuples, strings"
        assert isinstance(utils.get_list_opt(self.options, 'three'), list)
        assert isinstance(utils.get_list_opt(self.options, 'True'), list)




if __name__ == '__main__':
    unittest.main()
