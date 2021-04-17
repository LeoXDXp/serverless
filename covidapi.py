from googleapiclient.discovery import build
from google.oauth2 import service_account
import os
#from flask import jsonify

def covidEndPoint(request):
    json_content = request.get_json()
    get_content = request.args
    if get_content and 'comuna' in get_content:
        comuna = get_content['comuna']
    elif json_content and 'comuna' in json_content:
        comuna = json_content['comuna']
    else:
        comuna = "Valparaíso"
    # Comuna esta en la columna D
    sheetRange = "confirmados_comunas!D2:D347"

    service = build('sheets', 'v4', credentials=None)
    sheet = service.spreadsheets()
    result = service.spreadsheets().values().get(
        spreadsheetId=os.environ.get("SPREADSHEET_ID","0"),
        range=sheetRange).execute()
    values = result.get('values', [])
    del result

    if not len(values):
        return {'comuna':comuna, 'error': "sin data"}

    cntr = 2
    for com in values:
        if com[0].lower() == comuna.lower():
            break
        cntr += 1
    del values
    # Datos van de la columna E a la AR.
    sheetRange = "confirmados_comunas!E"+ str(cntr) + ":AR" + str(cntr)
    result = service.spreadsheets().values().get(
        spreadsheetId=os.environ.get("SPREADSHEET_ID","0"),
        range=sheetRange).execute()
    values = result.get('values', [])
    del result

    headerRange = "confirmados_comunas!E1:AR1"
    result = service.spreadsheets().values().get(
        spreadsheetId=os.environ.get("SPREADSHEET_ID","0"),
        range=headerRange).execute()
    headers = result.get('values', [])
    del result
    data = dict(zip(headers[0], values[0]))
    del values
    del headers
    data["comuna"] = comuna
    data["contador"] = cntr
    return data
