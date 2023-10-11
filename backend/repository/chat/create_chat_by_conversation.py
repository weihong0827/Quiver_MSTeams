from uuid import UUID
from repository.chat.get_chat_by_conversation import ChatConvResponse
from models.chats import CreateChatWithConvoProperties
from models import get_supabase_db


def create_chat_by_conversation(
    user_id: UUID, chat_data: CreateChatWithConvoProperties
) -> ChatConvResponse:
    supabase = get_supabase_db()
    insert_response = supabase.create_chat_by_conversation(user_id, chat_data)
    return insert_response.data[0]
