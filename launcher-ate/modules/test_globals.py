"""
Global test resources for import into test modules.

This module provides type stubs and documentation for all resources that are
injected into test modules at runtime. Import this to make linters happy:

    from modules.test_globals import ON, OFF, V5_UUT, fail, success

The actual objects are injected by TestRunner at runtime, but this provides
the names and type hints so your IDE/linter doesn't complain.

All the docstrings and type hints here mirror the actual implementations
in TestContext, providing full IDE support.
"""

from typing import Any, Dict, Optional


class Readable:
    """
    Readable signal interface for reading hardware values.
    
    Attributes:
        name: Signal name
        value: Current value of the signal (read-only property)
    """
    name: str
    
    @property
    def value(self) -> Any:
        """Get the current value of the readable."""
        pass
    
    def test_stable(self) -> None:
        """Test the stability of the readable value."""
        pass
    
    def test_change_time(self) -> None:
        """Test the time it takes for the value to change."""
        pass


class Setable:
    """
    Setable control interface for setting hardware outputs.
    
    Attributes:
        name: Control name
    """
    name: str
    
    def set(self, value: Any) -> None:
        """
        Set the value of the setable.
        
        Args:
            value: The value to set (type depends on hardware)
        """
        pass
    
    def set_pwm(self, duty_cycle: float) -> None:
        """
        Set the PWM duty cycle of the setable.
        
        Args:
            duty_cycle: PWM duty cycle (0.0 to 1.0)
        """
        pass


# Type stubs for linters (actual objects injected at runtime)
# Readable signals - hardware inputs we can read
ON_RTRN: Readable = None  # type: ignore
"""ON return signal - indicates ON state feedback"""

OFF_RTRN: Readable = None  # type: ignore
"""OFF return signal - indicates OFF state feedback"""

BIT_STAT: Readable = None  # type: ignore
"""BIT status signal - Built-In Test status"""

BIT_IND: Readable = None  # type: ignore
"""BIT indicator signal - Built-In Test indicator"""

DRN_PRES: Readable = None  # type: ignore
"""Drone present signal - indicates drone detection"""

CAP_PRES: Readable = None  # type: ignore
"""Capacitor present signal - indicates capacitor detection"""

Blue: Readable = None  # type: ignore
"""Blue LED indicator state"""

Green: Readable = None  # type: ignore
"""Green LED indicator state"""

Inflator: Readable = None  # type: ignore
"""Inflator status/feedback signal"""

Charge: Readable = None  # type: ignore
"""Charge status/feedback signal"""

V5_UUT: Readable = None  # type: ignore
"""5V UUT (Unit Under Test) voltage reading"""

# Setable controls - hardware outputs we can control
ON: Setable = None  # type: ignore
"""ON control - activate ON state"""

OFF: Setable = None  # type: ignore
"""OFF control - activate OFF state"""

INF_EN: Setable = None  # type: ignore
"""Inflator enable control"""

CHRG_EN: Setable = None  # type: ignore
"""Charge enable control"""

TRIG: Setable = None  # type: ignore
"""Trigger control"""

LAUNCH_EN: Setable = None  # type: ignore
"""Launch enable control"""

LAUNCH_CONSENT: Setable = None  # type: ignore
"""Launch consent control - safety interlock"""


# Test control functions
def fail(message: str) -> None:
    """
    Mark the current test as failed and stop execution.
    
    This raises a TestResult exception that is caught by the runner,
    which logs the failure and continues with the next test.
    
    Args:
        message: Description of why the test failed
        
    Raises:
        TestResult: Always raised to stop test execution
    """
    pass


def success(message: str = "Test succeeded") -> None:
    """
    Mark the current test as successful and stop execution.
    
    This raises a TestResult exception that is caught by the runner,
    which logs the success and continues with the next test.
    
    Args:
        message: Description of test success (optional)
        
    Raises:
        TestResult: Always raised to stop test execution
    """
    pass


def operator_action(message: str) -> str:
    """
    Request an action from the operator and wait for input.
    
    Displays a message to the operator and waits for them to complete
    the requested action and press Enter.
    
    Args:
        message: Instructions for the operator
        
    Returns:
        The operator's input (usually just confirmation via Enter)
        
    Example:
        operator_action("Please connect the cable and press Enter")
    """
    pass


def iperf(**parameters) -> None:
    """
    Run iperf network performance test with given parameters.
    
    Args:
        **parameters: iperf parameters (e.g., duration, bandwidth, etc.)
        
    Example:
        iperf(duration=10, bandwidth="100M")
    """
    pass


# Test utility functions
def test_time_to_trigger() -> None:
    """
    Test the time it takes for a signal to trigger.
    
    Measures and validates trigger timing against expected values.
    """
    pass


def test_time_to_value() -> None:
    """
    Test the time it takes for a signal to reach a target value.
    
    Measures and validates transition timing against expected values.
    """
    pass


def test_stable() -> None:
    """
    Test the stability of a signal over time.
    
    Validates that a signal remains within acceptable bounds over
    a specified duration.
    """
    pass

# Configuration dictionaries
i2c: Dict[str, Any] = {"timeout": None, "limits": None}
"""I2C communication configuration dict with timeout and limits settings"""

op_timeout: Optional[float] = None
"""Operator action timeout in seconds (None = no timeout)"""

# Export all for wildcard import
__all__ = [
    # Classes
    'Readable', 'Setable',
    # Readable signals
    'ON_RTRN', 'OFF_RTRN', 'BIT_STAT', 'BIT_IND', 'DRN_PRES', 'CAP_PRES',
    'Blue', 'Green', 'Inflator', 'Charge', 'V5_UUT',
    # Setable controls
    'ON', 'OFF', 'INF_EN', 'CHRG_EN', 'TRIG', 'LAUNCH_EN', 'LAUNCH_CONSENT',
    # Test control functions
    'fail', 'success', 'operator_action', 'iperf',
    # Test utilities
    'test_time_to_trigger', 'test_time_to_value', 'test_stable',
    # Configuration
    'i2c', 'op_timeout'
]
