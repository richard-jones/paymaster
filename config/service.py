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

QUERY_ROUTE = {
    "query" : {                                 # the URL route at which it is mounted
        "payment" : {                             # the URL name for the index type being queried
            "auth" : False,                     # whether the route requires authentication
            "role" : None,                      # if authenticated, what role is required to access the query endpoint
            "filters" : [],            # names of the standard filters to apply to the query
            "dao" : "service.dao.PaymentDAO"       # classpath for DAO which accesses the underlying ES index
        }
    }
}

CLIENTJS_PAYMENT_QUERY_ENDPOINT = "/query/payment"

CRUD = {
    "payment" : {
        "model" : "service.models.CRUDPayment",
        "create" : {
            "enable" : True
        },
        "retrieve" : {
            "enable" : True
        },
        "update" : {
            "enable" : True
        },
        "delete" : {
            "enable" : True
        }
    }
}

FRAGMENTS = {
    "payment_form" : {
        "function" : "service.payment.raw_form"
    }
}

# Service specific config
#########################

DEFAULT_VAT_PC = 20

DEFAULT_OVERHEAD_PC = 10
