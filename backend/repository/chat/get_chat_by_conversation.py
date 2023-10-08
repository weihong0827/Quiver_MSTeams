from dataclasses import dataclass
from datetime import datetime

from uuid import UUID
from models import get_supabase_db


@dataclass
class ChatConvResponse:
    chat_id: UUID
    conversation_id: str
    brain_id: UUID
    creation_time: datetime


NO_CHAT_FOUND_ERROR = "No chat found for this conversation"


def get_chat_by_conversation(conversation_id: str) -> ChatConvResponse:
    supabasedb = get_supabase_db()
    response = supabasedb.get_chat_by_conversation(conversation_id)
    if not response.data:
        raise Exception(NO_CHAT_FOUND_ERROR)
    return response.data[0]
