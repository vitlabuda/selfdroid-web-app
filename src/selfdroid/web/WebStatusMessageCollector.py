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


from typing import List, Tuple
import flask
import flask_wtf
from selfdroid.Constants import Constants
from selfdroid.UserReadableException import UserReadableException


class WebStatusMessageCollector:
    _FORM_ERROR_MESSAGE_PATTERN: str = "An error occurred while validating the <b>{field_name}</b> field of the <b>{form_name}</b> form: <b>{error_message}</b>"

    def __init__(self):
        self._forms: List[Tuple[str, flask_wtf.FlaskForm]] = []  # tuple: form name, form
        self._messages: List[Tuple[str, str]] = []  # tuple: category, message

    def register_form(self, form_name: str, form: flask_wtf.FlaskForm) -> None:
        self._forms.append((form_name, form))

    def add_success_message(self, message: str) -> None:
        self._add_message(Constants.FLASH_CATEGORY_SUCCESS, message)

    def add_error_message(self, message: str) -> None:
        self._add_message(Constants.FLASH_CATEGORY_ERROR, message)

    def _add_form_error_message(self, message: str) -> None:
        self._add_message(Constants.FLASH_CATEGORY_FORM_ERROR, message)

    def add_error_message_from_user_readable_exception(self, exception: UserReadableException) -> None:
        self.add_error_message(exception.user_readable_message)

    def _add_message(self, category: str, message: str) -> None:
        self._messages.append((category, message))

    def flash_all_messages_using_flask(self) -> None:
        """
        Should be used when redirecting.
        """

        self._extract_errors_from_forms()

        for category, message in self._messages:
            flask.flash(message, category)

    def get_all_messages_including_flask_flashed_messages(self) -> List[Tuple[str, str]]:
        """
        Should be used when rendering a template.
        """

        self._extract_errors_from_forms()

        flask_flashed_messages = flask.get_flashed_messages(with_categories=True)
        return self._messages + flask_flashed_messages

    def _extract_errors_from_forms(self) -> None:
        for form_name, form in self._forms:
            for field, errors in form.errors.items():
                for error in errors:
                    message = WebStatusMessageCollector.format_html_message(WebStatusMessageCollector._FORM_ERROR_MESSAGE_PATTERN,
                                                                            field_name=field,
                                                                            form_name=form_name,
                                                                            error_message=error)
                    self._add_form_error_message(message)

    @staticmethod
    def format_html_message(formatted_string: str, *format_args, **format_kwargs) -> str:
        # The format arguments are escaped to prevent XSS attacks
        safe_format_args = [str(flask.escape(arg)) for arg in format_args]
        safe_format_kwargs = {k:str(flask.escape(v)) for k, v in format_kwargs.items()}

        formatted_message = formatted_string.format(*safe_format_args, **safe_format_kwargs)

        return flask.Markup(formatted_message)
