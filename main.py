import numpy as np
import pandas as pd
from geopy.geocoders import Nominatim


df = pd.read_csv('./data/direccion.csv')


geolocator = Nominatim(user_agent="geocoding")

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

no_rows = len(df)
addresses = [np.NaN] * no_rows
latitudes = [np.NaN] * no_rows
longitudes = [np.NaN] * no_rows

for i, direccion in enumerate(df['DIRECCION_COMPLETA']):
    error = True

    while error:
        try:
            print(i)
            location = geolocator.geocode(direccion)
            if location is not None:
                address = location.address
                latitude = location.latitude
                longitude = location.longitude
                print(f'{address} ({latitude}, {longitude})')

                addresses[i] = address
                latitudes[i] = latitude
                longitudes[i] = longitude

            error = False

        except:
            error = True

df['address'] = addresses
df['latitudes'] = latitudes
df['longitudes'] = longitudes

print(df.head())

df.to_csv('./data/direccion_nominatim.csv')


