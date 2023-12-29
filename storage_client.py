import os
from azure.data.tables import TableServiceClient
from azure.core.exceptions import ResourceNotFoundError
import urllib.parse


def get_client():
    connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    table_service_client = TableServiceClient.from_connection_string(
        conn_str=connection_string)
    table_client = table_service_client.get_table_client(table_name="urls")
    return table_client


def get_url_count():
    table_client = get_client()
    try:
        entities = table_client.query_entities(
            query_filter="PartitionKey eq 'short_url'")
        # count the number of short urls
        count = 0
        for entity in entities:
            count += 1
        return count
    except Exception as e:
        return 0


def store_url(url, short_url, is_custom):
    table_client = get_client()
    table_client.create_entity(entity={
        'PartitionKey': 'short_url',
        'RowKey': short_url,
        'url': urllib.parse.quote_plus(url)
    })

    # we only want to store urls bidirectionally if they are not custom
    if not is_custom:
        table_client.create_entity(entity={
            'PartitionKey': 'url',
            'RowKey': urllib.parse.quote_plus(url),
            'short_url': short_url
        })


def get_full_url(short_url):
    table_client = get_client()
    try:
        entity = table_client.get_entity(
            partition_key='short_url', row_key=short_url)
        return entity.get('url'), 200
    except ResourceNotFoundError:
        return None, 404
    except Exception as e:
        return None, 500


def check_full_url(url):
    table_client = get_client()
    try:
        entity = table_client.get_entity(
            partition_key='url', row_key=urllib.parse.quote_plus(url))
        return entity.get('short_url'), 200
    except ResourceNotFoundError:
        return None, 404
    except Exception as e:
        return None, 500


def check_short_url(short_url):
    table_client = get_client()
    try:
        raise Exception("test")
        entity = table_client.get_entity(
            partition_key='short_url', row_key=short_url)
        return True, 200
    except ResourceNotFoundError:
        return False, 404
    except Exception as e:
        return False, 500
