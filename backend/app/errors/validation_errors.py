"""
Custom validation error exceptions for standardized error codes
"""

class ValidationError(Exception):
    """Base validation error class"""
    def __init__(self, error_code: str, field: str = ""):
        self.error_code = error_code
        self.field = field
        super().__init__(f"Validation error: {error_code}")


class InvalidVATNumberError(ValidationError):
    """Invalid VAT number format"""
    def __init__(self, field: str = "vat_number"):
        super().__init__("INVALID_VAT_NUMBER", field)


class InvalidTaxCodeError(ValidationError):
    """Invalid tax code format"""
    def __init__(self, field: str = "tax_code"):
        super().__init__("INVALID_TAX_CODE", field)


class InvalidURLError(ValidationError):
    """Invalid URL format"""
    def __init__(self, field: str = "website"):
        super().__init__("INVALID_URL", field)


class InvalidPhoneError(ValidationError):
    """Invalid phone number format"""
    def __init__(self, field: str = "phone"):
        super().__init__("INVALID_PHONE", field)


class InvalidEmailError(ValidationError):
    """Invalid email format"""
    def __init__(self, field: str = "email"):
        super().__init__("INVALID_EMAIL", field)


class InvalidIPAddressError(ValidationError):
    """Invalid IP address format"""
    def __init__(self, field: str = "ip_address"):
        super().__init__("INVALID_IP_ADDRESS", field)


class InvalidMACAddressError(ValidationError):
    """Invalid MAC address format"""
    def __init__(self, field: str = "mac_address"):
        super().__init__("INVALID_MAC_ADDRESS", field)


class InvalidSerialNumberError(ValidationError):
    """Invalid serial number format"""
    def __init__(self, field: str = "serial_number"):
        super().__init__("INVALID_SERIAL_NUMBER", field)


class InvalidDateError(ValidationError):
    """Invalid date format"""
    def __init__(self, field: str = "date"):
        super().__init__("INVALID_DATE", field)


class InvalidTimeError(ValidationError):
    """Invalid time format"""
    def __init__(self, field: str = "time"):
        super().__init__("INVALID_TIME", field)


class InvalidPortError(ValidationError):
    """Invalid port number"""
    def __init__(self, field: str = "port"):
        super().__init__("INVALID_PORT", field)


class InvalidVLANError(ValidationError):
    """Invalid VLAN number"""
    def __init__(self, field: str = "vlan"):
        super().__init__("INVALID_VLAN", field)


class InvalidImpactValueError(ValidationError):
    """Invalid impact value"""
    def __init__(self, field: str = "impact_value"):
        super().__init__("INVALID_IMPACT_VALUE", field)


class InvalidPurdueLevelError(ValidationError):
    """Invalid Purdue level"""
    def __init__(self, field: str = "purdue_level"):
        super().__init__("INVALID_PURDUE_LEVEL", field)


class InvalidRiskScoreError(ValidationError):
    """Invalid risk score"""
    def __init__(self, field: str = "risk_score"):
        super().__init__("INVALID_RISK_SCORE", field)


class InvalidBusinessCriticalityError(ValidationError):
    """Invalid business criticality"""
    def __init__(self, field: str = "business_criticality"):
        super().__init__("INVALID_BUSINESS_CRITICALITY", field)


class InvalidRemoteAccessTypeError(ValidationError):
    """Invalid remote access type"""
    def __init__(self, field: str = "remote_access_type"):
        super().__init__("INVALID_REMOTE_ACCESS_TYPE", field)


class InvalidPhysicalAccessEaseError(ValidationError):
    """Invalid physical access ease"""
    def __init__(self, field: str = "physical_access_ease"):
        super().__init__("INVALID_PHYSICAL_ACCESS_EASE", field)


class InvalidTenantSlugError(ValidationError):
    """Invalid tenant slug format"""
    def __init__(self, field: str = "tenant_slug"):
        super().__init__("INVALID_TENANT_SLUG", field)


class InvalidPasswordError(ValidationError):
    """Invalid password format"""
    def __init__(self, field: str = "password"):
        super().__init__("INVALID_PASSWORD", field) 