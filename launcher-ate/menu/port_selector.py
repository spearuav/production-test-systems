from menu.style import PALETTE
from modules.port_finder import PortInfo

# The Template - Clean, logic-free, and easy to read
PORT_TEMPLATE = """
{logo}
{separator}
            PORT SELECT
{separator}

Port list:
{PortListString}

{current_port_line}
p. Probe port to see if the connected device is a launcher tester (should be harmless)
a. Automatically probe all ports
s. Rescan port list

{neutral}b. Back{reset}

{separator}
{last_action}
"""

def color_selector(port:PortInfo):
    # color "vector"
    v="⚫🔴🟡🟢🔵"
    # return \
    # (
    #     v[0] if not port.is_serial else
    #     v[1] if not port.is_usb else
    #     v[2] if not port.known_vid else
    #     v[3] if not port.probed else
    #     v[4]
    # )
    return \
    (
        v[4] if port.probed else
        v[3] if port.known_vid else
        v[2] if port.is_usb else
        #v[1] if port.is_serial else
        v[0]
    )

def render_port_selector(props: dict):
    """
    Renders the port selector UI.
    Expects 'props' to contain:
    - logo, PortInfoList, last_action, current_port
    """
    P = PALETTE
    info_list:list[PortInfo] = props["PortInfoList"]
    current_port = props["current_port"]
    indexes = range(1,len(info_list)+1)
    # PortListString = "\n".join(map(lambda port,index:\
    #                     [f"{P["error"]}No ports were found"] if len(info_list) == 0 else \
    #                     f"{color_selector(port)} {index}{P["bright"]}{port.port.name} {P["normal"]}{port.port.usb_info()}.",info_list,indexes)\
    #                     )
    if len(info_list) == 0:
        PortListString = f"{P["error"]}No ports were found"
    else:
        PortListString = "\n".join(map(lambda port,index:\
                        [f"{P["error"]}No ports were found"] if len(info_list) == 0 else \
                        f"{color_selector(port)} {index}. {P["bright"]}{port.port.name} {P["normal"]}{port.port.usb_info()}.",info_list,indexes)\
                        )
    current_port_line = f"\t{P["error"]}No port selected" if not current_port else \
                        f"\t{color_selector(current_port)} {P["bright"]}{current_port.port.name} {P["normal"]}{current_port.port.usb_info()}"
    # Merge global styles with the specific instance data
    # This allows the template to use {neutral}, {reset}, etc. automatically
    render_context = {
        **PALETTE,
        **props,
        "PortListString": PortListString,
        "current_port_line": current_port_line
    }
    
    return PORT_TEMPLATE.format(**render_context)
