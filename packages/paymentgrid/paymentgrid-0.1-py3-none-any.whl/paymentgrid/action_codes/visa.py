from ._standard_action_codes import _StandardActionCodes

class VisaActionCodes(_StandardActionCodes):
    def __init__(self):
        self.visa_specific_codes = {
            "00": "Approved for Visa-specific process",  # Visa-specific description
            "01": "Refer to card issuer",
        }

    def get_action_description(self, action_code: str) -> str:
        return self.visa_specific_codes.get(action_code, super().get_standard_description(action_code))

    def get_all_codes(self) -> dict:
        combined_codes = self.visa_specific_codes.copy()
        combined_codes.update(self.get_all_standard_codes())
        return combined_codes
