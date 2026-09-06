# -*- coding: utf-8 -*-
"""ROI Dashboard - 实时统计线索数/触达数/回复率/预约数/转化率/ROI"""
from typing import Dict
import sqlite3


class ROIDashboard:
    """ROI统计面板"""

    def __init__(self, crm):
        self.crm = crm

    def get_stats(self) -> Dict:
        """获取实时统计数据"""
        conn = sqlite3.connect(self.crm.db_path)
        c = conn.cursor()

        # 线索统计
        c.execute("SELECT COUNT(*) FROM leads")
        total_leads = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM leads WHERE grade='A'")
        grade_a = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM leads WHERE grade='B'")
        grade_b = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM leads WHERE grade='C'")
        grade_c = c.fetchone()[0]

        # 沟通统计
        c.execute("SELECT COUNT(*) FROM communications WHERE direction='outbound'")
        total_outreach = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM communications WHERE direction='inbound'")
        total_replies = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM communications WHERE reply_type='interested'")
        interested = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM communications WHERE reply_type='rejected'")
        rejected = c.fetchone()[0]

        # 转化统计
        c.execute("SELECT COUNT(*) FROM leads WHERE status='converted'")
        converted = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM leads WHERE status='meeting_scheduled'")
        meetings = c.fetchone()[0]

        conn.close()

        reply_rate = (total_replies / total_outreach * 100) if total_outreach > 0 else 0
        conversion_rate = (converted / total_leads * 100) if total_leads > 0 else 0
        meeting_rate = (meetings / total_leads * 100) if total_leads > 0 else 0

        # ROI估算（模拟）
        cost_per_lead = 2.5  # 元/条
        total_cost = total_leads * cost_per_lead
        avg_deal_value = 50000  # 元
        estimated_revenue = converted * avg_deal_value
        roi = (estimated_revenue / total_cost) if total_cost > 0 else 0

        return {
            "total_leads": total_leads,
            "grade_distribution": {"A": grade_a, "B": grade_b, "C": grade_c},
            "total_outreach": total_outreach,
            "total_replies": total_replies,
            "reply_rate": round(reply_rate, 1),
            "interested_count": interested,
            "rejected_count": rejected,
            "meetings_scheduled": meetings,
            "meeting_rate": round(meeting_rate, 1),
            "converted": converted,
            "conversion_rate": round(conversion_rate, 1),
            "cost_estimation": {
                "cost_per_lead": cost_per_lead,
                "total_cost": total_cost,
                "avg_deal_value": avg_deal_value,
                "estimated_revenue": estimated_revenue,
                "roi_multiple": round(roi, 1),
            },
        }
