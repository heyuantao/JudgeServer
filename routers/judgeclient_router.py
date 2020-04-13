#-*- coding=utf-8 -*-
#该文件处理判题机的路由和视图函数的对应关系
from flask import render_template, request, session, jsonify
#from views.download_views import api_file_info_view, api_file_url_view, file_content_view
from config import config
from views.judgeclient_views import api_get_jobs_view,api_test_judgeclient

ROUTER_PREFIX = config.App.ROUTE_PREFIX

class Route:

    def init_app(self, app=None, auth=None):

        #Judge client post test
        @app.route(ROUTER_PREFIX + '/api/v1/judgeclient/test/', methods=['POST', ])
        def test_judgeclient():
            return api_test_judgeclient()

        # add a problem
        @app.route(ROUTER_PREFIX + '/api/v1/judgeclient/solution/', methods=['POST', ])
        @auth.login_required
        def get_jobs():
            return api_get_jobs_view()