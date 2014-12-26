# overrides for the webapp deployment
DEBUG = False
PORT = 5017
SSL = False
THREADED = True

# important overrides for the ES module

# elasticsearch back-end connection settings
ELASTIC_SEARCH_HOST = "http://localhost:9200"
ELASTIC_SEARCH_INDEX = "paymaster"

# Classes from which to retrieve ES mappings to be used in this application
ELASTIC_SEARCH_MAPPINGS = [
    "service.dao.PaymentDAO"
]

# overwrite example configurations
AUTOCOMPLETE_COMPOUND = None
AUTOCOMPLETE_TERM = None
QUERY_FILTERS = None
QUERY_ROUTE = None


