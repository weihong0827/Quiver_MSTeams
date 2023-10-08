from uuid import UUID

from models import get_supabase_db


def create_channel_brain(brain_id: UUID, channel_id: str):
    supabase_db = get_supabase_db()
    return supabase_db.create_channel_brain(brain_id, channel_id)
