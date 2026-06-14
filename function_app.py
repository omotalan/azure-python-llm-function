import json
import logging

import azure.functions as func

from src.application import document_analysis_service
from src.domain.exceptions import ValidationException

logger = logging.getLogger(__name__)

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)


@app.route(route="analyze-document", methods=["POST"])
def analyze_document(req: func.HttpRequest) -> func.HttpResponse:
    logger.info("Received POST /analyze-document")

    try:
        payload = req.get_json()
    except ValueError:
        logger.warning("Request body is not valid JSON")
        return func.HttpResponse(
            json.dumps({"error": "Request body must be valid JSON"}),
            status_code=400,
            mimetype="application/json",
        )

    if not isinstance(payload, dict):
        logger.warning("Request payload is not a JSON object")
        return func.HttpResponse(
            json.dumps({"error": "Request body must be a JSON object"}),
            status_code=400,
            mimetype="application/json",
        )

    try:
        result = document_analysis_service.analyze(payload)
        return func.HttpResponse(
            json.dumps(result),
            status_code=200,
            mimetype="application/json",
        )
    except ValidationException as exc:
        logger.warning("Validation error: %s", str(exc))
        return func.HttpResponse(
            json.dumps({"error": str(exc)}),
            status_code=400,
            mimetype="application/json",
        )
    except Exception:
        logger.exception("Unhandled error during document analysis")
        return func.HttpResponse(
            json.dumps({"error": "Internal server error"}),
            status_code=500,
            mimetype="application/json",
        )

