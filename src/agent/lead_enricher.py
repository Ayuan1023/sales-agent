# -*- coding: utf-8 -*-
"""线索富集器 - 模拟收集公司信息（明确标注模拟数据）"""
import random
import hashlib
from typing import Dict
from src.config import INDUSTRIES, COMPANY_SIZES, FUNDING_STAGES, TECH_STACKS


class LeadEnricher:
    """线索富集器 - 基于公司名模拟收集信息（数据为模拟，非真实API）"""

    def enrich(self, company_name: str, contact_name: str = "") -> Dict:
        """
        富集线索信息
        注意：返回数据为模拟数据，仅用于Demo演示
        """
        # 用公司名做种子，保证同一公司结果一致
        seed = int(hashlib.md5(company_name.encode()).hexdigest()[:8], 16)
        rng = random.Random(seed)

        industry = rng.choice(INDUSTRIES)
        size = rng.choice(COMPANY_SIZES)
        funding = rng.choice(FUNDING_STAGES)
        tech = rng.sample(TECH_STACKS, k=rng.randint(1, 3))
        employees = self._estimate_employees(size)
        revenue = self._estimate_revenue(size, funding)

        # 决策人信息
        decision_titles = ["CEO", "CTO", "VP of Engineering", "Director of IT", "Head of Operations"]
        decision_maker = {
            "name": contact_name or f"{rng.choice(['张','李','王','刘','陈'])}总",
            "title": rng.choice(decision_titles),
            "seniority": rng.choice(["C-level", "VP", "Director", "Manager"]),
        }

        return {
            "company_name": company_name,
            "industry": industry,
            "company_size": size,
            "estimated_employees": employees,
            "estimated_revenue": revenue,
            "funding_stage": funding,
            "tech_stack": tech,
            "decision_maker": decision_maker,
            "location": rng.choice(["北京", "上海", "深圳", "杭州", "广州", "成都"]),
            "data_source": "模拟数据（Demo演示用，非真实API数据）",
            "enrichment_coverage": "8/8字段已填充",
        }

    def _estimate_employees(self, size: str) -> int:
        mapping = {
            "10人以下": (5, 10), "10-50人": (10, 50), "50-200人": (50, 200),
            "200-500人": (200, 500), "500-1000人": (500, 1000), "1000人以上": (1000, 5000),
        }
        lo, hi = mapping.get(size, (10, 100))
        return random.randint(lo, hi)

    def _estimate_revenue(self, size: str, funding: str) -> str:
        base = {"10人以下": 100, "10-50人": 500, "50-200人": 2000,
                "200-500人": 8000, "500-1000人": 30000, "1000人以上": 100000}
        rev = base.get(size, 1000)
        if funding in ["B轮", "C轮", "D轮及以上", "已上市"]:
            rev *= 2
        return f"约{rev}万/年"
