# app/scheduler/jobs.py
from datetime import datetime
from app.database import get_session
from app.services.maintenance import deactivate_expired_configs


async def check_and_deactivate_vpn():
    async for session in get_session():
        await deactivate_expired_configs(session)
        print(f"[{datetime.now()}] Checked for expired VPN configs.")
