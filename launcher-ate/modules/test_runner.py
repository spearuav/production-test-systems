from modules.test_loader import TestLoader
from modules.test_context import TestContext

class TestRunner:
    def __init__(self, test_loader: TestLoader):
        self.test_loader = test_loader

    def run_all_tests(self, context: TestContext):
        # Run setup action
        if "setup" in self.test_loader.actions:
            context.run_action("setup")

        # Run all tests
        for test in self.test_loader.tests:
            context.run_test(test)
            if "reset" in self.test_loader.actions:
                context.run_action("reset")

        # Run setdown action
        if "setdown" in self.test_loader.actions:
            context.run_action("setdown")

    def run_single_test(self, context: TestContext, name: str):
        # Run setup action
        if "setup" in self.test_loader.actions:
            context.run_action("setup")

        # Run the test
        context.run_test(name)