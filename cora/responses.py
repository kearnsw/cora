from typing import Any, Dict, List, Optional, Text
import logging

from cora.models import UserRecord
from cora.utils import convert_model_to_snake_case

logger = logging.getLogger(__name__)


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

    def most_recent(self) -> UserRecord:
        logger.debug(f"most_recent")
        if len(self.data) != 0:
            return max(self.data, key=lambda d: d.timestamp)
        else:
            return UserRecord()

