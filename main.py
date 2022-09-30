import os

import numpy as np
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter


def write_chunk(part, lines):
    with open(f'./divided_files/direccion_{part:05d}.csv', 'w') as f_out:
        f_out.write(header)
        f_out.writelines(lines)


if __name__ == '__main__':
    # delete previous files
    divided_files = './divided_files/'

    for filename in os.listdir(divided_files):
        file_path = os.path.join(divided_files, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

    # split csv file
    path = './raw_files/direccion.csv'
    chunk_size = 20

    with open(path, "r") as f:
        count = 0
        header = f.readline()
        lines = []
        for line in f:
            count += 1
            lines.append(line)
            if count % chunk_size == 0:
                write_chunk(count // chunk_size, lines)
                lines = []

        # write remainder
        if len(lines) > 0:
            write_chunk((count // chunk_size) + 1, lines)

    # geocoding files
    geolocator = Nominatim(user_agent='geocoding')
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

    processed_files = './processed_files/'
    for i, filename in enumerate(os.listdir(divided_files)):
        if i > 1: break
        print(filename)
        file_path = os.path.join(divided_files, filename)
        df = pd.read_csv(file_path)
        
        df['location'] = df['DIRECCION_COMPLETA'].apply(geocode)
        df['latitude'] = df['location'].apply(lambda loc: loc.latitude if loc else None)
        df['longitude'] = df['location'].apply(lambda loc: loc.longitude if loc else None)

        df.to_csv(os.path.join(processed_files, filename))

    # # join files
    # csv_list = []
    # for file in os.listdir(processed_files):
    #     csv_list.append(pd.read_csv(os.path.join(processed_files, file)).assign(File_name=os.path.basename(file)))
        
    # csv_merged = pd.concat(csv_list, ignore_index=True)
    # csv_merged.to_csv('./direccion.csv', index=False)

    # print(df.columns)
    # Index(['ID_DIRECCION', 'ID_TIPO_VIA', 'NOMBRE_VIA_DIRECCION', 'ID_PREFIJO_1_1',
    #        'NUMERO_VIA_GENERADORA_DIRECCION', 'ID_PREFIJO_1_2',
    #        'NUMERO_PLACA_DIRECCION', 'DATO_COMPLEMENTARIO_DIRECCION',
    #        'ID_CONTRATO', 'ID_CIUDAD', 'ID_DEPARTAMENTO', 'LONGITUD_DIRECCION',
    #        'LATITUD_DIRECCION', 'ID_PREFIJO_2_1', 'ID_PREFIJO_2_2', 'ESTRATO',
    #        'ID_COMPLEMENTO', 'DIRECCION_COMPLETA', 'DEPARTAMENTO', 'CIUDAD'],
    #       dtype='object')

    # print(df.head())
    #    ID_DIRECCION ID_TIPO_VIA NOMBRE_VIA_DIRECCION ID_PREFIJO_1_1  ... ID_COMPLEMENTO                           DIRECCION_COMPLETA     DEPARTAMENTO        CIUDAD
    # 0             1         AUT                    4            NaN  ...            NaN  AUTOPISTA 4 # 4 4,BOGOTÁ, D.C.,BOGOTÁ, D.C.     BOGOTÁ, D.C.  BOGOTÁ, D.C.
    # 1             2         AUT                   01            NaN  ...            NaN    AUTOPISTA 01 # 69 57,CALI,VALLE DEL CAUCA  VALLE DEL CAUCA          CALI
    # 2             3         AUT                    1            NaN  ...            NaN         AUTOPISTA 1 # 1 1,MEDELLÍN,ANTIOQUIA        ANTIOQUIA      MEDELLÍN
    # 3             4         AUT                    1            NaN  ...            NaN        AUTOPISTA 1 # 1 1,ABEJORRAL,ANTIOQUIA        ANTIOQUIA     ABEJORRAL
    # 4             5         AUT                    1            NaN  ...            NaN         AUTOPISTA 1 # 1 1,APARTADÓ,ANTIOQUIA        ANTIOQUIA      APARTADÓ

    # no_rows = len(df)
    # addresses = [np.NaN] * no_rows
    # latitudes = [np.NaN] * no_rows
    # longitudes = [np.NaN] * no_rows

    # for i, direccion in enumerate(df['DIRECCION_COMPLETA']):
    #     error = True

    #     while error:
    #         try:
    #             print(i)
    #             location = geolocator.geocode(direccion)
    #             if location is not None:
    #                 address = location.address
    #                 latitude = location.latitude
    #                 longitude = location.longitude
    #                 print(f'{address} ({latitude}, {longitude})')

    #                 addresses[i] = address
    #                 latitudes[i] = latitude
    #                 longitudes[i] = longitude

    #             error = False

    #         except:
    #             error = True

    # df['address'] = addresses
    # df['latitudes'] = latitudes
    # df['longitudes'] = longitudes

    # print(df.head())    
