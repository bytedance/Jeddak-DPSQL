# Copyright (2023) Beijing Volcano Engine Technology Ltd.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import logging
import logging.config
import flask
from pyinstrument import Profiler
from http_service.timer_task import start_scheduler, init_scheduler
from http_service.utils.init_global_object import init_global_obj
from http_service.api.v1.metadata.metadata_views import meta
from http_service.api.v1.query.routes import app as app_v1_query
from http_service.api.v1.budget.views import budget

logging.config.fileConfig("logging.conf")

try:
    init_global_obj()
except Exception as err:
    logging.exception("dpaccess-internal-init global obj Exception: \n" + str(err))


app = flask.Flask(__name__)
app.register_blueprint(app_v1_query, url_prefix='/api/v1/query')
app.register_blueprint(meta, url_prefix='/api/v1/metadata')
app.register_blueprint(budget, url_prefix='/api/v1/budget')
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024


# profile
@app.before_request
def before_request():
    if "profile" in flask.request.args:
        flask.g.profiler = Profiler()
        flask.g.profiler.start()


@app.after_request
def after_request(response):
    if not hasattr(flask.g, "profiler"):
        return response
    flask.g.profiler.stop()
    output_html = flask.g.profiler.output_html()
    return flask.make_response(output_html)


init_scheduler(app)
start_scheduler()
