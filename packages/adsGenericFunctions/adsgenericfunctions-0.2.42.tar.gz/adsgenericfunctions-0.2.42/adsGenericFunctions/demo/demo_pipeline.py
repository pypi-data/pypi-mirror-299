from adsGenericFunctions import pipelineBulk
from adsGenericFunctions.logger import Logger
from adsGenericFunctions.global_config import set_timer
from adsGenericFunctions.dbPgsql import dbPgsql
from adsGenericFunctions.pipeline import pipeline
from to_sort.env import *
import logging
import psycopg2

# On établit une connexion pour le logger pour qu'il puisse écrire en base
logger_connection = psycopg2.connect(database=pg_dwh_db, user=pg_dwh_user, password=pg_dwh_pwd, port=pg_dwh_port,
                                     host=pg_dwh_host)
logger = Logger(logger_connection, logging.INFO, "AdsLogger", "LOGS", "LOGS_details")
logger.info("Début de la démonstration...")

# On active le timer, les requêtes seront chronométrées
set_timer(True)

source = dbPgsql({'database':pg_dwh_db
                    , 'user':pg_dwh_user
                    , 'password':pg_dwh_pwd
                    , 'port':pg_dwh_port
                    , 'host':pg_dwh_host}, logger)

destination = dbPgsql({'database':pg_dwh_db
                    , 'user':pg_dwh_user
                    , 'password':pg_dwh_pwd
                    , 'port':pg_dwh_port
                    , 'host':pg_dwh_host}, logger)

# Créons une table de démonstration
destination.connect()
destination.exec('''
CREATE TABLE IF NOT EXISTS demo_pipeline (
    id SERIAL PRIMARY KEY,
    tenantname VARCHAR(255),
    taille FLOAT(8),
    unite VARCHAR(10),
    fichier VARCHAR(255)
);
''')

query = '''
SELECT tenantname, taille, unite, fichier
FROM onyx_qs."diskcheck" LIMIT 3
'''

# Attention si on passe une liste de lignes à insérer à un pipeline simple, elles seront insérées une par une
# Loguée une par une et timée une par une
pipeline = pipeline({'db_source': source, 'query_source': query, 'db_destination': destination,
                         'table': 'demo_pipeline', 'cols': ['tenantname', 'taille', 'unite', 'fichier']}, logger)
pipeline.run()

# Si vous voulez insérer plusieurs lignes, utilisez plutôt
pipelineBulk = pipelineBulk({'db_source': source, 'query_source': query, 'db_destination': destination,
                         'table': 'demo_pipeline', 'cols': ['tenantname', 'taille', 'unite', 'fichier']}, logger)
pipelineBulk.run()

# Supprimons la table
destination.exec(''' DROP TABLE demo_pipeline ''')
logger.info("Fin de la démonstration")
