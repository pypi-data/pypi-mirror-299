from enum import Enum

class ButtonController:   

    def __init__(self, serialPort):
        self.serialPort = serialPort

    def IsButtonValid(self, pin) ->bool:
        if (pin != 0 and pin != 1 and pin != 2 and pin != 3 and pin != 4 and pin != 13 and pin != 14 and pin != 15 and pin != 16 and pin != 65 and pin != 66 and pin != 68 and pin != 76 and pin != 82 and pin != 85):
            return False
        return True
        
    def Enable(self, pin, enable: bool) -> bool:
        pin = (ord(pin) if isinstance(pin, str) else pin) & 0xdf
        if self.IsButtonValid(pin) == False:
            raise ValueError("Invalid pin")
    
        cmd = f"btnenable({pin}, {int(enable)})"

        self.serialPort.WriteCommand(cmd)
        res = self.serialPort.ReadRespone()

        return res.success
    
    def JustPressed(self, pin) -> bool:
        pin = (ord(pin) if isinstance(pin, str) else pin) & 0xdf
        if self.IsButtonValid(pin) == False:
            raise ValueError("Invalid pin")
            
        cmd = f"log(btndown({pin}))"

        self.serialPort.WriteCommand(cmd)
        res = self.serialPort.ReadRespone()

        if res.success:
            try:
                return int(res.respone) == 1
            except:
                pass

        return False
    
    def JustReleased(self, pin) -> bool:
        pin = (ord(pin) if isinstance(pin, str) else pin) & 0xdf
        if self.IsButtonValid(pin) == False:
            raise ValueError("Invalid pin")
            
        cmd = f"log(btnup({pin}))"

        self.serialPort.WriteCommand(cmd)
        res = self.serialPort.ReadRespone()

        if res.success:
            try:
                return int(res.respone) == 1
            except:
                pass

        return False   
       
