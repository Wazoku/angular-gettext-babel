try:
    from html.parser import HTMLParser
except ImportError:
    from HTMLParser import HTMLParser

import locale
import logging
import re


def interpolate(data):
    interpolation_regex = r"""{\$([\w\."'\]\[\(\)]+)\$}"""
    return re.sub(interpolation_regex, r'%(\1)', data)


class AngularGettextHTMLParser(HTMLParser):
    """Parse HTML to find translate directives.

    Note: This will not cope with nested tags (which I don't think make any
    sense)
    """

    def __init__(self):
        try:
            super(self.__class__, self).__init__()
        except TypeError:
            HTMLParser.__init__(self)

        self.in_translate = False
        self.data = []
        self.strings = []
        self.line = 0
        self.plural = False
        self.plural_form = ''
        self.comments = []

    def find_matches(self, string):
        for match in self._find_matches(string):
            if type(match) == tuple and len(match) == 2:
                self._add_plural_string(match[0], match[1])
            elif type(match) == tuple and len(match) == 3:
                self._add_context_string(match[0], match[1])
            else:
                self._add_string(match)

    def _find_matches(self, string):
        matches = []
        if not string:
            return []
        match = re.findall(r'\.gettext\(["\'](.*?)["\']\)', string)
        if match:
            matches.extend(match)
        match = re.findall(r'\.pgettext\(["\'](.*?)["\'], +["\'](.*?)["\']\)', string)
        if match:
            matches.extend([match[0] + ('+context',)])
        match = re.findall(
            r'\.ngettext\(["\'](.*?)["\'], +["\'](.*?)["\'],[^)]*\)', string)
        if match:
            matches.extend(match)
        return matches

    def _add_string(self, singular, comments=''):
        messages = interpolate(singular)
        self._add_msg(u'gettext', messages, comments)

    def _add_plural_string(self, singular, plural_form, comments=''):
        messages = (
            interpolate(singular),
            interpolate(plural_form)
        )
        self._add_msg(u'ngettext', messages, comments)

    def _add_context_string(self, singular, context, comments=''):
        messages = (
            interpolate(singular),
            interpolate(context)
        )
        self._add_msg(u'pgettext', messages, comments)

    def _add_msg(self, func_name, messages, comments):
        line = self.getpos()[0]
        if not comments:
            comments = []
        self.strings.append(
            (line, func_name, messages, comments)
        )

    def handle_starttag(self, tag, attrs):
        for attr, val in attrs:
            self.find_matches(val)

    def handle_data(self, data):
        self.find_matches(data)


def extract_angular(fileobj, keywords, comment_tags, options):
    """Extract messages from angular template (HTML) files

    :param fileobj: the file-like object the messages should be extracted
                    from
    :param keywords: This is a standard parameter so it is accepted but ignored.

    :param comment_tags: This is a standard parameter so it is accepted but
                        ignored.
    :param options: Another standard parameter that is accepted but ignored.
    :return: an iterator over ``(lineno, funcname, message, comments)``
             tuples
    :rtype: ``iterator``
    """
    if keywords:
        logging.debug('Parameter keywords ignored.')

    if comment_tags:
        logging.debug('Parameter comment_tags ignored.')

    if options:
        logging.debug('Parameter options ignored.')

    parser = AngularGettextHTMLParser()

    for line in fileobj:
        if not isinstance(line, str):
            line = line.decode(locale.getpreferredencoding())
        parser.feed(line)

    for string in parser.strings:
        yield(string)
