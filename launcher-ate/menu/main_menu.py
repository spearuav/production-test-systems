from menu.style import PALETTE

# The Template - Clean, logic-free, and easy to read
MENU_TEMPLATE = """
{logo}
{separator}
            MAIN MENU
{separator}

\t\t{op_color}Operator Name:{reset} {operator_name}
{op_color}1. Set Operator Name{reset}

\t\t{sn_color}Launcher SN#:{reset} {launcher_sn}
{sn_color}2. Set Launcher SN#{reset}

\t\t{port_color}Serial port:{reset} {port_display}
{neutral}3. Select USB Port{reset}

{test_info_str}
{run_color}4. Run Tests{reset}
{run_color}5. Run a Single Test{reset}
{neutral}6. Reload Tests{reset}
{neutral}7. Exit{reset}

{separator}
"""

def render_main_menu(props: dict):
    """
    Renders the main menu UI.
    Expects 'props' to contain:
    - logo, operator_name, launcher_sn, port_display, test_info_str
    - op_color, sn_color, port_color, run_color (resolved from PALETTE in logic)
    """
    
    # Merge global styles with the specific instance data
    # This allows the template to use {neutral}, {reset}, etc. automatically
    render_context = {
        **PALETTE,
        **props
    }
    
    return MENU_TEMPLATE.format(**render_context)
