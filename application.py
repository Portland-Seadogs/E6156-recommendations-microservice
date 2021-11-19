from flask import Flask, Response, request
from flask_cors import CORS

import json
import logging
from http import HTTPStatus
from application_services.recommender_resource import ArtRecommendationResource

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

application = app = Flask(__name__)
CORS(app)


@app.route("/")
def health_check():
    return "Hello World"


@app.route("/api/synchronous_recommendations", methods=["GET"])
def get_recommendation_async():
    limit = request.args.get("limit")
    limit = limit if limit else 1

    recommendation = ArtRecommendationResource.get_synchronous_recommendation(limit)
    return Response(
        json.dumps(recommendation), status=HTTPStatus.OK, content_type="application/json"
    )


@app.route("/api/recommendations", methods=["GET"])
def get_recommendation_async():
    limit = request.args.get("limit")
    limit = limit if limit else 1

    recommendation = ArtRecommendationResource.get_recommendation(limit)
    return Response(
        json.dumps(recommendation), status=HTTPStatus.OK, content_type="application/json"
    )


if __name__ == "__main__":
    application.run(host="0.0.0.0", port=7000)
