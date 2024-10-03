class FrequencyController:
    def __init__(self, serialPort):
        self.serialPort = serialPort
        self.MaxFrequency = 1000000
        self.MinFrequency = 16

    def Write(self, pin, frequency, duration_ms=0, dutycyle=50):
        if frequency < self.MinFrequency or frequency > self.MaxFrequency:
            raise ValueError("Frequency must be in range 15Hz..10000000Hz")

        if duration_ms > 99999999:
            raise ValueError("duration_ms must be in range 0..99999999")

        if dutycyle < 0 or dutycyle > 100:
            raise ValueError("dutycyle must be in range 0..100")

        if pin == 'p' or pin == 'P':
            pin = 112

        cmd = "freq({}, {}, {}, {})".format(pin, frequency, duration_ms, dutycyle)
        self.serialPort.WriteCommand(cmd)

        res = self.serialPort.ReadRespone()

        return res.success
