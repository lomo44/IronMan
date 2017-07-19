from enum import Enum

class eEvent_Loop_Status(Enum):
    eEvent_Loop_Continue = 0
    eEvent_Loop_Exit = 1

class eCommand_Process_Status(Enum):
    eCommand_Process_Status_Processed = 0
    eCommand_Process_Status_Passed = 1
