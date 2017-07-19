from logic_core.base_core import base_core


class im_control_core(base_core):
    def init_command_dict(self):
        return {
            'control/init': self._processor_init,
            'control/shutdown': self._processor_shutdown
        }

    def _processor_init(self):
        print("Initializing Processor")

    def _processor_shutdown(self):
        print("Shutting Down Processor")
