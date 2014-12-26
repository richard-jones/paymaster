from octopus.modules.es import testindex

from copy import deepcopy
import json, requests

TEST_URL = "http://localhost:5017/api/payment"

RECORD = {
    "id" : "12345",

    "ref" : "INV-001",
    "description" : "An invoice to be paid",
    "invoice_date" : "2014-01-01T00:00:00",
    "expected_amount" : 1000.50,
    "actual_amount" : 999.50,
    "vat_pc" : 20,
    "vat" : 832.92,
    "overhead_pc" : 10,
    "overhead" : 749.63,
    "available" : 352.13,
    "notes" : "Lots of money for you",
    "state" : "paid_to_cl",

    "expenses" : [
        {
            "ref" : "Contractor expenses for CC",
            "amount" : 100
        },
        {
            "ref" : "Travel",
            "amount" : 80,
            "allocate_to" : "AA"
        }
    ],
    "shares" : [
        {
            "who" : "AA",
            "pc" : 40,
            "share_amount" : 140.85,
            "expenses" : 80,
            "total" : 220.85
        },
        {
            "who" : "DD",
            "pc" : 60,
            "share_amount" : 211.28,
            "expenses" : 0,
            "total" : 211.28
        }
    ],
    "central" : [
        {
            "ref" : "staff",
            "description" : "Costs for BB",
            "amount" : 150
        },
        {
            "ref" : "sysadmin",
            "description" : "Costs for server",
            "amount" : 67.50
        }
    ]
}

class TestImport(testindex.ESTestCase):
    def setUp(self):
        super(TestImport, self).setUp()

    def tearDown(self):
        super(TestImport, self).tearDown()

    def test_01_create_success(self):
        r = deepcopy(RECORD)
        data = json.dumps(r)
        resp = requests.post(TEST_URL, data=data)

        assert resp.status_code == 201
        j = resp.json()
        assert j.get("status") == "success"
        assert j.get("id") is not None
        assert j.get("location") is not None
        assert resp.headers["location"].endswith(j.get("location"))

    def test_02_create_retrieve_success(self):
        r = deepcopy(RECORD)
        data = json.dumps(r)
        resp = requests.post(TEST_URL, data=data)

        loc = resp.headers["location"]
        resp = requests.get(loc)

        assert resp.status_code == 200
        j = resp.json()
        assert j.get("ref") == "INV-001"

    def test_03_create_update_retrieve(self):
        # create the initial record
        r = deepcopy(RECORD)
        data = json.dumps(r)
        resp = requests.post(TEST_URL, data=data)

        # get the location to use for further requests
        loc = resp.headers["location"]

        # retrieve the record and check the ref
        resp = requests.get(loc)
        j = resp.json()
        assert j.get("ref") == "INV-001"

        # create an updated record using the loc, with a different ref
        r2 = deepcopy(RECORD)
        r2["ref"] = "INV-003"
        resp = requests.put(loc, data=json.dumps(r2))

        # check the response data
        assert resp.status_code == 200
        j = resp.json()
        assert j.get("status") == "success"

        # retrieve the record again
        resp = requests.get(loc)
        j = resp.json()
        assert j.get("ref") == "INV-003"

    def test_04_create_retrieve_delete(self):
        # create the initial record
        r = deepcopy(RECORD)
        data = json.dumps(r)
        resp = requests.post(TEST_URL, data=data)

        # get the location to use for further requests
        loc = resp.headers["location"]

        # retrieve the record and check the ref
        resp = requests.get(loc)
        j = resp.json()
        assert j.get("ref") == "INV-001"

        # now issue a delete request on the record
        resp = requests.delete(loc)

        # check the delete response
        assert resp.status_code == 200
        j = resp.json()
        assert j.get("status") == "success"

        # check that we can't now retrieve the item
        resp = requests.get(loc)
        assert resp.status_code == 404
        j = resp.json()
        assert j.get("status") == "not found"


