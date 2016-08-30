# Copyright 2015, Rackspace, US, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


default_keys = []


import unittest

from babel._compat import StringIO

from angular_gettext_babel.extract import extract_angular

default_keys = []


class ExtractAngularTestCase(unittest.TestCase):

    def test_extract_no_tags(self):
        buf = StringIO('<html></html>')

        messages = list(extract_angular(buf, default_keys, [], {}))
        self.assertEqual([], messages)

    def test_gettext_value(self):
        """Check we obtain multiple attributes
        """
        buf = StringIO('''<html><div attr1="{$ ::$root.i18n.gettext('hello world1') $}">hello world!</div></html>''')

        messages = list(extract_angular(buf, [], [], {}))
        self.assertEqual(
            [
                (1, u'gettext', 'hello world1', []),
            ],
            messages)

    def test_pgettext_value(self):
        """Check we obtain multiple attributes
        """
        buf = StringIO('''<html><div>{$ ::$root.i18n.pgettext('context', 'hello world') $}"</div></html>''')

        messages = list(extract_angular(buf, [], [], {}))
        self.assertEqual(
            [
                (1, u'gettext', 'hello world', []),
            ],
            messages)

    def test_ngettext_value(self):
        """Check we obtain multiple attributes
        """
        buf = StringIO('''<html><div>{$ ::$root.i18n.ngettext('hello world', 'hello worlds', 1) $}"</div></html>''')

        messages = list(extract_angular(buf, [], [], {}))
        self.assertEqual(
            [
                (1, u'ngettext', ('hello world', 'hello worlds'), []),
            ],
            messages)

    def test_lineextraction(self):
        buf = StringIO(
            """<html><a attribute="{$ ::$root.i18n.gettext('hello world!') $}">hello world!</a>'
            <div>{$ ::$root.i18n.gettext('hello world!') $}</div></html>"""
        )

        messages = list(extract_angular(buf, default_keys, [], {}))
        self.assertEqual(
            [
                (1, u'gettext', 'hello world!', []),
                (2, u'gettext', 'hello world!', [])
            ],
            messages)

    def test_multipleattr_values(self):
        """Check we obtain multiple attributes
        """
        buf = StringIO('''<html><div attr1="{$ ::$root.i18n.gettext('hello world1') $}" attr2="{$ ::$root.i18n.gettext('hello world2') $}">hello world!</div></html>''')

        messages = list(extract_angular(buf, [], [], {}))
        self.assertEqual(
            [
                (1, u'gettext', 'hello world1', []),
                (1, u'gettext', 'hello world2', [])
            ],
            messages)
