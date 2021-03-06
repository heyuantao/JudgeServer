#-*- coding=utf-8 -*-
from flask import Flask
from flask_cors import CORS
from werkzeug.serving import WSGIRequestHandler
from config import config
import logging

logger = logging.getLogger(__name__)


def create_app():
    app = Flask(__name__,static_folder=config.App.STATIC_FOLDER, template_folder=config.App.TEMPLATE_FOLDER)
    app.config.from_object(config)
    CORS(app)
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RR'

    from auth import Auth
    auth_instance = Auth()
    auth_instance.init_app(app)

    #init router
    from routers import JudgeClient_Router, WebClient_Router
    route_instance = JudgeClient_Router()
    route_instance.init_app(app,auth_instance.get_auth())
    route_instance = WebClient_Router()
    route_instance.init_app(app,auth_instance.get_auth())

    from db import Database
    redis_instance = Database()
    redis_instance.init_app(app)

    #redis_instance._put_problem_id_into_unsolved_queue('1000')
    #redis_instance._put_problem_id_into_unsolved_queue('1001')
    #for i in range(5):
    #    output = redis_instance.get_problem()
    #    print(output)
    '''
    from storage import Storage
    storage_instance = Storage()
    storage_instance.init_app(app)


    #从gunicorn获得loglevel等级，并将其设置到app中
    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
'''
    #if logger.getEffectiveLevel()==logging.DEBUG:
    #    logger.critical("The app is in debug mode, the merge process will execute slowly !")

    return app

WSGIRequestHandler.protocol_version = "HTTP/1.1"
application = create_app()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    application.run(port=5001, host="0.0.0.0", debug=True)


