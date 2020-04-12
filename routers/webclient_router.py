#-*- coding=utf-8 -*-
#该文件处理第三方客户端的路由和视图函数的对应关系
from flask import render_template, request, session, jsonify
#from views.download_views import api_file_info_view, api_file_url_view, file_content_view
from config import config
#from views.judgeclient_views import api_version_info_view
from views.webeclient_views import api_version_info_view, api_solution_create_view, api_solution_info_view

ROUTER_PREFIX = config.App.ROUTE_PREFIX

class Route:

    def init_app(self, app=None, auth=None):
        @app.route(ROUTER_PREFIX + '/version', methods=['GET', ])
        def version_info():
            return api_version_info_view()


        #add a problem
        @app.route(ROUTER_PREFIX + '/api/v1/webclient/solution/', methods=['POST', ])
        @auth.login_required
        def solution_create():
            return api_solution_create_view()

        #retrive solution judged info
        @app.route(ROUTER_PREFIX + '/api/v1/webclient/solution/info', methods=['POST', ])
        @auth.login_required
        def solution_info():
            return api_solution_info_view()