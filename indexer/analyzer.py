import functools, email.parser, re
from html.parser import HTMLParser


parser = email.parser.BytesParser()


class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.content = []


    def handle_data(self, data):
        self.content = self.content + [data]


def parse_email(email_string):
    return parser.parsebytes(email_string)


def retrieve_subject(email_bytes):
    message = parse_email(email_bytes)
    return retrieve_subject_from_message(message)


def retrieve_subject_from_message(message):
    subjects = message.get_all('subject')
    if message.is_multipart():
        child_messages = message.get_payload()
        subjects = subjects + list(map(lambda x: x.get_all('subject'), child_messages))
    return list(filter(None, subjects))


def retrieve_email_content(email_string, url):
    print('processing: ' + url)
    message = parse_email(email_string)
    payload_strings = extract_payload_strings(message)
    plain_text = map(extract_plain_text_content, payload_strings)
    combined = functools.reduce(lambda x, y: x + y, functools.reduce(lambda x, y: x + y, plain_text))
    line_ends_removed = combined.replace('\n', ' ').replace('\r', ' ').replace('\xa0', '')
    return re.sub(r"\s+", ' ', re.sub(r"<!-- .*-->", '', re.sub(r"= *", '', line_ends_removed)))


def extract_payload_strings(message):
    if message.is_multipart():
        child_messages = message.get_payload()
        content = map(extract_payload_strings, child_messages)
        return functools.reduce(lambda x, y: x + y, content)
    else:
        return [(message.get_payload(), message.get('content-type').split(';')[0])]


def extract_plain_text_content(payload_string):
    if payload_string[1] == 'text/plain':
        return [payload_string[0]]
    elif payload_string[1] == 'text/html':
        return parse_html_content(payload_string[0])
    else:
        print('Unknown content type: ' + payload_string[1])
        return ['']


def parse_html_content(html_string):
    html_parser = MyHTMLParser()
    html_parser.feed(html_string)
    return html_parser.content


