# overrides for the webapp deployment
DEBUG = False
PORT = 5018
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

# Service specific config
#########################

DEFAULT_VAT_PC = 20

DEFAULT_OVERHEAD_PC = 10

