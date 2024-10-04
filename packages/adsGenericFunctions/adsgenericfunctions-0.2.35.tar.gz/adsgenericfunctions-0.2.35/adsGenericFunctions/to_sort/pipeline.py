import logging

class pipeline:
    def __init__(self, dictionnary : dict):
        self.__logger = logging.getLogger('adsGenericFunctions')
        self.__db_source=dictionnary['db_source']
        self.__query_source=dictionnary['query_source']
        self.__db_destination=dictionnary['db_destination']
        self.__table=dictionnary['table']
        self.__cols=dictionnary['cols']

    def run(self):
        try:

            self.__logger.info(f"Connexion établie avec la base de données.")
            self.__db_source.connect()
            self.__db_destination.connect()

            data=[]
            [data.append(element) for element in self.__db_source.sqlQuery(self.__query_source)]
            self.__db_destination.insert(table=self.__table, cols=self.__cols,rows=data)

        except Exception as e:
            self.__logger.error(f"Échec de la connexion à la base de données.")
            raise

class pipelineTableau:
    def __init__(self, dictionnary : dict):
        self.__logger = logging.getLogger('adsGenericFunctions')
        self.__tableau=dictionnary['tableau']
        self.__db_destination=dictionnary['db_destination']
        self.__table=dictionnary['table']
        self.__cols=dictionnary['cols']

    def run(self):
        try:

            self.__logger.info(f"Connexion établie avec la base de données.")
            self.__db_destination.connect()

            data=[]
            [data.append(element) for element in self.__tableau]
            self.__db_destination.insert(table=self.__table, cols=self.__cols,rows=data)

        except Exception as e:
            self.__logger.error(f"Échec de la connexion à la base de données.")
            raise


class pipelineBulk:
    def __init__(self, dictionnary : dict):
        self.__logger = logging.getLogger('adsGenericFunctions')
        self.__db_source=dictionnary['db_source']
        self.__query_source=dictionnary['query_source']
        self.__db_destination=dictionnary['db_destination']
        self.__table=dictionnary['table']
        self.__cols=dictionnary['cols']

    def run(self):
        try:

            self.__logger.info(f"Connexion établie avec la base de données.")
            self.__db_source.connect()
            self.__db_destination.connect()

            data=[]
            [data.append(element) for element in self.__db_source.sqlQuery(self.__query_source)]
            self.__db_destination.insertBulk(table=self.__table, cols=self.__cols,rows=data)

        except Exception as e:
            self.__logger.error(f"Échec de la connexion à la base de données.")
            raise

class pipelineTableauBulk:
    def __init__(self, dictionnary : dict):
        self.__logger = logging.getLogger('adsGenericFunctions')
        self.__tableau=dictionnary['tableau']
        self.__db_destination=dictionnary['db_destination']
        self.__table=dictionnary['table']
        self.__cols=dictionnary['cols']

    def run(self):
        try:

            self.__logger.info(f"Connexion établie avec la base de données.")
            self.__db_destination.connect()

            data=[]
            [data.append(element) for element in self.__tableau]
            self.__db_destination.insertBulk(table=self.__table, cols=self.__cols,rows=data)

        except Exception as e:
            self.__logger.error(f"Échec de la connexion à la base de données.")
            raise