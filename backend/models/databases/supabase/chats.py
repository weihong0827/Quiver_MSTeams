from typing import Optional
from uuid import UUID

from models.databases.repository import Repository
from pydantic import BaseModel
from models.chats import CreateChatWithConvoProperties


class CreateChatHistory(BaseModel):
    chat_id: UUID
    user_message: str
    assistant: str
    prompt_id: Optional[UUID]
    brain_id: Optional[UUID]


class Chats(Repository):
    def __init__(self, supabase_client):
        self.db = supabase_client

    def create_chat(self, new_chat):
        response = self.db.table("chats").insert(new_chat).execute()
        return response

    def get_chat_by_id(self, chat_id: str):
        response = (
            self.db.from_("chats")
            .select("*")
            .filter("chat_id", "eq", chat_id)
            .execute()
        )
        return response

    def get_chat_history(self, chat_id: str):
        reponse = (
            self.db.from_("chat_history")
            .select("*")
            .filter("chat_id", "eq", chat_id)
            .order("message_time", desc=False)  # Add the ORDER BY clause
            .execute()
        )

        return reponse

    def get_user_chats(self, user_id: str):
        response = (
            self.db.from_("chats")
            .select("chat_id,user_id,creation_time,chat_name")
            .filter("user_id", "eq", user_id)
            .order("creation_time", desc=False)
            .execute()
        )
        return response

    def update_chat_history(self, chat_history: CreateChatHistory):
        response = (
            self.db.table("chat_history")
            .insert(
                {
                    "chat_id": str(chat_history.chat_id),
                    "user_message": chat_history.user_message,
                    "assistant": chat_history.assistant,
                    "prompt_id": str(chat_history.prompt_id)
                    if chat_history.prompt_id
                    else None,
                    "brain_id": str(chat_history.brain_id)
                    if chat_history.brain_id
                    else None,
                }
            )
            .execute()
        )

        return response

    def update_chat(self, chat_id, updates):
        response = (
            self.db.table("chats").update(updates).match({"chat_id": chat_id}).execute()
        )

        return response

    def update_message_by_id(self, message_id, updates):
        response = (
            self.db.table("chat_history")
            .update(updates)
            .match({"message_id": message_id})
            .execute()
        )

        return response

    def get_chat_details(self, chat_id):
        response = (
            self.db.from_("chats")
            .select("*")
            .filter("chat_id", "eq", chat_id)
            .execute()
        )
        return response

    def delete_chat(self, chat_id):
        self.db.table("chats").delete().match({"chat_id": chat_id}).execute()

    def delete_chat_history(self, chat_id):
        self.db.table("chat_history").delete().match({"chat_id": chat_id}).execute()

    def get_chat_by_conversation(self, conversation_id: str):
        response = (
            self.db.from_("chats_teams_conversation")
            .select("*")
            .filter("conversation_id", "eq", conversation_id)
            .execute()
        )
        return response

    def create_chat_by_conversation(
        self, user_id, chat_data: CreateChatWithConvoProperties
    ):
        # Insert a new row into the chats table
        new_chat = {
            "user_id": str(user_id),
            "chat_name": chat_data.name,
        }
        insert_response = self.db.table("chats").insert(new_chat).execute()

        conversation_link = {
            "brain_id": str(chat_data.brain_id),
            "conversation_id": chat_data.conversation_id,
            "chat_id": insert_response.data[0]["chat_id"],
        }
        insert_response = (
            self.db.table("chats_teams_conversation")
            .insert(conversation_link)
            .execute()
        )
        return insert_response
