from models import get_supabase_db


def get_channel_brain(channel_id: str):
    supabase_db = get_supabase_db()
    return supabase_db.get_channel_brain(channel_id)
