from datetime import datetime, timedelta


class KeyModel:
    def __init__(self, value, expiration_delta=None):
        self.date_creation = datetime.now()
        self.value = value
        self.date_expiration = None
        if expiration_delta:
            self.date_expiration = self.date_creation + timedelta(seconds=int(expiration_delta))

    def to_dict(self):
        payload_dict = {}
        payload_dict.update(self.__dict__)
        filtered_payload = {k: v.__str__() for k, v in payload_dict.items() if v is not None}
        payload_dict.clear()
        payload_dict.update(filtered_payload)

        return payload_dict
