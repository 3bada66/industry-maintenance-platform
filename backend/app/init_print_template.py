# init_print_template.py

import os
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.print_template import PrintTemplate
from app.crud.print_templates import get_default_templates
from uuid import UUID


def init_default_templates(tenant_id=None):
    session: Session = SessionLocal()
    try:
        default_templates = get_default_templates()
        for template_data in default_templates:
            # Check if it already exists for key and tenant
            query = session.query(PrintTemplate).filter_by(key=template_data["key"])
            if tenant_id:
                query = query.filter_by(tenant_id=tenant_id)
            existing = query.first()
            if existing:
                # print(f"Template '{template_data['key']}' already exists.")
                continue
            template = PrintTemplate(
                key=template_data["key"],
                name=template_data["name"],
                name_translations=template_data.get("name_translations", {}),
                description=template_data["description"],
                description_translations=template_data.get(
                    "description_translations", {}
                ),
                icon=template_data["icon"],
                component=template_data["component"],
                options=template_data["options"],
                tenant_id=tenant_id,
            )
            session.add(template)
            # print(f"Template '{template_data['key']}' created.")
        session.commit()
        # print("All default templates have been created or already exist.")
    except Exception as e:
        # print("Error creating templates:", e)
        session.rollback()
    finally:
        session.close()


if __name__ == "__main__":
    # If you need multi-tenant support, you can pass a tenant_id here
    # Example: init_default_templates(tenant_id=UUID('...'))
    init_default_templates()
