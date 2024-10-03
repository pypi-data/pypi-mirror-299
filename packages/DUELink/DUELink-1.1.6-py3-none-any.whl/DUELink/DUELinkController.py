from DUELink.Analog import AnalogController
from DUELink.Button import ButtonController
from DUELink.Digital import DigitalController
from DUELink.Display import DisplayController
from DUELink.Display import DisplayConfiguration
from DUELink.DisplayType import DisplayTypeController
from DUELink.DistanceSensor import DistanceSensorController
from DUELink.Frequency import FrequencyController
from DUELink.I2C import I2cController
from DUELink.Infrared import InfraredController
from DUELink.Neo import NeoController
from DUELink.System import SystemController
from DUELink.SerialInterface import SerialInterface
from DUELink.Servo import ServoController
from DUELink.Spi import SpiController
from DUELink.Touch import TouchController
from DUELink.Uart import UartController
from DUELink.Led import LedController
from DUELink.Script import ScriptController
from DUELink.DeviceConfiguration import DeviceConfiguration
from DUELink.Pin import PinController
from DUELink.Temperature import TemperatureController
from DUELink.Humidity import HudimityController
from DUELink.Pulse import PulseController
from DUELink.Can import CanController
from DUELink.Sound import SoundController
from DUELink.Temperature import TemperatureSensorType
from DUELink.Humidity import HumiditySensorType
from DUELink.Bluetooth import BluetoothController
from enum import Enum
import platform
class DUELinkController:

    def __init__(self, comPort: str):
        self.IsPulse = False
        self.IsFlea = False
        self.IsPico = False
        self.IsEdge = False
        self.IsRave = False
        self.IsTick = False
        self.IsDue = False

        if comPort is None:
            raise ValueError(f"Invalid comport: {comPort}")
        try:
            self.__Connect(comPort)
        except:
            raise Exception(f"Could not connect to the comport: {comPort}")
        
        if self.serialPort is None:
            raise Exception(f"serialPort is null")

        self.Analog = AnalogController(self.serialPort)
        self.Digital = DigitalController(self.serialPort)
        self.I2c = I2cController(self.serialPort)
        self.Servo = ServoController(self.serialPort)
        self.Frequency = FrequencyController(self.serialPort)
        self.Spi = SpiController(self.serialPort)
        self.Infrared = InfraredController(self.serialPort)
        self.Neo = NeoController(self.serialPort)
        self.Uart = UartController(self.serialPort)
        self.Button = ButtonController(self.serialPort)
        self.Distance = DistanceSensorController(self.serialPort)        
        self.Display = DisplayController(self.serialPort)
        self.Touch = TouchController(self.serialPort)
        self.Led = LedController(self.serialPort)
        self.Script = ScriptController(self.serialPort)
        self.Pin = PinController()
        self.Temperature = TemperatureController(self.serialPort)
        self.Humidity = HudimityController(self.serialPort)
        self.System = SystemController(self.serialPort)        
        self.DisplayType = DisplayTypeController()        
  
        self.Pulse = PulseController(self.serialPort)
        self.Can = CanController(self.serialPort)
        self.Sound = SoundController(self.serialPort)
        self.Bluetooth = BluetoothController(self.serialPort)

        self.TemperatureSensorType = TemperatureSensorType()
        self.HumiditySensorType = HumiditySensorType()
        
        self.System.Version = self.Version

        
    
    def __Connect(self, comPort: str):
        self.serialPort = SerialInterface(comPort)
        self.serialPort.Connect()

        self.Version = self.serialPort.GetVersion().split("\n")[0]

        if self.Version == "" or len(self.Version) != 7:
            raise Exception("The device is not supported.")
        
        self.DeviceConfig = DeviceConfiguration()

        if self.Version[len(self.Version) -1] == 'P':
            self.DeviceConfig.IsPulse = True
            self.DeviceConfig.MaxPinIO = 23
            self.DeviceConfig.MaxPinAnalog = 29
        elif self.Version[len(self.Version) -1] == 'I':
            self.DeviceConfig.IsPico = True
            self.DeviceConfig.MaxPinIO = 29
            self.DeviceConfig.MaxPinAnalog = 29  
        elif self.Version[len(self.Version) -1] == 'F':
            self.DeviceConfig.IsFlea = True
            self.DeviceConfig.MaxPinIO = 11
            self.DeviceConfig.MaxPinAnalog = 29    
        elif self.Version[len(self.Version) -1] == 'E':
            self.DeviceConfig.IsEdge = True
            self.DeviceConfig.MaxPinIO = 22
            self.DeviceConfig.MaxPinAnalog = 11  
        elif self.Version[len(self.Version) -1] == 'R':
            self.DeviceConfig.IsRave = True
            self.DeviceConfig.MaxPinIO = 23
            self.DeviceConfig.MaxPinAnalog = 29
        elif self.Version[len(self.Version) -1] == 'T':
            self.DeviceConfig.IsTick = True
            self.DeviceConfig.MaxPinIO = 23
            self.DeviceConfig.MaxPinAnalog = 11
        elif self.Version[len(self.Version) -1] == 'D':
            self.DeviceConfig.IsDue = True
            self.DeviceConfig.MaxPinIO = 15
            self.DeviceConfig.MaxPinAnalog = 10

        self.serialPort.DeviceConfig = self.DeviceConfig

        self.IsPulse = self.DeviceConfig.IsPulse
        self.IsFlea = self.DeviceConfig.IsFlea
        self.IsPico = self.DeviceConfig.IsPico
        self.IsEdge = self.DeviceConfig.IsEdge
        self.IsRave = self.DeviceConfig.IsRave
        self.IsTick = self.DeviceConfig.IsTick
        self.IsDue = self.DeviceConfig.IsDue

    def Disconnect(self):
        self.serialPort.Disconnect()

    def GetConnectionPort():
        try:
            from serial.tools.list_ports import comports
        except ImportError:
            return ""
        
        if comports:
            com_ports_list = list(comports())
            ebb_ports_list = []
            for port in com_ports_list:               
                if port.vid ==0x1B9F and port.pid==0xF300:
                    if (platform.system() == 'Windows'):
                        return port.name                    
                    else:
                        return port.device

        return ""
   
         

        
        


