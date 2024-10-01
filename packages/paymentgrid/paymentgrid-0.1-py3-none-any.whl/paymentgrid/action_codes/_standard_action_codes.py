class _StandardActionCodes:
    """
    Private class holding standard credit card action codes.
    Meant to be used internally by card-specific classes.
    """
    standard_codes = {
        "00": "Approved and completed successfully",
        "05": "Do not honor",
        "12": "Invalid transaction",
    }

    @classmethod
    def get_standard_description(cls, action_code: str) -> str:
        return cls.standard_codes.get(action_code, "Unknown action code")
