"""
This File contains the main method to start this service. 
"""

import logging
import os
import json

from flasgger import Swagger
from flask import Flask
from flask.wrappers import Response

from src.multi_task_agent.assistant import AssistantHandler

config_path: str = os.path.join(os.getcwd(), "config", "config.json")
with open(config_path, "r") as file:
    config: dict = json.load(file)
config["absolute_data_path"] = os.path.join(os.getcwd(), config["data_path"])

logging.basicConfig(
    level=config["log_level"],
    format="%(filename)s:%(lineno)d %(asctime)s %(levelname)s:%(message)s",
)


def health():
    try:
        return Response(
            response=json.dumps(
                {"name": config["name"], "status": "ok"}
            ),
            status=200,
            mimetype="application/json",
        )
    except Exception as e:
        logging.error(e)
        return Response(response="Health status could not be sent.", status=500)


def startup_flask_app():
    """Prepares all prerequisites for the server to work properly."""
    logging.info("Starting flask app")
    flask = Flask(__name__)
    flask.add_url_rule(rule="/health", view_func=health, methods=["GET"])
    return flask


app = startup_flask_app()

app.config["SWAGGER"] = {
    "title": config["display_name"],
}
swagger = Swagger(app)


if __name__ == "__main__":

    assistant_handler = AssistantHandler(config)
    assistant_handler.setup_assistants_parallel()

    reactor_args = {}

    def run_twisted_wsgi():
        from twisted.internet import reactor
        from twisted.web.server import Site
        from twisted.web.wsgi import WSGIResource
        from twisted.python import log

        log.PythonLoggingObserver().start()

        resource = WSGIResource(reactor, reactor.getThreadPool(), app)
        site = Site(resource)
        reactor.listenTCP(80, site)
        reactor.run(**reactor_args)

    if app.debug:
        reactor_args["installSignalHandlers"] = 0
        import werkzeug.serving

        run_twisted_wsgi = werkzeug.serving.run_with_reloader(run_twisted_wsgi)

    run_twisted_wsgi()
