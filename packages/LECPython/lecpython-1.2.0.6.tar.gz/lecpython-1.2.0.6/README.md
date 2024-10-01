# LECPython

LECPython is a Python component developed in C# that enables seamless communication between Python and PLCs. It requires .NET 8 runtime support,When LECPython is called for the first time, the component automatically checks if .NET 8 is installed, and if not, it will perform an automatic online installation. 

LECPython supports a wide range of PLCs available in the market, including those supporting the Modbus protocol, Mitsubishi, Siemens, Omron, Rockwell, Keyence PLC, Delta, Beckhoff, Panasonic, Inovance, Fuji, EverSensing, Schneider, and more. This component is standalone, requiring no additional third-party PLC controls for support.

## Installation

Ensure you have Python installed. You can install LECPython using pip:

```bash
pip install LECPython
```

LECPython automatically installs the required `pythonnet` dependency. However, if needed, you can manually install it using:

```bash
pip install pythonnet==3.0.4
```

## Usage

Here's a basic example of how to use LECPython:

```python
from LECPython import LECPython

if __name__ == "__main__":
    lecp = LECPython()
    try:
        # Establish connection to Omron FINS PLC
        result = lecp.OmronFinsNetConnection("192.168.31.64", 9600, 13, 0, "CDAB", True, 2000)
        print("ModbusTcpNetConnection called successfully:", result["ErrorCode"])
        
        # Read 10 float values from address D100
        rtval = lecp.ReadNodeValues(result["Content"], "D100", "float", 10)
        print(f"The rtval is: {rtval}")
        
        # Write a float value to address D100
        rtval = lecp.WriteNodeValues(result["Content"], "D100", "float", [88.123, 726.1223])
        print(f"The rtval is: {rtval}")
        
        # Read 10 float values from address D100 again
        rtval = lecp.ReadNodeValues(result["Content"], "D100", "float", 10)
        print(f"The rtval is: {rtval}")
    except AttributeError as e:
        print(e)
```

## Features

- Supports multiple PLC protocols including Modbus, Mitsubishi, Siemens, Omron, Rockwell and more.
- Easy to use API for connecting and communicating with PLCs.
- Standalone component with no need for additional third-party PLC controls.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
