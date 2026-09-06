# -*- coding: utf-8 -*-
"""跟进序列管理器 - 3-5封跟进邮件，第1/4/8/15天节奏"""
from typing import Dict, List
from src.config import FOLLOWUP_SEQUENCE


class FollowupSequence:
    """多轮跟进序列管理器"""

    def __init__(self):
        self.sequence = FOLLOWUP_SEQUENCE

    def get_plan(self, lead_id: str) -> List[Dict]:
        """获取完整跟进计划"""
        plan = []
        for i, step in enumerate(self.sequence):
            plan.append({
                "step": i + 1,
                "day": step["day"],
                "angle": step["angle"],
                "subject_prefix": step["subject_prefix"],
                "status": "pending",
                "lead_id": lead_id,
            })
        return plan

    def get_next_step(self, completed_steps: int) -> Dict:
        """获取下一个待执行的跟进步骤"""
        if completed_steps >= len(self.sequence):
            return {"step": -1, "angle": "完成", "message": "跟进序列已完成"}
        return self.sequence[completed_steps]

    def should_followup(self, days_since_last: int, completed_steps: int) -> bool:
        """判断是否应该执行下一次跟进"""
        if completed_steps >= len(self.sequence):
            return False
        next_day = self.sequence[completed_steps]["day"]
        return days_since_last >= next_day
