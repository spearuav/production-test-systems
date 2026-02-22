"""
iPerf network performance test.

Tests network throughput and connectivity using iPerf.
"""
from modules.test_globals import iperf, success, fail, operator_action


def run(context):
    """
    Run iPerf network performance test.
    
    Args:
        context: TestContext (provided by runner)
    """
    # Example: Run iperf with specific parameters
    # In a real implementation, this would execute iperf and check results
    
    try:
        # Request operator to ensure network connection
        operator_action("Ensure network cable is connected, then press Enter")
        
        # Run iperf test with desired parameters
        iperf(
            duration=10,          # 10 second test
            bandwidth="100M",     # 100 Mbps target
            protocol="TCP"        # TCP protocol
        )
        
        # In a real test, you would:
        # 1. Parse iperf output
        # 2. Check against minimum thresholds
        # 3. Validate connection stability
        
        # Example validation (placeholder):
        # actual_bandwidth = parse_iperf_results()
        # if actual_bandwidth < 80:  # 80 Mbps minimum
        #     fail(f"Bandwidth too low: {actual_bandwidth} Mbps")
        
        success("Network performance test passed")
        
    except Exception as e:
        fail(f"iPerf test failed: {e}")
