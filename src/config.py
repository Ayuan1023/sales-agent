# -*- coding: utf-8 -*-
"""智能销售Agent - 全局配置"""
from typing import Dict, List

# 线索评分维度及权重
SCORING_WEIGHTS = {
    "company_size": 0.20,
    "industry_match": 0.20,
    "funding_stage": 0.15,
    "tech_stack_match": 0.15,
    "decision_maker": 0.15,
    "engagement_signal": 0.15,
}

SCORE_GRADES = {
    "A": {"min": 80, "label": "高意向", "action": "立即跟进"},
    "B": {"min": 50, "label": "中意向", "action": "常规跟进"},
    "C": {"min": 0, "label": "低意向", "action": "培育观察"},
}

FOLLOWUP_SEQUENCE = [
    {"day": 1, "angle": "价值点", "subject_prefix": "解决方案"},
    {"day": 4, "angle": "客户案例", "subject_prefix": "成功案例"},
    {"day": 8, "angle": "紧迫感", "subject_prefix": "限时优惠"},
    {"day": 15, "angle": "最后通知", "subject_prefix": "最后机会"},
]

REPLY_TYPES = ["interested", "rejected", "pending", "questioning"]
REPLY_TYPE_LABELS = {
    "interested": "感兴趣", "rejected": "拒绝", "pending": "待定", "questioning": "问问题",
}

INDUSTRIES = ["互联网", "金融", "制造业", "教育", "医疗", "零售", "物流", "房地产"]
COMPANY_SIZES = ["10人以下", "10-50人", "50-200人", "200-500人", "500-1000人", "1000人以上"]
FUNDING_STAGES = ["未融资", "天使轮", "A轮", "B轮", "C轮", "D轮及以上", "已上市"]
TECH_STACKS = ["Python", "Java", "Go", "Node.js", "PHP", "Ruby", ".NET"]

CRM_DB_PATH = "data/crm.db"
