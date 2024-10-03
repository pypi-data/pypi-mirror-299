from ab_py.http.ab_rest_processor import ABRestProcessor
from ab_py.exsited.setting.setting_api_url import SettingApiUrl


class Setting(ABRestProcessor):
    def get_settings(self):
        response = self.get(url=SettingApiUrl.SETTINGS)
        return response
