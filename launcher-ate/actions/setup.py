"""
Example setup action with injected globals.

Import from test_globals to make linters happy - the actual objects are
injected at runtime by TestRunner.

Actions are automatically run by TestRunner:
- 'setup' runs before all tests
- 'reset' runs between each test
- 'teardown' runs after all tests
"""
from modules.test_globals import *


def run(context):
    """
    Setup action - prepares the test environment.
    
    Args:
        context: TestContext (provided by runner, but not needed since globals are injected)
    """
    # Initialize hardware to a known state - no prefixes needed!
    ON.set(False)
    OFF.set(False)
    INF_EN.set(False)
    CHRG_EN.set(False)
    TRIG.set(False)
    LAUNCH_EN.set(False)
    LAUNCH_CONSENT.set(False)
    success("Setup complete - hardware initialized to known state")
    
    # Can request operator actions if needed
    # response = operator_action("Please connect the device and press Enter")
    
    # Actions don't need to call success() or fail()
    # If they complete without raising an exception, they're considered successful
