from logic_core.base_core import base_core


class im_debug_core(base_core):
    def init_command_dict(self):
        return {
            "debug/get_basic_data_size": self._get_basic_data_size()
        }

    def _get_basic_data_size(self):
        return str(len(self.processor.basic_data))

