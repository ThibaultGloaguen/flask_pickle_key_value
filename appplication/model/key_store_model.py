from datetime import datetime, timedelta


class KeyStoreModel:
    def __init__(self, value, date_creation, time_to_live=None):
        self.value = value
        self.date_creation = date_creation
        self.time_to_live = time_to_live

    @property
    def is_expired(self):
        if not self.time_to_live:
            return False
        date_expiration = self.date_creation + timedelta(seconds=self.time_to_live)
        return date_expiration < datetime.now()

    def to_dict(self):
        payload_dict = {}
        payload_dict.update(self.__dict__)
        filtered_payload = {k: v.__str__() for k, v in payload_dict.items() if v is not None}
        payload_dict.clear()
        payload_dict.update(filtered_payload)

        return payload_dict
