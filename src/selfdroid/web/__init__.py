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
from selfdroid.EndpointExecutor import EndpointExecutor
from selfdroid.web.WebHelpers import WebHelpers
from selfdroid.web.endpoints.WebLoginEndpoint import WebLoginEndpoint
from selfdroid.web.endpoints.WebLogoutEndpoint import WebLogoutEndpoint
from selfdroid.web.endpoints.WebIndexEndpoint import WebIndexEndpoint
from selfdroid.web.endpoints.WebAppDetailsEndpoint import WebAppDetailsEndpoint
from selfdroid.web.endpoints.WebAppIconEndpoint import WebAppIconEndpoint
from selfdroid.web.endpoints.WebDownloadAPKEndpoint import WebDownloadAPKEndpoint
from selfdroid.web.endpoints.WebAddAppEndpoint import WebAddAppEndpoint
from selfdroid.web.endpoints.WebUpdateAppEndpoint import WebUpdateAppEndpoint
from selfdroid.web.endpoints.WebDeleteAppEndpoint import WebDeleteAppEndpoint


URL_PREFIX = "/web"

web_blueprint = flask.Blueprint("web_blueprint", __name__, template_folder="templates", url_prefix=URL_PREFIX)


@web_blueprint.context_processor
def flcp_web():
    return WebHelpers.generate_web_template_context()


@web_blueprint.route("/login", methods=["GET", "POST"])
def fl_web_login(**url_params):
    return EndpointExecutor(WebLoginEndpoint, url_params).execute()


@web_blueprint.route("/logout", methods=["POST"])
def fl_web_logout(**url_params):
    return EndpointExecutor(WebLogoutEndpoint, url_params).execute()


@web_blueprint.route("/", methods=["GET"])
def fl_web_index(**url_params):
    return EndpointExecutor(WebIndexEndpoint, url_params).execute()


@web_blueprint.route("/app-details/<int:app_id>", methods=["GET"])
def fl_web_app_details(**url_params):
    return EndpointExecutor(WebAppDetailsEndpoint, url_params).execute()


@web_blueprint.route("/app-icon/<int:app_id>", methods=["GET"])
def fl_web_app_icon(**url_params):
    return EndpointExecutor(WebAppIconEndpoint, url_params).execute()


@web_blueprint.route("/download-apk/<int:app_id>", methods=["GET"])
def fl_web_download_apk(**url_params):
    return EndpointExecutor(WebDownloadAPKEndpoint, url_params).execute()


@web_blueprint.route("/add-app", methods=["POST"])
def fl_web_add_app(**url_params):
    return EndpointExecutor(WebAddAppEndpoint, url_params).execute()


@web_blueprint.route("/update-app/<int:app_id>", methods=["POST"])
def fl_web_update_app(**url_params):
    return EndpointExecutor(WebUpdateAppEndpoint, url_params).execute()


@web_blueprint.route("/delete-app/<int:app_id>", methods=["POST"])
def fl_web_delete_app(**url_params):
    return EndpointExecutor(WebDeleteAppEndpoint, url_params).execute()
