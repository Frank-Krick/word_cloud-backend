import requests, whoosh.index, analyzer


INDEX_OUTPUT_DIRECTORY = '/mnt/data/index/'


WIKI_LEAKS_PODESTA_BASE_URL = 'https://www.wikileaks.org/podesta-emails/get/'


class EMailSchema(whoosh.fields.SchemaClass):
    url = whoosh.fields.ID(stored=True)
    content = whoosh.fields.TEXT()
    subject = whoosh.fields.TEXT()


def add_emails(index, base, email_ids):
    for i in email_ids:
        add_email(index, base, i)


def add_email(index, base, email_id):
    email_bytes = get_from_wikileaks_by_index(base, email_id)
    content = analyzer.retrieve_email_content(email_bytes, base + str(email_id))
    subject = analyzer.retrieve_subject(email_bytes)
    writer = index.writer()
    writer.add_document(url = base + str(email_id),
                        content = content,
                        subject = subject)
    writer.commit()


def open_index(path):
    if whoosh.index.exists_in(INDEX_OUTPUT_DIRECTORY):
        return whoosh.index.open_dir(INDEX_OUTPUT_DIRECTORY)
    else:
        return whoosh.index.create_in(INDEX_OUTPUT_DIRECTORY,
                                      create_schema())


def create_schema():
    return EMailSchema() 


def get_from_wikileaks_by_index(base, index):
    url = base + str(index)
    return requests.get(url).content


index = open_index(INDEX_OUTPUT_DIRECTORY)


