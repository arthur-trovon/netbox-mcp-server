from mcp.server.fastmcp import FastMCP
from fastmcp import FastMCP
from netbox_client import NetBoxRestClient
import os

# Constants for NetBox
NETBOX_STATUS = {
    "ACTIVE": "active",
    "PLANNED": "planned",
    "STAGED": "staged",
    "OFFLINE": "offline",
    "FAILED": "failed",
    "DECOMMISSIONING": "decommissioning"
}

# Mapping of simple object names to API endpoints
NETBOX_OBJECT_TYPES = {
    # DCIM (Device and Infrastructure)
    "cables": "dcim/cables",
    "console-ports": "dcim/console-ports", 
    "console-server-ports": "dcim/console-server-ports",
    "devices": "dcim/devices",
    "device-bays": "dcim/device-bays",
    "device-roles": "dcim/device-roles",
    "device-types": "dcim/device-types",
    "front-ports": "dcim/front-ports",
    "interfaces": "dcim/interfaces",
    "inventory-items": "dcim/inventory-items",
    "locations": "dcim/locations",
    "manufacturers": "dcim/manufacturers",
    "modules": "dcim/modules",
    "module-bays": "dcim/module-bays",
    "module-types": "dcim/module-types",
    "platforms": "dcim/platforms",
    "power-feeds": "dcim/power-feeds",
    "power-outlets": "dcim/power-outlets",
    "power-panels": "dcim/power-panels",
    "power-ports": "dcim/power-ports",
    "racks": "dcim/racks",
    "rack-reservations": "dcim/rack-reservations",
    "rack-roles": "dcim/rack-roles",
    "regions": "dcim/regions",
    "sites": "dcim/sites",
    "site-groups": "dcim/site-groups",
    "virtual-chassis": "dcim/virtual-chassis",
    
    # IPAM (IP Address Management)
    "asns": "ipam/asns",
    "asn-ranges": "ipam/asn-ranges", 
    "aggregates": "ipam/aggregates",
    "fhrp-groups": "ipam/fhrp-groups",
    "ip-addresses": "ipam/ip-addresses",
    "ip-ranges": "ipam/ip-ranges",
    "prefixes": "ipam/prefixes",
    "rirs": "ipam/rirs",
    "roles": "ipam/roles",
    "route-targets": "ipam/route-targets",
    "services": "ipam/services",
    "vlans": "ipam/vlans",
    "vlan-groups": "ipam/vlan-groups",
    "vrfs": "ipam/vrfs",
    
    # Circuits
    "circuits": "circuits/circuits",
    "circuit-types": "circuits/circuit-types",
    "circuit-terminations": "circuits/circuit-terminations",
    "providers": "circuits/providers",
    "provider-networks": "circuits/provider-networks",
    
    # Virtualization
    "clusters": "virtualization/clusters",
    "cluster-groups": "virtualization/cluster-groups",
    "cluster-types": "virtualization/cluster-types",
    "virtual-machines": "virtualization/virtual-machines",
    "vm-interfaces": "virtualization/interfaces",
    
    # Tenancy
    "tenants": "tenancy/tenants",
    "tenant-groups": "tenancy/tenant-groups",
    "contacts": "tenancy/contacts",
    "contact-groups": "tenancy/contact-groups",
    "contact-roles": "tenancy/contact-roles",
    
    # VPN
    "ike-policies": "vpn/ike-policies",
    "ike-proposals": "vpn/ike-proposals",
    "ipsec-policies": "vpn/ipsec-policies",
    "ipsec-profiles": "vpn/ipsec-profiles",
    "ipsec-proposals": "vpn/ipsec-proposals",
    "l2vpns": "vpn/l2vpns",
    "tunnels": "vpn/tunnels",
    "tunnel-groups": "vpn/tunnel-groups",
    
    # Wireless
    "wireless-lans": "wireless/wireless-lans",
    "wireless-lan-groups": "wireless/wireless-lan-groups",
    "wireless-links": "wireless/wireless-links",

    # Extras
    "config-contexts": "extras/config-contexts",
    "custom-fields": "extras/custom-fields",
    "export-templates": "extras/export-templates",
    "image-attachments": "extras/image-attachments",
    "jobs": "extras/jobs",
    "saved-filters": "extras/saved-filters",
    "scripts": "extras/scripts",
    "tags": "extras/tags",
    "webhooks": "extras/webhooks",
}

mcp = FastMCP("NetBox", log_level="DEBUG")
netbox = None

@mcp.tool()
def netbox_get_objects(object_type: str, filters: dict):
    """
    Get objects from NetBox based on their type and filters
    Args:
        object_type: String representing the NetBox object type (e.g. "devices", "ip-addresses")
        filters: dict of filters to apply to the API call based on the NetBox API filtering options
    
    Valid object_type values:
    
    DCIM (Device and Infrastructure):
    - cables
    - console-ports
    - console-server-ports  
    - devices
    - device-bays
    - device-roles
    - device-types
    - front-ports
    - interfaces
    - inventory-items
    - locations
    - manufacturers
    - modules
    - module-bays
    - module-types
    - platforms
    - power-feeds
    - power-outlets
    - power-panels
    - power-ports
    - racks
    - rack-reservations
    - rack-roles
    - regions
    - sites
    - site-groups
    - virtual-chassis
    
    IPAM (IP Address Management):
    - asns
    - asn-ranges
    - aggregates 
    - fhrp-groups
    - ip-addresses
    - ip-ranges
    - prefixes
    - rirs
    - roles
    - route-targets
    - services
    - vlans
    - vlan-groups
    - vrfs
    
    Circuits:
    - circuits
    - circuit-types
    - circuit-terminations
    - providers
    - provider-networks
    
    Virtualization:
    - clusters
    - cluster-groups
    - cluster-types
    - virtual-machines
    - vm-interfaces
    
    Tenancy:
    - tenants
    - tenant-groups
    - contacts
    - contact-groups
    - contact-roles
    
    VPN:
    - ike-policies
    - ike-proposals
    - ipsec-policies
    - ipsec-profiles
    - ipsec-proposals
    - l2vpns
    - tunnels
    - tunnel-groups
    
    Wireless:
    - wireless-lans
    - wireless-lan-groups
    - wireless-links
    
    See NetBox API documentation for filtering options for each object type.
    """
    # Validate object_type exists in mapping
    if object_type not in NETBOX_OBJECT_TYPES:
        valid_types = "\n".join(f"- {t}" for t in sorted(NETBOX_OBJECT_TYPES.keys()))
        raise ValueError(f"Invalid object_type. Must be one of:\n{valid_types}")
        
    # Get API endpoint from mapping
    endpoint = NETBOX_OBJECT_TYPES[object_type]
        
    # Make API call
    return netbox.get(endpoint, params=filters)

@mcp.tool()
def netbox_get_object_by_id(object_type: str, object_id: int):
    """
    Get detailed information about a specific NetBox object by its ID.
    
    Args:
        object_type: String representing the NetBox object type (e.g. "devices", "ip-addresses")
        object_id: The numeric ID of the object
    
    Returns:
        Complete object details
    """
    # Validate object_type exists in mapping
    if object_type not in NETBOX_OBJECT_TYPES:
        valid_types = "\n".join(f"- {t}" for t in sorted(NETBOX_OBJECT_TYPES.keys()))
        raise ValueError(f"Invalid object_type. Must be one of:\n{valid_types}")
        
    # Get API endpoint from mapping
    endpoint = f"{NETBOX_OBJECT_TYPES[object_type]}/{object_id}"
    
    return netbox.get(endpoint)

@mcp.tool()
def netbox_get_changelogs(filters: dict):
    """
    Get object change records (changelogs) from NetBox based on filters.
    
    Args:
        filters: dict of filters to apply to the API call based on the NetBox API filtering options
    
    Returns:
        List of changelog objects matching the specified filters
    
    Filtering options include:
    - user_id: Filter by user ID who made the change
    - user: Filter by username who made the change
    - changed_object_type_id: Filter by ContentType ID of the changed object
    - changed_object_id: Filter by ID of the changed object
    - object_repr: Filter by object representation (usually contains object name)
    - action: Filter by action type (created, updated, deleted)
    - time_before: Filter for changes made before a given time (ISO 8601 format)
    - time_after: Filter for changes made after a given time (ISO 8601 format)
    - q: Search term to filter by object representation

    Example:
    To find all changes made to a specific device with ID 123:
    {"changed_object_type_id": "dcim.device", "changed_object_id": 123}
    
    To find all deletions in the last 24 hours:
    {"action": "delete", "time_after": "2023-01-01T00:00:00Z"}
    
    Each changelog entry contains:
    - id: The unique identifier of the changelog entry
    - user: The user who made the change
    - user_name: The username of the user who made the change
    - request_id: The unique identifier of the request that made the change
    - action: The type of action performed (created, updated, deleted)
    - changed_object_type: The type of object that was changed
    - changed_object_id: The ID of the object that was changed
    - object_repr: String representation of the changed object
    - object_data: The object's data after the change (null for deletions)
    - object_data_v2: Enhanced data representation
    - prechange_data: The object's data before the change (null for creations)
    - postchange_data: The object's data after the change (null for deletions)
    - time: The timestamp when the change was made
    """
    endpoint = "core/object-changes"
    
    # Make API call
    return netbox.get(endpoint, params=filters)

@mcp.tool()
def update_netbox_object(object_type: str, object_id: int, data: dict):
    """
    Update an existing NetBox object by its ID.
    
    Args:
        object_type: String representing the NetBox object type (e.g. "devices", "ip-addresses")
        object_id: The numeric ID of the object to update
        data: Object data to update with new values
    
    Returns:
        The updated object as a dict
    """
    # Validate object_type exists in mapping
    if object_type not in NETBOX_OBJECT_TYPES:
        valid_types = "\n".join(f"- {t}" for t in sorted(NETBOX_OBJECT_TYPES.keys()))
        raise ValueError(f"Invalid object_type. Must be one of:\n{valid_types}")
        
    # Get API endpoint from mapping
    endpoint = NETBOX_OBJECT_TYPES[object_type]
    
    # Make API call
    return netbox.update(endpoint, object_id, data)

@mcp.tool()
def create_netbox_object(object_type: str, data: dict):
    """
    Create a new NetBox object.
    
    Args:
        object_type: String representing the NetBox object type (e.g. "devices", "ip-addresses")
        data: Dictionary containing the object data according to NetBox API specifications
    
    Returns:
        The created object as a dict

    Examples:
    Creating a new device:
    {
        "name": "sw-core-01",
        "device_type": 1,  # ID of the device type
        "device_role": 1,  # ID of the device role
        "site": 1,         # ID of the site
        "status": "active"
    }

    Creating a new IP address:
    {
        "address": "192.168.1.1/24",
        "status": "active",
        "dns_name": "gateway.local"
    }

    Creating a new VLAN:
    {
        "vid": 100,
        "name": "User Access",
        "site": 1,
        "status": "active"
    }
    """
    # Validate object_type exists in mapping
    if object_type not in NETBOX_OBJECT_TYPES:
        valid_types = "\n".join(f"- {t}" for t in sorted(NETBOX_OBJECT_TYPES.keys()))
        raise ValueError(f"Invalid object_type. Must be one of:\n{valid_types}")
        
    # Get API endpoint from mapping
    endpoint = NETBOX_OBJECT_TYPES[object_type]
    
    # Make API call
    return netbox.create(endpoint, data)

@mcp.tool()
def bulk_create_netbox_objects(object_type: str, data: list):
    """
    Create multiple NetBox objects at once.
    
    Args:
        object_type: String representing the NetBox object type (e.g. "devices", "ip-addresses")
        data: List of dictionaries containing the object data
              Format: [{"field1": "value1"}, {"field2": "value2"}]
    
    Returns:
        List of created objects as dicts
    """
    # Validate object_type exists in mapping
    if object_type not in NETBOX_OBJECT_TYPES:
        valid_types = "\n".join(f"- {t}" for t in sorted(NETBOX_OBJECT_TYPES.keys()))
        raise ValueError(f"Invalid object_type. Must be one of:\n{valid_types}")
        
    # Get API endpoint from mapping
    endpoint = NETBOX_OBJECT_TYPES[object_type]
    
    # Make API call
    return netbox.bulk_create(endpoint, data)

@mcp.tool()
def create_network_device(name: str, device_type_id: int, site_id: int, role_id: int, status: str = "active", serial: str = "", description: str = ""):
    """
    Create a new network device in NetBox with simplified parameters.
    
    Args:
        name: Name of the device (e.g. "R1", "SW-CORE-01")
        device_type_id: ID of the device type (reference to device types in NetBox)
        site_id: ID of the site where the device is located
        role_id: ID of the device role (e.g. Router, Switch, Firewall)
        status: Device status (use NETBOX_STATUS constants, defaults to "active")
        serial: Serial number of the device
        description: Description of the device
    
    Returns:
        The created device object
    
    Example:
        create_network_device(
            name="R1",
            device_type_id=1,  # ISR4321
            site_id=1,         # Main Site
            role_id=1,         # Router
            status=NETBOX_STATUS["ACTIVE"],
            serial="FTX1234567",
            description="Core Router"
        )
    """
    # Validate status
    if status not in NETBOX_STATUS.values():
        valid_statuses = ", ".join(NETBOX_STATUS.values())
        raise ValueError(f"Invalid status. Must be one of: {valid_statuses}")
    
    # Prepare device data
    device_data = {
        "name": name,
        "device_type": device_type_id,
        "site": site_id,
        "role": role_id,
        "status": status
    }
    
    # Add optional fields if provided
    if serial:
        device_data["serial"] = serial
    if description:
        device_data["description"] = description
    
    return create_netbox_object("devices", device_data)

@mcp.tool()
def create_interface(device_id: int, name: str, type: str = "1000base-t", enabled: bool = True, description: str = ""):
    """
    Create a new interface for a device in NetBox.
    
    Args:
        device_id: ID of the device to add the interface to
        name: Name of the interface (e.g. "GigabitEthernet0/0", "Eth1/1")
        type: Interface type (e.g. "1000base-t", "10gbase-x-sfpp")
        enabled: Whether the interface is enabled
        description: Description of the interface
    
    Returns:
        The created interface object
    
    Example:
        create_interface(
            device_id=1,
            name="GigabitEthernet0/0",
            type="1000base-t",
            enabled=True,
            description="Connection to SW1"
        )
    """
    interface_data = {
        "device": device_id,
        "name": name,
        "type": type,
        "enabled": enabled
    }
    
    if description:
        interface_data["description"] = description
    
    return create_netbox_object("interfaces", interface_data)

@mcp.tool()
def assign_ip_to_interface(interface_id: int, ip_address: str, status: str = "active", dns_name: str = ""):
    """
    Create an IP address and assign it to an interface in NetBox.
    
    Args:
        interface_id: ID of the interface to assign the IP to
        ip_address: IP address with prefix (e.g. "192.168.1.1/24")
        status: IP address status (use NETBOX_STATUS constants, defaults to "active")
        dns_name: DNS name for the IP address
    
    Returns:
        The created IP address object
    
    Example:
        assign_ip_to_interface(
            interface_id=1,
            ip_address="192.168.1.1/24",
            status=NETBOX_STATUS["ACTIVE"],
            dns_name="router1.local"
        )
    """
    # Validate status
    if status not in NETBOX_STATUS.values():
        valid_statuses = ", ".join(NETBOX_STATUS.values())
        raise ValueError(f"Invalid status. Must be one of: {valid_statuses}")
    
    ip_data = {
        "address": ip_address,
        "status": status,
        "assigned_object_type": "dcim.interface",
        "assigned_object_id": interface_id
    }
    
    if dns_name:
        ip_data["dns_name"] = dns_name
    
    return create_netbox_object("ip-addresses", ip_data)

if __name__ == "__main__":
    # Load NetBox configuration from environment variables
    netbox_url = os.getenv("NETBOX_URL")
    netbox_token = os.getenv("NETBOX_TOKEN")
    
    if not netbox_url or not netbox_token:
        raise ValueError("NETBOX_URL and NETBOX_TOKEN environment variables must be set")
    
    # Initialize NetBox client
    netbox = NetBoxRestClient(url=netbox_url, token=netbox_token, verify_ssl=False)
    
    port = 8081
    mcp.run(transport="http", host="10.0.0.130", port=port)
