# -*- coding: utf-8 -*-
"""线索评分器 - 多维度加权A/B/C级评分"""
from typing import Dict, Tuple
from src.config import SCORING_WEIGHTS, SCORE_GRADES, COMPANY_SIZES, FUNDING_STAGES


class LeadScorer:
    """多维度线索评分器"""

    def score(self, lead: Dict) -> Dict:
        """对线索进行多维度评分，返回评分详情"""
        scores = {}
        # 公司规模
        size_idx = COMPANY_SIZES.index(lead["company_size"]) if lead["company_size"] in COMPANY_SIZES else 2
        scores["company_size"] = round((size_idx / (len(COMPANY_SIZES) - 1)) * 100, 1)
        # 行业匹配（互联网/金融/科技行业匹配度高）
        high_match = ["互联网", "金融", "科技"]
        scores["industry_match"] = 90 if lead["industry"] in high_match else 60
        # 融资阶段
        fund_idx = FUNDING_STAGES.index(lead["funding_stage"]) if lead["funding_stage"] in FUNDING_STAGES else 2
        scores["funding_stage"] = round((fund_idx / (len(FUNDING_STAGES) - 1)) * 100, 1)
        # 技术栈匹配（Python/Go匹配度高）
        tech_match = 100 if any(t in lead["tech_stack"] for t in ["Python", "Go"]) else 70
        scores["tech_stack_match"] = tech_match
        # 决策人级别
        seniority_scores = {"C-level": 100, "VP": 85, "Director": 70, "Manager": 50}
        scores["decision_maker"] = seniority_scores.get(lead["decision_maker"]["seniority"], 50)
        # 互动信号（新线索默认50，有回复则提升）
        scores["engagement_signal"] = lead.get("engagement_score", 50)

        # 加权总分
        total = sum(scores[k] * SCORING_WEIGHTS[k] for k in SCORING_WEIGHTS)
        total = round(total, 1)

        # 等级判定
        grade = "C"
        for g, info in SCORE_GRADES.items():
            if total >= info["min"]:
                grade = g
                break

        return {
            "total_score": total,
            "grade": grade,
            "grade_label": SCORE_GRADES[grade]["label"],
            "recommended_action": SCORE_GRADES[grade]["action"],
            "dimension_scores": scores,
            "weights": SCORING_WEIGHTS,
        }
