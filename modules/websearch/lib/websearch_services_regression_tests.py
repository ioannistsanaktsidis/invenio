# -*- coding: utf-8 -*-
##
## This file is part of Invenio.
## Copyright (C) 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2014 CERN.
##
## Invenio is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 2 of the
## License, or (at your option) any later version.
##
## Invenio is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with Invenio; if not, write to the Free Software Foundation, Inc.,
## 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

# pylint: disable=C0301
# pylint: disable=E1102

"""WebSearch services regression tests."""

__revision__ = "$Id$"

from invenio.testutils import InvenioTestCase
import time
import os
import traceback

from invenio.testutils import make_test_suite, \
    run_test_suite, \
    test_web_page_content, \
    merge_error_messages
from invenio.webuser import collect_user_info, get_uid_from_email
from invenio.pluginutils import PluginContainer
from invenio.search_engine import create_basic_search_units
from invenio.config import CFG_SITE_NAME, \
    CFG_SITE_SECURE_URL
from invenio.websearch_services import \
    get_search_services, \
    CFG_SEARCH_SERVICES_PATH, \
    __required_plugin_API_version__, \
    SearchService


class WebSearchServicesLoading(InvenioTestCase):

    """Check loading of WebSearch services"""

    def test_search_services_loading_time(self):
        """websearch - speed of loading all search services"""

        # Load search services, maybe first time
        t1 = time.time()
        get_search_services()
        t2 = time.time()
        search_services_loading_time = t2 - t1

        # We expect search services on the demo site to be loaded
        # in any case under 10 seconds
        max_seconds_services_loading_time_first_time = 10
        if search_services_loading_time > max_seconds_services_loading_time_first_time:
            self.fail("""Loading Search services (from scratch) took too much time:
%s seconds.
Limit: %s seconds""" % (search_services_loading_time,
                        max_seconds_services_loading_time_first_time))

        # Load search services, hopefully from cache
        t1 = time.time()
        get_search_services()
        t2 = time.time()
        search_services_loading_time = t2 - t1

        # We expect search services on the demo site to be loaded
        # under 1 second, i.e. retrieved from cache
        max_seconds_services_loading_time_from_cache = 1
        if search_services_loading_time > max_seconds_services_loading_time_from_cache:
            self.fail("""Loading Search services from cache took too much time:
%s seconds.
Limit: %s second""" % (search_services_loading_time,
                       max_seconds_services_loading_time_from_cache))


    def test_no_broken_search_services_(self):
        """websearch - no broken search services"""
        error_messages = []
        search_service_plugins = PluginContainer(
            os.path.join(CFG_SEARCH_SERVICES_PATH, '*Service.py'),
            api_version=__required_plugin_API_version__,
            plugin_signature=SearchService
        )
        for name, error in search_service_plugins.get_broken_plugins().iteritems():
            error_messages.append("Service '%s' could not be loaded:\n%s" %
                                  (name, repr(error[0]) + " " + repr(error[1]) + "\n" + "\n".join(traceback.format_tb(error[2]))))

        if error_messages:
            self.fail(merge_error_messages(error_messages))





class WebSearchServicesJournalHintService(InvenioTestCase):
    """Check JournalHintService plugin"""

    def setUp(self):
        """Load plugin"""
        search_service_plugins = PluginContainer(os.path.join(CFG_SEARCH_SERVICES_PATH, '*Service.py'),
                                                 api_version=__required_plugin_API_version__,
                                                 plugin_signature=SearchService)
        self.plugin = search_service_plugins.get('JournalHintService')()

    def test_search_author_Tom(self):
        """websearch - search for an author using invenio sintax, with JournalHintService"""
        user_info = collect_user_info(0)
        pattern = 'author:Tom'
        search_units = create_basic_search_units(None, pattern, '')
        response = self.plugin.answer(req=user_info, user_info=user_info, of='hb',
                                      cc=CFG_SITE_NAME, colls_to_search='', p=pattern,
                                      f='', search_units=search_units, ln='en')
        self.assertEqual(response,
                         (0, ''))

    def test_search_find_a_John(self):
        """websearch - search 'find a John', with JournalHintService"""
        user_info = collect_user_info(0)
        pattern = 'find a John'
        search_units = create_basic_search_units(None, pattern, '')
        response = self.plugin.answer(req=user_info, user_info=user_info, of='hb',
                                      cc=CFG_SITE_NAME, colls_to_search='', p=pattern,
                                      f='', search_units=search_units, ln='en')
        self.assertEqual(response,
                         (0, ''))

    def test_search_date_after_2001(self):
        """websearch - search 'find date after 2001', with JournalHintService"""
        user_info = collect_user_info(0)
        pattern = 'find date after 2001'
        search_units = create_basic_search_units(None, pattern, '')
        response = self.plugin.answer(req=user_info, user_info=user_info, of='hb',
                                      cc=CFG_SITE_NAME, colls_to_search='', p=pattern,
                                      f='', search_units=search_units, ln='en')
        self.assertEqual(response,
                         (0, ''))

    def test_search_year_2001_or_year_2002(self):
        """websearch - search 'year:2001 OR year:2002', with JournalHintService"""
        user_info = collect_user_info(0)
        pattern = 'year:2001 OR year:2002'
        search_units = create_basic_search_units(None, pattern, '')
        response = self.plugin.answer(req=user_info, user_info=user_info, of='hb',
                                      cc=CFG_SITE_NAME, colls_to_search='', p=pattern,
                                      f='', search_units=search_units, ln='en')
        self.assertEqual(response,
                         (0, ''))

    def test_search_Monkey(self):
        """websearch - search 'Monkey', with JournalHintService"""
        user_info = collect_user_info(0)
        pattern = 'Monkey'
        search_units = create_basic_search_units(None, pattern, '')
        response = self.plugin.answer(req=user_info, user_info=user_info, of='hb',
                                      cc=CFG_SITE_NAME, colls_to_search='', p=pattern,
                                      f='', search_units=search_units, ln='en')
        self.assertEqual(response,
                         (0, ''))

    def test_search_Monkey_monkey(self):
        """websearch - search 'Monkey monkey', with JournalHintService"""
        user_info = collect_user_info(0)
        pattern = 'Monkey monkey'
        search_units = create_basic_search_units(None, pattern, '')
        response = self.plugin.answer(req=user_info, user_info=user_info, of='hb',
                                      cc=CFG_SITE_NAME, colls_to_search='', p=pattern,
                                      f='', search_units=search_units, ln='en')
        self.assertEqual(response,
                         (0, ''))

    def test_search_Monkey_monkey_2014(self):
        """websearch - search 'Monkey monkey (2014)', with JournalHintService"""
        user_info = collect_user_info(0)
        pattern = 'Monkey monkey (2014)'
        search_units = create_basic_search_units(None, pattern, '')
        response = self.plugin.answer(req=user_info, user_info=user_info, of='hb',
                                      cc=CFG_SITE_NAME, colls_to_search='', p=pattern,
                                      f='', search_units=search_units, ln='en')
        self.assertEqual(response,
                         (0, ''))

    def test_search_empty_string(self):
        """websearch - search empty string, with JournalHintService"""
        user_info = collect_user_info(0)
        pattern = ''
        search_units = create_basic_search_units(None, pattern, '')
        response = self.plugin.answer(req=user_info, user_info=user_info, of='hb',
                                      cc=CFG_SITE_NAME, colls_to_search='', p=pattern,
                                      f='', search_units=search_units, ln='en')
        self.assertEqual(response,
                         (0, ''))

    def test_search_Nucl_Phys_B75_1974_461(self):
        """websearch - search 'Nucl.Phys.,B75,(1974),461', with JournalHintService"""
        user_info = collect_user_info(1)
        pattern = "Nucl.Phys.,B75,(1974),461"
        search_units = create_basic_search_units(None, pattern, '')
        response = self.plugin.answer(req=user_info, user_info=user_info, of='hb',
                                      cc=CFG_SITE_NAME, colls_to_search='', p=pattern,
                                      f='', search_units=search_units, ln='en')
        self.assertEqual(response, (0, ''))

    def test_search_Nucl_Phys_B75_1974_461_with_spaces(self):
        """websearch - search '  Nucl.  Phys.   B75   (1974)  461   ', with JournalHintService"""
        user_info = collect_user_info(1)
        pattern = '  Nucl.  Phys.   B75   (1974)  461   '
        search_units = create_basic_search_units(None, pattern, '')
        response = self.plugin.answer(req=user_info, user_info=user_info, of='hb',
                                      cc=CFG_SITE_NAME, colls_to_search='', p=pattern,
                                      f='', search_units=search_units, ln='en')
        self.assertEqual(response, (0, ''))

    def test_search_Nucl_Instrum_Methods_Phys_Res_A_445_2000_456_462(self):
        """webseach - search 'Nucl. Instrum. Methods Phys. Res., A :445 2000 456-462', with JournalHintService"""
        user_info = collect_user_info(1)
        pattern = 'Nucl. Instrum. Methods Phys. Res., A :445 2000 456-462'
        search_units = create_basic_search_units(None, pattern, '')
        response = self.plugin.answer(req=user_info, user_info=user_info, of='hb',
                                      cc=CFG_SITE_NAME, colls_to_search='', p=pattern,
                                      f='', search_units=search_units, ln='en')
        self.assert_(response[0] >=50)
        self.assert_('Development of photon beam diagnostics for VUV radiation from a SASE FEL' in response[1])

    def test_search_D_S_Salopek_J_R_Bond_and_J_M_Bardeen_Phys_Rev_D40_1989_1753(self):
        """websearch - search 'D.S. Salopek, J.R.Bond and J.M.Bardeen,Phys.Rev.D40(1989)1753.', with JournalHintService"""
        user_info = collect_user_info(1)
        pattern = 'D.S. Salopek, J.R.Bond and J.M.Bardeen,Phys.Rev.D40(1989)1753.'
        search_units = create_basic_search_units(None, pattern, '')
        response = self.plugin.answer(req=user_info, user_info=user_info, of='hb',
                                      cc=CFG_SITE_NAME, colls_to_search='', p=pattern,
                                      f='', search_units=search_units, ln='en')
        self.assertEqual(response, (0, ''))

    def test_search_Capella_Pere_utf8(self):
        """websearch - search 'Capellà Pere' utf8, with JournalHintService"""
        user_info = collect_user_info(0)
        pattern = u'Capellà Pere'.encode('utf8')
        search_units = create_basic_search_units(None, pattern, '')
        response = self.plugin.answer(req=user_info, user_info=user_info, of='hb',
                                      cc=CFG_SITE_NAME, colls_to_search='', p=pattern,
                                      f='', search_units=search_units, ln='en')
        self.assertEqual(response,
                         (0, ''))

    def test_search_Pais_Valencia_utf8(self):
        """websearch - search 'País Valencià' utf8, with JournalHintService"""
        user_info = collect_user_info(0)
        pattern = u'País Valencià'.encode('utf8')
        search_units = create_basic_search_units(None, pattern, '')
        response = self.plugin.answer(req=user_info, user_info=user_info, of='hb',
                                      cc=CFG_SITE_NAME, colls_to_search='', p=pattern,
                                      f='', search_units=search_units, ln='en')
        self.assertEqual(response,
                         (0, ''))


TEST_SUITE = make_test_suite(WebSearchServicesLoading,
                             WebSearchServicesJournalHintService)

if __name__ == "__main__":
    run_test_suite(TEST_SUITE, warn_user=True)
