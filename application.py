from flask import Flask, Response, request
from flask_cors import CORS

import json
import logging
from http import HTTPStatus
from application_services.recommender_resource import ArtRecommendationResource
from middleware.security.security import Security
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

application = app = Flask(__name__)
CORS(app)


@application.before_request
def verify_oauth_token():
    """
    Method to run before all requests; determines if a user has a valid
    Google OAuth2 token and uses the token to discover who the user making the request is.
    The google user and auth token loaded into special flask object called 'g'.
    While g is not appropriate for storing data across requests, it provides a global namespace
    for holding any data you want during a single request.
    """
    return Security.verify_token(request)


@app.route("/")
def health_check():
    return "Hello World"


@app.route("/api/sync_recommendations", methods=["GET"])
def get_recommendation_sync():
    limit = request.args.get("limit")
    limit = int(limit) if limit else 1

    recommendations = ArtRecommendationResource.get_synchronous_recommendation(limit)
    return Response(
        json.dumps(recommendations), status=HTTPStatus.OK, content_type="application/json"
    )


@app.route("/api/recommendations", methods=["GET"])
def get_recommendation_async():
    limit = request.args.get("limit")
    limit = int(limit) if limit else 1

    recommendation = ArtRecommendationResource.get_asynchronous_recommendation(limit)
    return Response(
        json.dumps(recommendation), status=HTTPStatus.OK, content_type="application/json"
    )


if __name__ == "__main__":
    application.run(host="0.0.0.0", port=9999)
