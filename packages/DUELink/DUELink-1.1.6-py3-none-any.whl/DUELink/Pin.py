import time

class PinController:   
     
    def __init__(self):
        pass


    def __get_button_a(self):
        return 97

    def __get_button_b(self):
        return 98
    
    def __get_button_up(self):
        return 85
    
    def __get_button_down(self):
        return 68
    
    def __get_button_left(self):
        return 76
    
    def __get_button_right(self):
        return 82
    
    def __get_led(self):
        return 108

    def __get_piezo(self):
        return 112
    
    def __get_pullnone(self):
        return 0
    
    def __get_pullup(self):
        return 1
    
    def __get_pulldown(self):
        return 2

    def __set_empty(self, value: int):
        return    
    
    ButtonA = property(__get_button_a, __set_empty)  
    ButtonB = property(__get_button_b, __set_empty)   
    ButtonUp = property(__get_button_up, __set_empty)  
    ButtonDown = property(__get_button_down, __set_empty)   
    ButtonLeft = property(__get_button_left, __set_empty)  
    ButtonRight = property(__get_button_right, __set_empty)   
    Led = property(__get_led, __set_empty) 
    Piezo = property(__get_piezo, __set_empty)
    PullNone = property(__get_pullnone, __set_empty)
    PullUp = property(__get_pullup, __set_empty)
    PullDown = property(__get_pulldown, __set_empty)
