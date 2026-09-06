# -*- coding: utf-8 -*-
"""智能销售Agent - 单元测试"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from src.agent.lead_enricher import LeadEnricher
from src.agent.lead_scorer import LeadScorer
from src.agent.email_generator import EmailGenerator
from src.agent.followup_sequence import FollowupSequence
from src.agent.reply_handler import ReplyHandler
from src.agent.meeting_scheduler import MeetingScheduler
from src.agent.crm_sync import CRMSync
from src.agent.agent import SalesAgent


@pytest.fixture
def agent():
    return SalesAgent()


class TestLeadEnricher:
    def test_enrich_returns_all_fields(self):
        e = LeadEnricher()
        result = e.enrich("测试公司", "张总")
        assert result["company_name"] == "测试公司"
        assert "industry" in result
        assert "company_size" in result
        assert "funding_stage" in result
        assert "tech_stack" in result
        assert "decision_maker" in result
        assert "模拟数据" in result["data_source"]

    def test_deterministic(self):
        e = LeadEnricher()
        r1 = e.enrich("同一公司")
        r2 = e.enrich("同一公司")
        assert r1["industry"] == r2["industry"]


class TestLeadScorer:
    def test_score_returns_grade(self):
        s = LeadScorer()
        lead = {"company_size": "1000人以上", "industry": "互联网",
                "funding_stage": "已上市", "tech_stack": ["Python", "Go"],
                "decision_maker": {"seniority": "C-level"}}
        result = s.score(lead)
        assert result["total_score"] > 0
        assert result["grade"] in ["A", "B", "C"]
        assert len(result["dimension_scores"]) == 6

    def test_high_grade_for_strong_lead(self):
        s = LeadScorer()
        lead = {"company_size": "1000人以上", "industry": "互联网",
                "funding_stage": "已上市", "tech_stack": ["Python"],
                "decision_maker": {"seniority": "C-level"}, "engagement_score": 100}
        result = s.score(lead)
        assert result["grade"] == "A"


class TestEmailGenerator:
    def test_generate_personalized(self):
        g = EmailGenerator()
        lead = {"company_name": "测试公司", "industry": "互联网",
                "company_size": "50-200人", "tech_stack": ["Python"],
                "decision_maker": {"name": "张总", "title": "CTO"}}
        email = g.generate(lead, "价值点")
        assert "测试公司" in email["body"]
        assert "互联网" in email["body"]
        assert email["personalized"] is True

    def test_all_angles(self):
        g = EmailGenerator()
        lead = {"company_name": "X", "industry": "金融", "company_size": "大",
                "tech_stack": ["Java"], "decision_maker": {"name": "李", "title": "CEO"}}
        for angle in ["价值点", "客户案例", "紧迫感", "最后通知"]:
            email = g.generate(lead, angle)
            assert len(email["body"]) > 50


class TestFollowupSequence:
    def test_plan_has_4_steps(self):
        f = FollowupSequence()
        plan = f.get_plan("lead1")
        assert len(plan) == 4
        assert plan[0]["day"] == 1
        assert plan[3]["day"] == 15

    def test_should_followup(self):
        f = FollowupSequence()
        assert f.should_followup(1, 0) is True
        assert f.should_followup(0, 0) is False
        assert f.should_followup(20, 4) is False


class TestReplyHandler:
    def test_classify_interested(self):
        h = ReplyHandler()
        result = h.classify("我很感兴趣，我们可以聊聊价格")
        assert result["reply_type"] == "interested"

    def test_classify_rejected(self):
        h = ReplyHandler()
        result = h.classify("不需要，谢谢")
        assert result["reply_type"] == "rejected"

    def test_classify_questioning(self):
        h = ReplyHandler()
        result = h.classify("你们的产品价格是多少？")
        assert result["reply_type"] == "questioning"

    def test_auto_response_not_empty(self):
        h = ReplyHandler()
        for t in ["感兴趣", "不需要", "考虑一下", "多少钱"]:
            r = h.classify(t)
            assert len(r["auto_response"]) > 0


class TestMeetingScheduler:
    def test_recommend_slots(self):
        s = MeetingScheduler()
        slots = s.recommend_slots(3)
        assert len(slots) == 3
        assert "time" in slots[0]

    def test_schedule(self):
        s = MeetingScheduler()
        meeting = s.schedule("lead1", "slot_1", "张总")
        assert meeting["status"] == "scheduled"
        assert "calendar_invite" in meeting


class TestCRM:
    def test_upsert_and_get(self, tmp_path):
        db = str(tmp_path / "test.db")
        crm = CRMSync(db)
        lead = {"company_name": "测试", "industry": "互联网", "company_size": "大",
                "funding_stage": "A轮", "tech_stack": ["Python"],
                "decision_maker": {"name": "张"}}
        score = {"total_score": 85.0, "grade": "A"}
        lid = crm.upsert_lead(lead, score)
        leads = crm.get_leads()
        assert len(leads) >= 1
        assert leads[0]["company_name"] == "测试"

    def test_communication(self, tmp_path):
        db = str(tmp_path / "test2.db")
        crm = CRMSync(db)
        cid = crm.add_communication("lead1", "email", "主题", "内容", "outbound")
        assert cid
        comms = crm.get_communications("lead1")
        assert len(comms) == 1


class TestAgent:
    def test_full_pipeline(self, agent, tmp_path):
        # 新线索
        result = agent.process_new_lead("测试科技公司", "王总")
        assert result["lead_id"]
        assert result["score"]["grade"] in ["A", "B", "C"]
        assert "first_email" in result
        # 处理回复
        reply_result = agent.handle_reply(result["lead_id"], "我很感兴趣，可以聊聊")
        assert reply_result["classification"]["reply_type"] == "interested"
        assert "recommended_slots" in reply_result
        # 预约会议
        meeting = agent.schedule_meeting(result["lead_id"], "slot_1")
        assert meeting["status"] == "scheduled"
        # ROI统计
        stats = agent.get_roi_stats()
        assert stats["total_leads"] >= 1

    def test_followup(self, agent):
        result = agent.process_new_lead("跟进测试公司")
        f = agent.send_followup(result["lead_id"])
        assert "email" in f
        assert f["step"] == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
