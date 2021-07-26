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


from typing import List, Optional
from selfdroid.appstorage.AppMetadata import AppMetadata
from selfdroid.appstorage.AppMetadataDBModel import AppMetadataDBModel


class AppGetter:
    def get_all_db_models_while_locked(self) -> List[AppMetadataDBModel]:
        return AppMetadataDBModel.query.order_by(AppMetadataDBModel.app_name).all()

    def get_all_metadata_while_locked(self) -> List[AppMetadata]:
        return [self._convert_db_model_to_metadata(db_model) for db_model in self.get_all_db_models_while_locked()]

    def get_db_model_while_locked(self, app_id: int) -> Optional[AppMetadataDBModel]:
        return AppMetadataDBModel.query.get(app_id)

    def get_metadata_while_locked(self, app_id: int) -> Optional[AppMetadata]:
        return self._convert_db_model_to_metadata(self.get_db_model_while_locked(app_id))

    def get_db_model_or_404_while_locked(self, app_id: int) -> AppMetadataDBModel:
        return AppMetadataDBModel.query.get_or_404(app_id)

    def get_metadata_or_404_while_locked(self, app_id: int) -> AppMetadata:
        return self._convert_db_model_to_metadata(self.get_db_model_or_404_while_locked(app_id))

    def does_app_exist_in_database(self, app_id: int) -> bool:
        return self.get_db_model_while_locked(app_id) is not None

    def _convert_db_model_to_metadata(self, db_model: AppMetadataDBModel) -> AppMetadata:
        return AppMetadata.from_db_model(db_model)
