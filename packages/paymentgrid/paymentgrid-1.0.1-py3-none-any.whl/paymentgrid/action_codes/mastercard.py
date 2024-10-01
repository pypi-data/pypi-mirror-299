from ._standard_action_codes import _StandardActionCodes

class MastercardActionCodes(_StandardActionCodes):
    def __init__(self):
        self.mastercard_specific_codes = {
            "51": "Not sufficient funds",
            "57": "Transaction not permitted to cardholder",
        }

    def get_action_description(self, action_code: str) -> str:
        return self.mastercard_specific_codes.get(action_code, super().get_standard_description(action_code))

    def get_all_codes(self) -> dict:
        combined_codes = self.mastercard_specific_codes.copy()
        combined_codes.update(self.get_all_standard_codes())
        return combined_codes
