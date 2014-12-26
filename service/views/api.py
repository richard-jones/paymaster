from flask import Blueprint, make_response, url_for, request, abort
import json
from service import models
from octopus.lib.dataobj import ObjectSchemaValidationError

blueprint = Blueprint('api', __name__)

def _not_found():
    resp = make_response(json.dumps({"status" : "not found"}))
    resp.mimetype = "application/json"
    resp.status_code = 404
    return resp

def _bad_request(e):
    resp = make_response(json.dumps({"status" : "error", "error" : e.message}))
    resp.mimetype = "application/json"
    resp.status_code = 400
    return resp

def _created(p):
    url = url_for("api.payment", payment_id=p.id)
    resp = make_response(json.dumps({"status" : "success", "id" : p.id, "location" : url }))
    resp.mimetype = "application/json"
    resp.headers["Location"] = url
    resp.status_code = 201
    return resp

def _success():
    resp = make_response(json.dumps({"status" : "success"}))
    return resp

@blueprint.route("/payment", methods=["POST"])
def payments():
    # if this is the creation of a new object
    if request.method == "POST":
        # get the data and clean out any fields that aren't allowed
        data = json.loads(request.data)

        if "id" in data:
            del data["id"]
        if "created_date" in data:
            del data["created_date"]
        if "last_updated" in data:
            del data["last_updated"]

        # make and save a new object
        try:
            p = models.Payment(data)
        except ObjectSchemaValidationError as e:
            return _bad_request(e)
        p.save()

        # return a useful response object
        return _created(p)

@blueprint.route("/payment/<payment_id>", methods=["GET", "PUT", "DELETE"])
def payment(payment_id):
    if request.method == "GET":
        # get the existing paymemt, json it, and return it
        p = models.Payment.pull(payment_id)
        if p is None:
            return _not_found()
        resp = make_response(p.json())
        resp.mimetype = "application/json"
        return resp

    elif request.method == "PUT":
        # get the existing payment
        p = models.Payment.pull(payment_id)
        if p is None:
            return _not_found()

        # ge the data and clean out any fields that aren't allowed
        data = json.loads(request.data)
        if "id" in data:
            del data["id"]
        if "created_date" in data:
            del data["created_date"]
        if "last_updated" in data:
            del data["last_updated"]

        # carry over the data from the old object
        data["id"] = p.id
        data["created_date"] = p.created_date

        try:
            np = models.Payment(data)
        except ObjectSchemaValidationError as e:
            return _bad_request(e)
        np.save()

        # return a useful response object
        return _success()

    elif request.method == "DELETE":
        p = models.Payment.pull(payment_id)
        if p is None:
            return _not_found()
        p.delete()

        # return a useful response object
        return _success()