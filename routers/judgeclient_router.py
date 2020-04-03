#-*- coding=utf-8 -*-
from flask import render_template, request, session, jsonify
#from views.download_views import api_file_info_view, api_file_url_view, file_content_view
from config import config
from views.judgeclient_views import api_software_info_view

ROUTER_PREFIX = config.App.ROUTE_PREFIX

class Route:

    def init_app(self, app=None, auth=None):
        @app.route(ROUTER_PREFIX + '/software', methods=['GET', ])
        def software_info():
            return api_software_info_view()