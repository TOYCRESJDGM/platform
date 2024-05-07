import os
import re
import pymysql
from logger import logger
from datetime import datetime
from scrapper import scrapper_platform



def insert_single_record(connection, table, data, code):
    existing_data = None
    new_id = None
    message = 'Successful operation'
    error = None
    try:
        with connection.cursor() as cursor:
            #Crear la consulta de selección basada en el diccionario code
            if code and isinstance(code, dict):
                where_clause = ' AND '.join(["{} = %s".format(key) for key in code.keys()])
                sql_select = "SELECT * FROM {} WHERE {}".format(table, where_clause)
                
                # Ejecutar la consulta de selección
                cursor.execute(sql_select, tuple(code.values()))
                existing_data = cursor.fetchone()
                
            if not existing_data:
                # Crear la consulta de inserción
                columns = ', '.join(data.keys())
                placeholders = ', '.join(['%s'] * len(data))
                sql_insert = "INSERT INTO {} ({}) VALUES ({})".format(table, columns, placeholders)
                
                # Ejecutar la consulta de inserción
                cursor.execute(sql_insert, tuple(data.values()))
                connection.commit()

                new_id = cursor.lastrowid
            else:
                new_id = existing_data.get('id')
                
            return new_id, message, error

    except Exception as e:
        error = str(e)
        message = 'Error occurred while inserting data: {}'.format(error)
        logger.error(message)
        return None, message, error


def insert_multiple_records(connection, table, data):

    with connection.cursor() as cursor:
        # Crear la consulta de inserción
        columns = ', '.join(data[0].keys())
        placeholders = ', '.join(['%s'] * len(data[0]))
        sql_insert = "INSERT INTO {} ({}) VALUES ({})".format(table, columns, placeholders)
        
        # Obtener los valores de los datos a insertar
        values = [tuple(item.values()) for item in data]
        
        # Ejecutar la consulta de inserción múltiple
        cursor.executemany(sql_insert, values)
        connection.commit()


def search_code(data):

    if 'document_number' in data:
        return {
            'document_number':data.get('document_number')
        }
    elif 'number_invoice' in data:
        return {
            'number_invoice': data.get('number_invoice')
        }
    else:
        return None


def save_data(data, table):
    # Conexión a la base de datos    
    connection = pymysql.connect(host=os.getenv('DB_HOST'),
                                user=os.getenv('DB_USER'),
                                password=os.getenv('DB_PASSWORD'),
                                database=os.getenv('DB_NAME'),
                                cursorclass=pymysql.cursors.DictCursor)
    
    if table == os.getenv('TABLE_EVENT'):
        insert_multiple_records(connection, table, data)

    else:

        code = search_code(data)
        new_id, message, error = insert_single_record(connection, table, data, code)
        if not error:
            return new_id
    
        logger.error(error)


                

def validate_data(receptor, transmitter, total_taxes, invoice_info, url_pdf, events):

    logger.info('Validando información...')
    # Verificar que todos los campos obligatorios estén presentes y no estén vacíos
    if not all([receptor, transmitter, total_taxes, invoice_info, url_pdf, events]):
        return False

    if not isinstance(receptor, dict) or not isinstance(transmitter, dict) or not isinstance(total_taxes, dict) or not isinstance(invoice_info, dict):
        return False

    if not all([receptor.get('NIT'), receptor.get('Nombre')]):
        return False

    if not all([transmitter.get('NIT'), transmitter.get('Nombre')]):
        return False

    if not all([total_taxes.get('IVA'), total_taxes.get('Total')]):
        return False
    
    if not all([invoice_info.get('Serie'), invoice_info.get('Folio'), invoice_info.get('Fecha de emisión de la factura Electrónica')]):
        return False
    
    if not isinstance(url_pdf, str):
        return False
    
    return True


def map_records_information(records):
    
    return {
        'document_number':records['NIT'],
        'name': records['Nombre']
    }
    

def map_number_value(value):
   
    patron = r"\$([\d,]+)"

    resultado = re.search(patron, value)

    if resultado:
        numero_sin_simbolo = resultado.group(1)
        
        numero_sin_comas = numero_sin_simbolo.replace(",", "")
        
        return int(numero_sin_comas)

    return 0  


def map_record_invoice(cufe, total_taxes, invoice_info, url_pdf, seller_id, receiver_id):
    
    return {
        'number_invoice': cufe,
        'date_issued' : convert_date(invoice_info.get('Fecha de emisión de la factura Electrónica')),
        'folio': invoice_info.get('Folio'),
        'series': invoice_info.get('Serie'),
        'pdf_url': url_pdf,
        'emitter_id': seller_id,
        'receiver_id': receiver_id,
        'tax': map_number_value(total_taxes.get('IVA')),
        'total': map_number_value(total_taxes.get('Total')),
    }


def convert_date(date):
    date_datetime = datetime.strptime(date, '%d-%m-%Y')

    return date_datetime.strftime('%Y-%m-%d')
            

def map_record_events(invoice_id, event):
    return {
        'invoice_id': invoice_id,
        'code': event.get('code'),
        'description': event.get('description'),
        'date_event': event.get('date')
    }


def process_cufe(cufe):

    try:

        logger.info('Procesando...')
    
        receptor, transmitter, total_taxes, invoice_info, url_pdf, events = scrapper_platform(cufe)

        if(validate_data(receptor, transmitter, total_taxes, invoice_info, url_pdf, events)):
            seller = map_records_information(transmitter)
            receiver = map_records_information(receptor)

            seller_id = save_data(seller, os.getenv('TABLE_EMITTERS'))
            receiver_id = save_data(receiver, os.getenv('TABLE_RECEIVERS'))

            invoice = map_record_invoice(cufe, total_taxes, invoice_info, url_pdf, seller_id, receiver_id)

            invoice_id = save_data(invoice, os.getenv('TABLE_INVOICE'))

            records_event = []
            for event in events:
                records_event.append(map_record_events(invoice_id, event))
                        
            save_data(records_event, os.getenv('TABLE_EVENT')) 
            logger.info('Procesamiento exitoso')

    except Exception as e:
        logger.error(e)

