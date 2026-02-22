
import time

class Readable:
    def __init__(self, name):
        self.name = name
        self._value = None

    @property
    def value(self):
        """Get the current value of the readable."""
        return self._value

    def test_stable(self):
        """Test the stability of the readable value."""
        # Implement stability test logic here
        pass

    def test_change_time(self):
        """Test the time it takes for the value to change."""
        # Implement change time test logic here
        pass


class Setable:
    def __init__(self, name):
        self.name = name

    def set(self, value):
        """Set the value of the setable."""
        # Implement set logic here
        pass

    def set_pwm(self, duty_cycle):
        """Set the PWM value of the setable."""
        # Implement PWM logic here
        pass


class TestContext:
    def __init__(self, operator_name, launcher_sn, logger, atr_writer):
        self.operator_name = operator_name
        self.launcher_sn = launcher_sn
        self.logger = logger
        self.atr_writer = atr_writer
        self.i2c = {"timeout": None, "limits": None}
        self.op_timeout = None

        # Initialize readable properties
        self.ON_RTRN = Readable("ON_RTRN")
        self.OFF_RTRN = Readable("OFF_RTRN")
        self.BIT_STAT = Readable("BIT_STAT")
        self.BIT_IND = Readable("BIT_IND")
        self.DRN_PRES = Readable("DRN_PRES")
        self.CAP_PRES = Readable("CAP_PRES")
        self.Blue = Readable("Blue")
        self.Green = Readable("Green")
        self.Inflator = Readable("Inflator")
        self.Charge = Readable("Charge")
        self.V5_UUT = Readable("5V_UUT")

        # Initialize setable properties
        self.ON = Setable("ON")
        self.OFF = Setable("OFF")
        self.INF_EN = Setable("INF_EN")
        self.CHRG_EN = Setable("CHRG_EN")
        self.TRIG = Setable("TRIG")
        self.LAUNCH_EN = Setable("LAUNCH_EN")
        self.LAUNCH_CONSENT = Setable("LAUNCH_CONSENT")

    # Test methods
    def fail(self, message):
        self.log(f"Test failed: {message}")
        self._test_end(success=False)
        raise Exception(message)

    def success(self):
        msg= "Test succeeded"
        self.log(msg)
        self._test_end(success=True)
        raise Exception(msg)

    # Logging
    def log(self, text):
        self.logger.info(text)

    def operator_action(self, message):
        return input(f"Operator action required: {message}")


    # Test utilities
    def test_time_to_trigger(self):
        self.log("Testing time to trigger")

    def test_time_to_value(self):
        self.log("Testing time to value")

    def test_stable(self):
        self.log("Testing stability")

    # Test execution
    def run_test(self, name):
        self.log(f"Running test: {name}")
        self._test_start_time = time.time()
        self._test_name = name

    def _test_end(self, success):
        end_time = time.time()
        duration = end_time - getattr(self, '_test_start_time', end_time)
        status = 'passed' if success else 'failed'
        self.log(f"Test {status}: {getattr(self, '_test_name', '')}")
        self.log(f"Test time taken: {duration:.2f} seconds")

    def run_action(self, name):
        self.log(f"Running action: {name}")

    # Iperf
    def iperf(self, **parameters):
        self.log(f"Running iperf with parameters: {parameters}")