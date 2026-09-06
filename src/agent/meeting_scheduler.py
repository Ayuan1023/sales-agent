# -*- coding: utf-8 -*-
"""会议预约器 - 推荐时间+模拟日历邀请+提醒"""
from typing import Dict, List
from datetime import datetime, timedelta


class MeetingScheduler:
    """会议预约管理器"""

    def __init__(self):
        self.time_slots = [
            "周一 10:00-10:30", "周一 14:00-14:30",
            "周二 10:00-10:30", "周二 15:00-15:30",
            "周三 11:00-11:30", "周三 14:00-14:30",
            "周四 10:00-10:30", "周四 16:00-16:30",
            "周五 10:00-10:30", "周五 14:00-14:30",
        ]

    def recommend_slots(self, n: int = 3) -> List[Dict]:
        """推荐可用时间段"""
        today = datetime.now()
        slots = []
        for i, slot in enumerate(self.time_slots[:n]):
            day_offset = (i // 2) + 1
            slot_date = today + timedelta(days=day_offset)
            slots.append({
                "slot_id": f"slot_{i+1}",
                "time": slot,
                "date": slot_date.strftime("%Y-%m-%d"),
                "duration": "30分钟",
                "format": "在线会议（Zoom/腾讯会议）",
            })
        return slots

    def schedule(self, lead_id: str, slot_id: str, lead_name: str) -> Dict:
        """预约会议（模拟日历邀请）"""
        slot = next((s for s in self.recommend_slots(10) if s["slot_id"] == slot_id), None)
        if not slot:
            slot = self.recommend_slots(1)[0]
        return {
            "meeting_id": f"mtg_{lead_id}_{slot_id}",
            "lead_id": lead_id,
            "lead_name": lead_name,
            "scheduled_time": f"{slot['date']} {slot['time']}",
            "duration": slot["duration"],
            "format": slot["format"],
            "calendar_invite": "已发送模拟日历邀请（.ics文件）",
            "reminder_24h": "已设置24小时前提醒",
            "reminder_1h": "已设置1小时前提醒",
            "status": "scheduled",
        }
