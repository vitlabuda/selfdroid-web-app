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
from selfdroid.api.v1.endpoints.APIv1InfoEndpoint import APIv1InfoEndpoint
from selfdroid.api.v1.endpoints.APIv1AllAppDetailsEndpoint import APIv1AllAppDetailsEndpoint
from selfdroid.api.v1.endpoints.APIv1AppDetailsEndpoint import APIv1AppDetailsEndpoint
from selfdroid.api.v1.endpoints.APIv1AppIconEndpoint import APIv1AppIconEndpoint
from selfdroid.api.v1.endpoints.APIv1DownloadAPKEndpoint import APIv1DownloadAPKEndpoint


URL_PREFIX = "/v1"

api_v1_blueprint = flask.Blueprint("api_v1_blueprint", __name__, url_prefix=URL_PREFIX)


@api_v1_blueprint.route("/info", methods=["GET"])
def fl_api_v1_info(**url_params):
    return EndpointExecutor(APIv1InfoEndpoint, url_params).execute()


@api_v1_blueprint.route("/app-details", methods=["GET"])
def fl_api_v1_all_app_details(**url_params):
    return EndpointExecutor(APIv1AllAppDetailsEndpoint, url_params).execute()


@api_v1_blueprint.route("/app-details/<int:app_id>", methods=["GET"])
def fl_api_v1_app_details(**url_params):
    return EndpointExecutor(APIv1AppDetailsEndpoint, url_params).execute()


@api_v1_blueprint.route("/app-icon/<int:app_id>", methods=["GET"])
def fl_api_v1_app_icon(**url_params):
    return EndpointExecutor(APIv1AppIconEndpoint, url_params).execute()


@api_v1_blueprint.route("/download-apk/<int:app_id>", methods=["GET"])
def fl_api_v1_download_apk(**url_params):
    return EndpointExecutor(APIv1DownloadAPKEndpoint, url_params).execute()
