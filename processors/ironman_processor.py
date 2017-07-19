from processors.basic_processor import basic_processor
from event_loop_status import eEvent_Loop_Status
from enum import Enum
from marvel_wikia_module import get_marvel_basic_info, marvel_hero_name
import json

regex_Get = r"[g|G][e|E][t|T] (.*)"


class eIM_Data_Loading_Type(Enum):
    eIM_Data_Loading_Default = 0
    eIM_Data_Loading_Local = 1
    eIM_Data_Loading_Online = 2




class ironman_processor(basic_processor):
    def load_data(self, data_loading_type: eIM_Data_Loading_Type):
        def load_data_online():
            return get_marvel_basic_info(marvel_hero_name.eMarvel_Hero_Iron_Man)

        def load_data_local():
            file = open("data/Iron_Man.json", "r")
            if file is not None:
                return json.load(file)
            return None

        if data_loading_type is eIM_Data_Loading_Type.eIM_Data_Loading_Default:
            data = load_data_online()
            if data is None:
                data = load_data_local()
            return data
        elif data_loading_type is eIM_Data_Loading_Type.eIM_Data_Loading_Local:
            return load_data_local()
        elif data_loading_type is eIM_Data_Loading_Type.eIM_Data_Loading_Online:
            return load_data_online()
        else:
            return None

    def process(self, input):
        return NotImplemented
