#-*- coding=utf-8 -*-
#该文件处理判题机的路由和视图函数的对应关系
from flask import render_template, request, session, jsonify
#from views.download_views import api_file_info_view, api_file_url_view, file_content_view
from config import config
from views.judgeclient_views import api_get_jobs_view

ROUTER_PREFIX = config.App.ROUTE_PREFIX

class Route:

    def init_app(self, app=None, auth=None):

        # add a problem
        @app.route(ROUTER_PREFIX + '/api/v1/judgeclient/solution/', methods=['POST', ])
        @auth.login_required
        def get_jobs():
            return api_get_jobs_view()