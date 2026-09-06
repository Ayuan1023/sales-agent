# -*- coding: utf-8 -*-
"""智能销售Agent - 核心编排器"""
from typing import Dict, List, Optional
from src.agent.lead_enricher import LeadEnricher
from src.agent.lead_scorer import LeadScorer
from src.agent.email_generator import EmailGenerator
from src.agent.followup_sequence import FollowupSequence
from src.agent.reply_handler import ReplyHandler
from src.agent.meeting_scheduler import MeetingScheduler
from src.agent.crm_sync import CRMSync
from src.agent.roi_dashboard import ROIDashboard


class SalesAgent:
    """智能销售Agent编排器"""

    def __init__(self):
        self.enricher = LeadEnricher()
        self.scorer = LeadScorer()
        self.email_gen = EmailGenerator()
        self.sequence = FollowupSequence()
        self.reply_handler = ReplyHandler()
        self.scheduler = MeetingScheduler()
        self.crm = CRMSync()
        self.dashboard = ROIDashboard(self.crm)
        self.lead_states: Dict[str, Dict] = {}

    def process_new_lead(self, company_name: str, contact_name: str = "") -> Dict:
        """处理新线索：富集→评分→生成首封邮件→写入CRM"""
        # 1. 线索富集
        enriched = self.enricher.enrich(company_name, contact_name)
        # 2. 线索评分
        score = self.scorer.score(enriched)
        enriched["score"] = score
        # 3. 写入CRM
        lead_id = self.crm.upsert_lead(enriched, score)
        enriched["id"] = lead_id
        # 4. 生成首封邮件
        email = self.email_gen.generate(enriched, "价值点")
        # 5. 记录沟通
        self.crm.add_communication(lead_id, "email", email["subject"], email["body"], "outbound")
        # 6. 状态跟踪
        self.lead_states[lead_id] = {
            "lead": enriched, "score": score,
            "followup_step": 0, "emails_sent": 1,
            "replies_received": 0, "status": "contacted",
        }
        return {
            "lead_id": lead_id,
            "enriched": enriched,
            "score": score,
            "first_email": email,
            "followup_plan": self.sequence.get_plan(lead_id),
        }

    def handle_reply(self, lead_id: str, reply_text: str) -> Dict:
        """处理客户回复：分类→自动响应→更新状态"""
        # 1. 分类回复
        classification = self.reply_handler.classify(reply_text)
        # 2. 记录回复
        self.crm.add_communication(lead_id, "email", "Re: 客户回复", reply_text, "inbound", classification["reply_type"])
        # 3. 更新状态
        state = self.lead_states.get(lead_id, {"followup_step": 0, "emails_sent": 0})
        state["replies_received"] = state.get("replies_received", 0) + 1
        # 4. 根据类型处理
        result = {"classification": classification, "auto_response": classification["auto_response"]}
        if classification["reply_type"] == "interested":
            # 推荐会议时间
            slots = self.scheduler.recommend_slots(3)
            result["recommended_slots"] = slots
            result["action"] = "提议会议"
            self.crm.update_lead_status(lead_id, "interested")
        elif classification["reply_type"] == "questioning":
            # 自动回复FAQ
            result["action"] = "自动回复FAQ"
            self.crm.add_communication(lead_id, "email", "Re: 问题解答", classification["auto_response"], "outbound")
        elif classification["reply_type"] == "rejected":
            result["action"] = "礼貌结束"
            self.crm.update_lead_status(lead_id, "rejected")
        else:
            result["action"] = "延迟跟进"
            self.crm.update_lead_status(lead_id, "pending")
        self.lead_states[lead_id] = state
        return result

    def schedule_meeting(self, lead_id: str, slot_id: str) -> Dict:
        """预约会议"""
        state = self.lead_states.get(lead_id, {})
        lead_name = state.get("lead", {}).get("decision_maker", {}).get("name", "客户")
        meeting = self.scheduler.schedule(lead_id, slot_id, lead_name)
        self.crm.update_lead_status(lead_id, "meeting_scheduled")
        self.crm.add_communication(lead_id, "meeting", "会议预约", f"已预约{meeting['scheduled_time']}", "system")
        return meeting

    def send_followup(self, lead_id: str) -> Dict:
        """发送下一封跟进邮件"""
        state = self.lead_states.get(lead_id)
        if not state:
            return {"error": "线索不存在"}
        step = state.get("followup_step", 0)
        next_step = self.sequence.get_next_step(step)
        if step >= len(self.sequence.sequence):
            return {"message": "跟进序列已完成"}
        email = self.email_gen.generate(state["lead"], next_step["angle"])
        self.crm.add_communication(lead_id, "email", email["subject"], email["body"], "outbound")
        state["followup_step"] = step + 1
        state["emails_sent"] = state.get("emails_sent", 0) + 1
        return {"email": email, "step": step + 1, "angle": next_step["angle"]}

    def get_roi_stats(self) -> Dict:
        return self.dashboard.get_stats()

    def get_leads(self, grade: str = None) -> List[Dict]:
        return self.crm.get_leads(grade)

    def get_lead_detail(self, lead_id: str) -> Dict:
        comms = self.crm.get_communications(lead_id)
        state = self.lead_states.get(lead_id, {})
        return {"lead_id": lead_id, "state": state, "communications": comms}
