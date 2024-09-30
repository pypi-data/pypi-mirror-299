from pythonnet import load
load("coreclr")

import clr
import os

# Load the C# DLL
dll_path = os.path.join(os.path.dirname(__file__), "LECPythonLib.dll")  # Updated path
clr.AddReference(dll_path)

# Import namespaces from the DLL
from LECPythonLib import DeviceProfinetConnection
from LECPythonLib import DeviceProfinetCommunication


class LECPython:
    def __init__(self):
        # Create an instance of DeviceProfinetConnection
        self.connection = DeviceProfinetConnection()

    def __getattr__(self, method_name):
        # Dynamically handle method calls
        def method(*args, **kwargs):
            # Attempt to retrieve the corresponding method
            if hasattr(self.connection, method_name):
                result = getattr(self.connection, method_name)(*args, **kwargs)
                result_json = {
                    "ErrorCode": result.ErrorCode,
                    "IsSuccess": result.IsSuccess,
                    "Message": result.Message,
                    "Content": result.Content
                }
                return result_json
            else:
                raise AttributeError(f"'{DeviceProfinetConnection.__name__}' object has no method '{method_name}'")
        return method
    
    @staticmethod
    def ReadNodeValues(plc, address, data_type, length):
        # Read node values from the PLC
        result = DeviceProfinetCommunication.ReadNodeValues(plc, address, data_type, length)
        print(result.Content[0])
        content_array = result.Content if isinstance(result.Content, list) else list(result.Content)
        return {
            "ErrorCode": result.ErrorCode,
            "IsSuccess": result.IsSuccess,
            "Message": result.Message,
            "Content": content_array
        }

    @staticmethod
    def WriteNodeValues(plc, address, data_type, value):
        # Write node values to the PLC
        success = DeviceProfinetCommunication.WriteNodeValues(plc, address, data_type, value)
        return {"IsSuccess": success}
    
    @staticmethod
    def Test():
        # Perform a test operation
        success = DeviceProfinetConnection.Test()
        return {"IsSuccess": success}