from contextlib import contextmanager


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


class TestResult(Exception):
    """Base exception for test results."""
    def __init__(self, message, success):
        super().__init__(message)
        self.success = success


class TestContext:
    """
    Context object passed to tests containing only the resources they need.
    Does NOT expose logger, ATRWriter, operator_name, or launcher_sn.
    """
    def __init__(self):
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

    # Test control methods
    def fail(self, message):
        """Mark the current test as failed and stop execution."""
        raise TestResult(message, success=False)

    def success(self, message="Test succeeded"):
        """Mark the current test as successful and stop execution."""
        raise TestResult(message, success=True)

    def operator_action(self, message):
        """Request an action from the operator."""
        return input(f"Operator action required: {message}")

    # Test utilities
    def test_time_to_trigger(self):
        """Test time to trigger logic."""
        # Implement time to trigger test logic here
        pass

    def test_time_to_value(self):
        """Test time to value logic."""
        # Implement time to value test logic here
        pass

    def test_stable(self):
        """Test stability logic."""
        # Implement stability test logic here
        pass

    # Iperf
    def iperf(self, **parameters):
        """Run iperf with given parameters."""
        # Implement iperf logic here
        pass

    @contextmanager
    def select(self, *names):
        """
        Context manager for clean resource access.
        
        Usage:
            with context.select('ON', 'OFF', 'V5_UUT') as (ON, OFF, V5):
                ON.set(True)
                voltage = V5.value
        
        This allows tests to unpack only the resources they need and use them
        without the context. prefix, making code cleaner and more readable.
        """
        resources = []
        for name in names:
            if hasattr(self, name):
                resources.append(getattr(self, name))
            else:
                # Special case for methods like 'fail', 'success'
                if name in ('fail', 'success', 'operator_action'):
                    resources.append(getattr(self, name))
                else:
                    raise AttributeError(f"TestContext has no attribute '{name}'")
        
        yield tuple(resources) if len(resources) > 1 else resources[0]
