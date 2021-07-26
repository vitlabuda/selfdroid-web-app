# SPDX-License-Identifier: BSD-3-Clause
#
# Copyright (c) 2021 Vít Labuda. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
# following conditions are met:
#  1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following
#     disclaimer.
#  2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
#     following disclaimer in the documentation and/or other materials provided with the distribution.
#  3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote
#     products derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


import flask
import flask_sqlalchemy
import flask_talisman
from selfdroid.Constants import Constants
from selfdroid.Settings import Settings
from selfdroid.Initializer import Initializer
from selfdroid.TemplateFilters import TemplateFilters


initializer = Initializer()
initializer.initialize_data_directory()


app = flask.Flask(__name__)
app.secret_key = initializer.get_secret_key()
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = Constants.DATABASE_URI
app.config["MAX_CONTENT_LENGTH"] = Settings.MAX_UPLOAD_SIZE
app.config["SESSION_COOKIE_SECURE"] = True
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = True


db = flask_sqlalchemy.SQLAlchemy(app)
from selfdroid.appstorage.AppMetadataDBModel import AppMetadataDBModel

db.create_all()
db.session.commit()


from selfdroid.api import api_blueprint
from selfdroid.web import web_blueprint
app.register_blueprint(api_blueprint)
app.register_blueprint(web_blueprint)


talisman = flask_talisman.Talisman(app, **Constants.TALISMAN_OPTIONS)


# It seems that template filters cannot be registered for a blueprint.
@app.template_filter("tf_format_datetime")
def fltf_global_format_datetime(value):
    return TemplateFilters.tf_format_datetime(value)


@app.template_filter("tf_android_api_level_to_version_string")
def fltf_global_android_api_level_to_version_string(value):
    return TemplateFilters.tf_android_api_level_to_version_string(value)


@app.template_filter("tf_human_readable_file_size")
def fltf_global_human_readable_file_size(value):
    return TemplateFilters.tf_human_readable_file_size(value)


@app.route("/robots.txt", methods=["GET"])
def fl_global_robots_txt():
    return flask.send_from_directory(app.static_folder, "robots.txt")


@app.route("/", methods=["GET"])
def fl_global_index():
    return flask.redirect(flask.url_for("web_blueprint.fl_web_login"))
