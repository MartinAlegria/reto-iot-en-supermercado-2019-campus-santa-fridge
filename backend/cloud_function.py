import base64
import json
from google.api_core import retry
from google.cloud import bigquery

BQ_DATASET = 'semana_i'
BQ_TABLE_CAMARA = 'datos_camara'
BQ_TABLE_RFID = 'datos_rfid'
BQ = bigquery.Client()

tabla_camara = [
        bigquery.SchemaField('ts', 'TIMESTAMP', mode='NULLABLE'),
        bigquery.SchemaField('edad', 'INTEGER', mode='NULLABLE'),
        bigquery.SchemaField('genero', 'STRING', mode='NULLABLE'),
        bigquery.SchemaField('id_sesion', 'INTEGER', mode='NULLABLE'),
        bigquery.SchemaField('device_id', 'STRING', mode='NULLABLE')
        ]

tabla_rfid = [
        bigquery.SchemaField('ts', 'TIMESTAMP', mode='NULLABLE'),
        bigquery.SchemaField('rfid_id', 'INTEGER', mode='NULLABLE'),
        bigquery.SchemaField('sku', 'STRING', mode='NULLABLE'),
        bigquery.SchemaField('nombre', 'STRING', mode='NULLABLE'),
        bigquery.SchemaField('id_sesion', 'INTEGER', mode='NULLABLE'),
        bigquery.SchemaField('device_id', 'STRING', mode='NULLABLE')
        ]

def process_data(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
        event (dict): Event payload.
        context (google.cloud.functions.Context): Metadata for the event.
    """
    pubsub_message = json.loads(base64.b64decode(event['data']).decode('utf-8'))
    print(pubsub_message)
    try:
        _insert_into_bigquery(pubsub_message)

    except  BigQueryError as e:
        print(e.errors)


def _insert_into_bigquery(message):
    print()
    print(message['device_id'])
    if message['device_id'] == 'camara':
        table = BQ.dataset(BQ_DATASET).table(BQ_TABLE_CAMARA)
        errors = BQ.insert_rows(table, [message], selected_fields = tabla_camara )
        if errors != []:
            raise BigQueryError(errors)
    else:
        if message['device_id'] == 'rfid':
            print("Good syntax")
            table = BQ.dataset(BQ_DATASET).table(BQ_TABLE_RFID)
            errors = BQ.insert_rows(table, [message], selected_fields = tabla_rfid )
            if errors != []:
                raise BigQueryError(errors)
class BigQueryError(Exception):
    '''Exception raised whenever a BigQuery error happened'''

    def __init__(self, errors):
        super().__init__(self._format(errors))
        self.errors = errors

    def _format(self, errors):
        err = []
        for error in errors:
            err.extend(error['errors'])
        return json.dumps(err)
