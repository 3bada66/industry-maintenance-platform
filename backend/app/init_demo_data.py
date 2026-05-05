import uuid
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import (
    User, Role, Tenant, Asset, Location, Site, Area, 
    Supplier, Manufacturer, Contact, AssetType, AssetStatus,
    AssetInterface, AssetConnection
)
from app.services.auth import get_password_hash
from datetime import datetime, timedelta
import random


def seed_demo_data():
    """Populate database with realistic demo data in English"""
    print("🌱 Seeding demo data using Python...")
    seed_demo_data_python()


def seed_demo_data_python():
    """Populate database with realistic demo data using Python"""
    db: Session = SessionLocal()
    
    # Get or create tenant
    tenant = db.query(Tenant).first()
    if not tenant:
        tenant = Tenant(
            id=uuid.uuid4(),
            name="Industrial Solutions Corp",
            slug="industrial-solutions",
            settings={"theme": "industrial", "language": "en"}
        )
        db.add(tenant)
        db.commit()
        db.refresh(tenant)
        print(f"✅ Created tenant: {tenant.name}")
    
    # Get roles
    admin_role = db.query(Role).filter_by(name="admin").first()
    editor_role = db.query(Role).filter_by(name="editor").first()
    viewer_role = db.query(Role).filter_by(name="viewer").first()
    
    # Initialize asset types, statuses and manufacturers if they don't exist
    from app.init_asset_types import setup_asset_types
    from app.init_asset_statuses import setup_asset_statuses
    from app.init_manufacturers import seed_manufacturers
    
    setup_asset_types(tenant.id)
    setup_asset_statuses(tenant.id)
    seed_manufacturers(tenant.id)
    
    # Get asset types and statuses
    asset_types = db.query(AssetType).all()
    asset_statuses = db.query(AssetStatus).all()
    
    # Ensure we have at least one asset type and status
    if not asset_types:
        print("❌ No asset types found. Cannot create assets.")
        db.close()
        return
    if not asset_statuses:
        print("❌ No asset statuses found. Cannot create assets.")
        db.close()
        return
    
    # Create demo sites
    sites_data = [
        {
            "name": "Main Production Plant",
            "code": "MPP",
            "description": "Primary manufacturing facility for automotive components",
            "address": "Atatürk Sanayi Sitesi, Ikitelli OSB, 34306 Istanbul, Turkey"
        },
        {
            "name": "Research & Development Center",
            "code": "RDC",
            "description": "Innovation hub for new product development",
            "address": "ODTÜ Teknokent, Üniversiteler Mah., 06800 Ankara, Turkey"
        },
        {
            "name": "Distribution Warehouse",
            "code": "DW",
            "description": "Central logistics and distribution facility",
            "address": "Torbali Logistics Park, 35860 Izmir, Turkey"
        }
    ]
    
    sites = []
    for site_data in sites_data:
        existing_site = db.query(Site).filter_by(name=site_data["name"], tenant_id=tenant.id).first()
        if not existing_site:
            site = Site(
                id=uuid.uuid4(),
                tenant_id=tenant.id,
                name=site_data["name"],
                code=site_data["code"],
                description=site_data["description"],
                address=site_data["address"]
            )
            db.add(site)
            sites.append(site)
            print(f"✅ Created site: {site.name}")
        else:
            sites.append(existing_site)
    
    db.commit()
    
    # Create demo areas for each site
    areas_data = [
        # Main Production Plant areas
        {"name": "Assembly Line A", "code": "ALA", "notes": "Primary assembly line for engine components"},
        {"name": "Assembly Line B", "code": "ALB", "notes": "Secondary assembly line for transmission parts"},
        {"name": "Quality Control Lab", "code": "QCL", "notes": "Testing and quality assurance facility"},
        {"name": "Maintenance Bay", "code": "MB", "notes": "Equipment maintenance and repair area"},
        {"name": "Control Room", "code": "CR", "notes": "Central monitoring and control center"},
        
        # R&D Center areas
        {"name": "Prototype Lab", "code": "PL", "notes": "New product prototyping and testing"},
        {"name": "Materials Lab", "code": "ML", "notes": "Material science research and testing"},
        {"name": "Software Development", "code": "SD", "notes": "Control system software development"},
        {"name": "Testing Chamber", "code": "TC", "notes": "Environmental and stress testing"},
        
        # Distribution Warehouse areas
        {"name": "Receiving/Shipping Docks", "code": "RSD", "notes": "Incoming and outgoing logistics"},
        {"name": "Storage Zone A", "code": "SZA", "notes": "High-value component storage"},
        {"name": "Storage Zone B", "code": "SZB", "notes": "Bulk material storage"}
    ]
    
    areas = []
    for area_data in areas_data:
        existing_area = db.query(Area).filter_by(name=area_data["name"], tenant_id=tenant.id).first()
        if not existing_area:
            # Assign area to appropriate site
            if "Assembly" in area_data["name"] or "Quality" in area_data["name"] or "Maintenance" in area_data["name"] or "Control" in area_data["name"]:
                site = next((s for s in sites if "Production Plant" in s.name), sites[0])
            elif "Prototype" in area_data["name"] or "Materials" in area_data["name"] or "Software" in area_data["name"] or "Testing" in area_data["name"]:
                site = next((s for s in sites if "Research" in s.name), sites[0])
            else:
                site = next((s for s in sites if "Distribution" in s.name), sites[0])
            
            area = Area(
                id=uuid.uuid4(),
                tenant_id=tenant.id,
                name=area_data["name"],
                site_id=site.id,
                code=area_data["code"],
                notes=area_data["notes"]
            )
            db.add(area)
            areas.append(area)
            print(f"✅ Created area: {area.name}")
        else:
            areas.append(existing_area)
    
    db.commit()
    
    # Create demo locations
    locations_data = [
        # Production Plant locations
        {"name": "Control Panel A1", "code": "CPA1", "description": "Main control panel for Assembly Line A", "area": "Assembly Line A"},
        {"name": "Control Panel A2", "code": "CPA2", "description": "Secondary control panel for Assembly Line A", "area": "Assembly Line A"},
        {"name": "Control Panel B1", "code": "CPB1", "description": "Main control panel for Assembly Line B", "area": "Assembly Line B"},
        {"name": "Quality Station 1", "code": "QS1", "description": "Primary quality control station", "area": "Quality Control Lab"},
        {"name": "Quality Station 2", "code": "QS2", "description": "Secondary quality control station", "area": "Quality Control Lab"},
        {"name": "Maintenance Bay 1", "code": "MB1", "description": "Primary maintenance work area", "area": "Maintenance Bay"},
        {"name": "Maintenance Bay 2", "code": "MB2", "description": "Secondary maintenance work area", "area": "Maintenance Bay"},
        {"name": "Control Room Console", "code": "CRC", "description": "Main control room console", "area": "Control Room"},
        {"name": "Control Room Display", "code": "CRD", "description": "Control room display wall", "area": "Control Room"},
        
        # R&D Center locations
        {"name": "Prototype Station 1", "code": "PS1", "description": "Primary prototype development station", "area": "Prototype Lab"},
        {"name": "Prototype Station 2", "code": "PS2", "description": "Secondary prototype development station", "area": "Prototype Lab"},
        {"name": "Materials Testing Station", "code": "MTS", "description": "Materials testing and analysis station", "area": "Materials Lab"},
        {"name": "Software Development Station", "code": "SDS", "description": "Software development and testing station", "area": "Software Development"},
        {"name": "Testing Chamber 1", "code": "TC1", "description": "Primary environmental testing chamber", "area": "Testing Chamber"},
        
        # Warehouse locations
        {"name": "Receiving Dock 1", "code": "RD1", "description": "Primary receiving dock", "area": "Receiving/Shipping Docks"},
        {"name": "Shipping Dock 1", "code": "SD1", "description": "Primary shipping dock", "area": "Receiving/Shipping Docks"},
        {"name": "Storage Rack A1", "code": "SRA1", "description": "High-value component storage rack", "area": "Storage Zone A"},
        {"name": "Storage Rack A2", "code": "SRA2", "description": "Secondary high-value storage rack", "area": "Storage Zone A"},
        {"name": "Bulk Storage Area 1", "code": "BSA1", "description": "Primary bulk material storage area", "area": "Storage Zone B"}
    ]
    
    locations = []
    for location_data in locations_data:
        existing_location = db.query(Location).filter_by(name=location_data["name"], tenant_id=tenant.id).first()
        if not existing_location:
            # Find the area for this location
            area = next((a for a in areas if a.name == location_data["area"]), None)
            if area:
                location = Location(
                    id=uuid.uuid4(),
                    tenant_id=tenant.id,
                    site_id=area.site_id,
                    area_id=area.id,
                    name=location_data["name"],
                    code=location_data["code"],
                    description=location_data["description"]
                )
                db.add(location)
                locations.append(location)
                print(f"✅ Created location: {location.name}")
        else:
            locations.append(existing_location)
    
    db.commit()
    
    # Create demo manufacturers
    manufacturers_data = [
        {"name": "Siemens", "description": "Industrial automation and control systems"},
        {"name": "Rockwell Automation", "description": "Industrial automation and information solutions"},
        {"name": "Schneider Electric", "description": "Energy management and automation"},
        {"name": "ABB", "description": "Power and automation technologies"}
    ]
    
    manufacturers = []
    for mfg_data in manufacturers_data:
        existing_mfg = db.query(Manufacturer).filter_by(name=mfg_data["name"], tenant_id=tenant.id).first()
        if not existing_mfg:
            manufacturer = Manufacturer(
                id=uuid.uuid4(),
                tenant_id=tenant.id,
                name=mfg_data["name"],
                description=mfg_data["description"]
            )
            db.add(manufacturer)
            manufacturers.append(manufacturer)
            print(f"✅ Created manufacturer: {manufacturer.name}")
        else:
            manufacturers.append(existing_mfg)
    
    db.commit()
    
    # Create demo suppliers
    suppliers_data = [
        {"name": "Siemens Industrial Automation", "description": "PLC and HMI systems supplier"},
        {"name": "Rockwell Automation Solutions", "description": "Allen-Bradley products and services"},
        {"name": "Schneider Electric Systems", "description": "Modicon and Telemecanique products"},
        {"name": "ABB Industrial Solutions", "description": "AC500 and 800xA systems"}
    ]
    
    suppliers = []
    for sup_data in suppliers_data:
        existing_sup = db.query(Supplier).filter_by(name=sup_data["name"], tenant_id=tenant.id).first()
        if not existing_sup:
            supplier = Supplier(
                id=uuid.uuid4(),
                tenant_id=tenant.id,
                name=sup_data["name"],
                description=sup_data["description"]
            )
            db.add(supplier)
            suppliers.append(supplier)
            print(f"✅ Created supplier: {supplier.name}")
        else:
            suppliers.append(existing_sup)
    
    db.commit()
    
    # Create demo contacts
    contacts_data = [
        {"first_name": "Ahmet",   "last_name": "Yilmaz", "email": "ahmet.yilmaz@siemens-otomasyon.com.tr",    "phone1": "+90-212-555-0101", "type": "Sales Manager",         "supplier": "Siemens Industrial Automation"},
        {"first_name": "Fatma",   "last_name": "Kaya",   "email": "fatma.kaya@rockwell.com.tr",               "phone1": "+90-312-555-0102", "type": "Technical Support",     "supplier": "Rockwell Automation Solutions"},
        {"first_name": "Mehmet",  "last_name": "Demir",  "email": "mehmet.demir@schneider-electric.com.tr",   "phone1": "+90-232-555-0103", "type": "Account Manager",       "supplier": "Schneider Electric Systems"},
        {"first_name": "Ayse",    "last_name": "Celik",  "email": "ayse.celik@abb.com.tr",                    "phone1": "+90-216-555-0104", "type": "Product Specialist",    "supplier": "ABB Industrial Solutions"},
        {"first_name": "Ibrahim", "last_name": "Sahin",  "email": "ibrahim.sahin@siemens-otomasyon.com.tr",   "phone1": "+90-212-555-0105", "type": "Service Engineer",      "supplier": "Siemens Industrial Automation"},
        {"first_name": "Zeynep",  "last_name": "Arslan", "email": "zeynep.arslan@rockwell.com.tr",            "phone1": "+90-312-555-0106", "type": "Sales Representative",  "supplier": "Rockwell Automation Solutions"}
    ]
    
    contacts = []
    for contact_data in contacts_data:
        existing_contact = db.query(Contact).filter_by(email=contact_data["email"], tenant_id=tenant.id).first()
        if not existing_contact:
            # Find the supplier for this contact
            supplier = next((s for s in suppliers if s.name == contact_data["supplier"]), None)
            
            contact = Contact(
                id=uuid.uuid4(),
                tenant_id=tenant.id,
                first_name=contact_data["first_name"],
                last_name=contact_data["last_name"],
                email=contact_data["email"],
                phone1=contact_data["phone1"],
                type=contact_data["type"]
            )
            db.add(contact)
            contacts.append(contact)
            print(f"✅ Created contact: {contact.first_name} {contact.last_name}")
        else:
            contacts.append(existing_contact)
    
    db.commit()
    
    # Create demo assets
    assets_data = [
        {
            "name": "PLC Controller A1",
            "tag": "PLC-A1",
            "description": "Siemens S7-1500 PLC for Assembly Line A",
            "asset_type": "PLC",
            "manufacturer": "Siemens",
            "model": "S7-1500",
            "serial_number": "SN-PLC-A1-001",
            "location": "Control Panel A1",
            "risk_score": 7.5,
            "business_criticality": "high",
            "remote_access_type": "attended",
            "physical_access_ease": "internal"
        },
        {
            "name": "HMI Display A1",
            "tag": "HMI-A1",
            "description": "Siemens KTP900 HMI for Assembly Line A",
            "asset_type": "HMI",
            "manufacturer": "Siemens",
            "model": "KTP900",
            "serial_number": "SN-HMI-A1-001",
            "location": "Control Panel A1",
            "risk_score": 6.0,
            "business_criticality": "medium",
            "remote_access_type": "attended",
            "physical_access_ease": "internal"
        },
        {
            "name": "PLC Controller B1",
            "tag": "PLC-B1",
            "description": "Rockwell ControlLogix PLC for Assembly Line B",
            "asset_type": "PLC",
            "manufacturer": "Rockwell Automation",
            "model": "ControlLogix 5580",
            "serial_number": "SN-PLC-B1-001",
            "location": "Control Panel B1",
            "risk_score": 7.0,
            "business_criticality": "high",
            "remote_access_type": "attended",
            "physical_access_ease": "internal"
        },
        {
            "name": "Quality Control Robot",
            "tag": "ROBOT-QC1",
            "description": "ABB IRB 1200 robot for quality inspection",
            "asset_type": "Actuator",
            "manufacturer": "ABB",
            "model": "IRB 1200",
            "serial_number": "SN-ROBOT-QC1-001",
            "location": "Quality Station 1",
            "risk_score": 8.0,
            "business_criticality": "high",
            "remote_access_type": "unattended",
            "physical_access_ease": "internal"
        },
        {
            "name": "Network Switch A",
            "tag": "SW-A1",
            "description": "Cisco Catalyst switch for production network",
            "asset_type": "Switch",
            "manufacturer": "Cisco",
            "model": "Catalyst 2960",
            "serial_number": "SN-SW-A1-001",
            "location": "Control Room",
            "risk_score": 5.5,
            "business_criticality": "medium",
            "remote_access_type": "attended",
            "physical_access_ease": "internal"
        },
        {
            "name": "Temperature Sensor Array",
            "tag": "SENSOR-TEMP1",
            "description": "Temperature monitoring sensors for Assembly Line A",
            "asset_type": "Sensor",
            "manufacturer": "Honeywell",
            "model": "T775",
            "serial_number": "SN-SENSOR-TEMP1-001",
            "location": "Control Panel A1",
            "risk_score": 3.0,
            "business_criticality": "low",
            "remote_access_type": "none",
            "physical_access_ease": "internal"
        },
        {
            "name": "Production Server",
            "tag": "SRV-PROD1",
            "description": "Production data collection and analysis server",
            "asset_type": "Server",
            "manufacturer": "Siemens",
            "model": "PowerEdge R740",
            "serial_number": "SN-SRV-PROD1-001",
            "location": "Control Room",
            "risk_score": 9.0,
            "business_criticality": "critical",
            "remote_access_type": "unattended",
            "physical_access_ease": "internal"
        },
        {
            "name": "Safety System Controller",
            "tag": "SAFETY-CTRL1",
            "description": "Emergency stop and safety monitoring system",
            "asset_type": "PLC",
            "manufacturer": "Schneider Electric",
            "model": "Modicon M580",
            "serial_number": "SN-SAFETY-CTRL1-001",
            "location": "Control Room",
            "risk_score": 9.5,
            "business_criticality": "critical",
            "remote_access_type": "none",
            "physical_access_ease": "internal"
        }
    ]
    
    assets = []
    for asset_data in assets_data:
        existing_asset = db.query(Asset).filter_by(tag=asset_data["tag"], tenant_id=tenant.id).first()
        if not existing_asset:
            # Find the asset type
            asset_type = next((at for at in asset_types if at.name.lower() == asset_data["asset_type"].lower()), None)
            if not asset_type and asset_types:
                asset_type = asset_types[0]
                print(f"⚠️  Asset type '{asset_data['asset_type']}' not found, using '{asset_type.name}' for asset '{asset_data['name']}'")
            
            # Find the manufacturer
            manufacturer = next((m for m in manufacturers if m.name.lower() in asset_data["manufacturer"].lower()), None)
            if not manufacturer and manufacturers:
                manufacturer = manufacturers[0]
                print(f"⚠️  Manufacturer '{asset_data['manufacturer']}' not found, using '{manufacturer.name}' for asset '{asset_data['name']}'")
            
            # Find the location
            location = next((l for l in locations if l.name == asset_data["location"]), None)
            if not location and locations:
                location = locations[0]
                print(f"⚠️  Location '{asset_data['location']}' not found, using '{location.name}' for asset '{asset_data['name']}'")
            
            # Use the first "Active" status, or fall back to first available
            asset_status = next(
                (s for s in asset_statuses if s.name.lower() == "active"),
                asset_statuses[0] if asset_statuses else None,
            )
            
            # Ensure we have all required fields
            if not asset_type:
                print(f"❌ No asset type available for asset '{asset_data['name']}'. Skipping.")
                continue
            if not asset_status:
                print(f"❌ No asset status available for asset '{asset_data['name']}'. Skipping.")
                continue
            
            asset = Asset(
                id=uuid.uuid4(),
                tenant_id=tenant.id,
                name=asset_data["name"],
                tag=asset_data["tag"],
                description=asset_data["description"],
                asset_type_id=asset_type.id,
                manufacturer_id=manufacturer.id if manufacturer else None,
                location_id=location.id if location else None,
                site_id=location.site_id if location else None,
                area_id=location.area_id if location else None,
                model=asset_data["model"],
                serial_number=asset_data["serial_number"],
                status_id=asset_status.id,
                risk_score=asset_data["risk_score"],
                business_criticality=asset_data["business_criticality"],
                remote_access_type=asset_data["remote_access_type"],
                physical_access_ease=asset_data["physical_access_ease"],
                installation_date=datetime.now() - timedelta(days=random.randint(30, 365))
            )
            db.add(asset)
            assets.append(asset)
            print(f"✅ Created asset: {asset.name}")
        else:
            assets.append(existing_asset)
    
    db.commit()
    
    # Create demo interfaces for assets
    interfaces_data = [
        {"asset": "PLC Controller A1", "name": "Ethernet Port 1", "ip_address": "192.168.1.10", "mac_address": "00:1B:44:11:3A:B7", "type": "Ethernet", "protocols": ["Ethernet/IP"]},
        {"asset": "PLC Controller A1", "name": "Serial Port 1", "ip_address": None, "mac_address": None, "type": "Serial", "protocols": ["Modbus RTU"]},
        {"asset": "HMI Display A1", "name": "Ethernet Port 1", "ip_address": "192.168.1.11", "mac_address": "00:1B:44:11:3A:B8", "type": "Ethernet", "protocols": ["Ethernet/IP"]},
        {"asset": "PLC Controller B1", "name": "Ethernet Port 1", "ip_address": "192.168.1.12", "mac_address": "00:1B:44:11:3A:B9", "type": "Ethernet", "protocols": ["Ethernet/IP"]},
        {"asset": "Quality Control Robot", "name": "Ethernet Port 1", "ip_address": "192.168.1.13", "mac_address": "00:1B:44:11:3A:BA", "type": "Ethernet", "protocols": ["Ethernet/IP"]},
        {"asset": "Network Switch A", "name": "Port 1", "ip_address": "192.168.1.1", "mac_address": "00:1B:44:11:3A:BB", "type": "Ethernet", "protocols": ["Ethernet"]},
        {"asset": "Network Switch A", "name": "Port 2", "ip_address": "192.168.1.1", "mac_address": "00:1B:44:11:3A:BC", "type": "Ethernet", "protocols": ["Ethernet"]},
        {"asset": "Temperature Sensor Array", "name": "Analog Output", "ip_address": None, "mac_address": None, "type": "Analog", "protocols": ["4-20mA"]},
        {"asset": "Production Server", "name": "Ethernet Port 1", "ip_address": "192.168.1.100", "mac_address": "00:1B:44:11:3A:BD", "type": "Ethernet", "protocols": ["Ethernet"]},
        {"asset": "Safety System Controller", "name": "Safety Network", "ip_address": "192.168.2.10", "mac_address": "00:1B:44:11:3A:BE", "type": "Safety", "protocols": ["SafetyNet"]}
    ]
    
    interfaces = []
    for interface_data in interfaces_data:
        # Find the asset for this interface
        asset = next((a for a in assets if a.name == interface_data["asset"]), None)
        if asset:
            existing_interface = db.query(AssetInterface).filter_by(
                name=interface_data["name"], 
                asset_id=asset.id
            ).first()
            
            if not existing_interface:
                interface = AssetInterface(
                    id=uuid.uuid4(),
                    tenant_id=tenant.id,
                    asset_id=asset.id,
                    name=interface_data["name"],
                    ip_address=interface_data["ip_address"],
                    mac_address=interface_data["mac_address"],
                    type=interface_data["type"],
                    protocols=interface_data["protocols"]
                )
                db.add(interface)
                interfaces.append(interface)
                print(f"✅ Created interface: {interface.name} for {asset.name}")
            else:
                interfaces.append(existing_interface)
    
    db.commit()
    
    # Create demo connections between assets
    connections_data = [
        {"parent": "PLC Controller A1", "child": "HMI Display A1", "connection_type": "Ethernet/IP", "description": "Control communication"},
        {"parent": "PLC Controller A1", "child": "Network Switch A", "connection_type": "Ethernet", "description": "Network connectivity"},
        {"parent": "Quality Control Robot", "child": "PLC Controller A1", "connection_type": "Ethernet/IP", "description": "Robot control"},
        {"parent": "Production Server", "child": "Network Switch A", "connection_type": "Ethernet", "description": "Data collection"},
        {"parent": "Safety System Controller", "child": "PLC Controller A1", "connection_type": "SafetyNet", "description": "Safety monitoring"}
    ]
    
    connections = []
    for connection_data in connections_data:
        # Find the parent and child assets
        parent_asset = next((a for a in assets if a.name == connection_data["parent"]), None)
        child_asset = next((a for a in assets if a.name == connection_data["child"]), None)
        
        if parent_asset and child_asset:
            existing_connection = db.query(AssetConnection).filter_by(
                parent_asset_id=parent_asset.id,
                child_asset_id=child_asset.id
            ).first()
            
            if not existing_connection:
                connection = AssetConnection(
                    id=uuid.uuid4(),
                    tenant_id=tenant.id,
                    parent_asset_id=parent_asset.id,
                    child_asset_id=child_asset.id,
                    connection_type=connection_data["connection_type"],
                    description=connection_data["description"]
                )
                db.add(connection)
                connections.append(connection)
                print(f"✅ Created connection: {parent_asset.name} → {child_asset.name}")
            else:
                connections.append(existing_connection)
    
    db.commit()
    
    print(f"\n🎉 Demo data seeding completed successfully!")
    print(f"📊 Created/Found:")
    print(f"   • {len(sites)} Sites")
    print(f"   • {len(areas)} Areas")
    print(f"   • {len(locations)} Locations")
    print(f"   • {len(manufacturers)} Manufacturers")
    print(f"   • {len(suppliers)} Suppliers")
    print(f"   • {len(contacts)} Contacts")
    print(f"   • {len(assets)} Assets")
    print(f"   • {len(interfaces)} Interfaces")
    print(f"   • {len(connections)} Connections")
    
    db.close()


if __name__ == "__main__":
    seed_demo_data() 