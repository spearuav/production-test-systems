"""
Example test demonstrating the clean test structure with injected globals.

Import from test_globals to make linters happy - the actual objects are
injected at runtime by TestRunner.
"""
from modules.test_globals import V5_UUT, fail, success


def run(context):
    """
    Main test function - resources imported from test_globals are replaced at runtime.
    
    Args:
        context: TestContext (provided by runner, but not needed since globals are injected)
    """
    # Example: Check if a value is within range - no prefixes needed!
    expected_voltage = 5.0
    
    # Simulate reading a value (in real test, this would come from hardware)
    V5_UUT._value = 5.1
    actual_voltage = V5_UUT.value
    
    # Check if within tolerance
    tolerance = 0.5
    if abs(actual_voltage - expected_voltage) <= tolerance:
        success(f"Voltage OK: {actual_voltage}V (expected {expected_voltage}V)")
    else:
        fail(f"Voltage out of range: {actual_voltage}V (expected {expected_voltage}V ± {tolerance}V)")
    
    # Note: You don't need to log anything - the runner handles all logging
    # The runner will automatically log the start, end, time, and result
