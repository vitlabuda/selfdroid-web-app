from selfdroid.api.v1.APIv1EndpointBase import APIv1EndpointBase
from selfdroid.appstorage.AppStorageHelpers import AppStorageHelpers
from selfdroid.appstorage.crud.AppGetter import AppGetter


class APIv1AllAppDetailsEndpoint(APIv1EndpointBase):
    def handle_request(self) -> None:
        with AppStorageHelpers.get_app_storage_lock():
            all_apps_metadata = AppGetter().get_all_metadata_while_locked()

        json_object = [app_metadata.to_api_dict() for app_metadata in all_apps_metadata]
        self.jsonify_and_finish_request(json_object)
