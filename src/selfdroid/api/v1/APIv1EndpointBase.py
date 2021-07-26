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


from typing import Union, List, Dict, Any
import abc
import flask
from selfdroid.EndpointBase import EndpointBase
from selfdroid.api.v1.APIv1Authenticator import APIv1Authenticator


class APIv1EndpointBase(EndpointBase, metaclass=abc.ABCMeta):
    JSONValue = Union[str, int, float, bool, None, List[Any], Dict[str, Any]]
    JSONType = Union[List[JSONValue], Dict[str, JSONValue]]

    def __init__(self, url_params: Dict[str, Any]):
        super().__init__(url_params)

        if not APIv1Authenticator().check_user_password_from_headers():
            flask.abort(401)

    def jsonify_and_finish_request(self, jsonifiable_object: JSONType) -> None:
        jsonified_object = flask.jsonify(jsonifiable_object)
        self.finish_request(jsonified_object)

    def send_file_and_finish_request(self, directory: str, filename: str, download_name: str, **send_file_kwargs) -> None:
        send_file_kwargs["download_name"] = download_name

        sent_file = flask.send_from_directory(directory, filename, **send_file_kwargs)
        self.finish_request(sent_file)
