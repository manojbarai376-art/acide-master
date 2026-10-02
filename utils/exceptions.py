# Custom Exceptions for ACID Master

class AcidMasterException(Exception):
    """बेस एक्सेप्शन क्लास"""
    pass

class ScraperError(AcidMasterException):
    """जब स्क्रैपर वेबसाइट से डेटा फेच करने में फेल हो जाए"""
    pass

class DatabaseError(AcidMasterException):
    """जब डेटाबेस में रीड या राइट करने में दिक्कत आए"""
    pass

print("Exceptions script ready!")