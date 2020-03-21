from typing import Any, Dict, List, Optional, Text
from cora.models import UserRecord
from cora.utils import convert_model_to_snake_case


class UserRecordResponse:
    def __init__(self, user_id: Text = None, data: List[UserRecord] = None):
        self.user_id: Optional[Text] = user_id
        self.data: Optional[List[UserRecord]] = data

    def load_from_model(self, m: Dict[Text, Any]):
        for k, v in convert_model_to_snake_case(m).items():
            if k == "data":
                v = [UserRecord().load_from_model(record) for record in v]
            setattr(self, k, v)
        return self
