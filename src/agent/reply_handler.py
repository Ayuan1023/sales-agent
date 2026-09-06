# -*- coding: utf-8 -*-
"""邮件回复处理器 - 自动分析回复类型并响应"""
from typing import Dict
from src.config import REPLY_TYPE_LABELS


class ReplyHandler:
    """邮件回复自动分类处理器"""

    def classify(self, reply_text: str) -> Dict:
        """
        分类回复类型：感兴趣/拒绝/待定/问问题
        基于关键词规则（LLM可用时升级为语义分类）
        """
        text = reply_text.lower()
        scores = {
            "interested": 0, "rejected": 0, "pending": 0, "questioning": 0,
        }
        # 感兴趣关键词
        interested_kw = ["感兴趣", "有兴趣", "可以", "好的", "聊聊", "沟通", "会议", "演示", "demo", "价格", "报价", "详细", "资料", "yes", "sure", "interested"]
        for kw in interested_kw:
            if kw in text:
                scores["interested"] += 1
        # 拒绝关键词
        rejected_kw = ["不需要", "不感兴趣", "拒绝", "算了", "不用", "谢谢", "no", "not interested", "stop", "退订", "unsubscribe"]
        for kw in rejected_kw:
            if kw in text:
                scores["rejected"] += 2
        # 待定关键词
        pending_kw = ["考虑", "想想", "以后", "后续", "再看", "暂时", "可能", "maybe", "later", "consider"]
        for kw in pending_kw:
            if kw in text:
                scores["pending"] += 1
        # 问问题关键词
        questioning_kw = ["什么", "怎么", "如何", "为什么", "哪里", "哪个", "多少", "?", "？", "how", "what", "why", "when", "can you", "请问"]
        for kw in questioning_kw:
            if kw in text:
                scores["questioning"] += 1
        # 取最高分
        reply_type = max(scores, key=scores.get)
        confidence = scores[reply_type] / max(sum(scores.values()), 1)

        return {
            "reply_type": reply_type,
            "reply_label": REPLY_TYPE_LABELS[reply_type],
            "confidence": round(confidence, 2),
            "scores": scores,
            "auto_response": self._get_auto_response(reply_type, reply_text),
        }

    def _get_auto_response(self, reply_type: str, original_text: str) -> str:
        """生成自动响应"""
        responses = {
            "interested": "感谢您的关注！我将为您安排一次产品演示会议。请问您本周什么时间方便？我们可以提供30分钟的在线演示。",
            "rejected": "感谢您的回复，抱歉打扰了。如果未来有相关需求，欢迎随时联系。祝您工作顺利！",
            "pending": "理解您需要时间考虑。我会在一周后再次联系您。如有任何问题，欢迎随时回复。",
            "questioning": "感谢您的提问！关于您的问题，我整理了以下信息供参考。如需更详细的解答，我们可以安排一次简短的沟通。",
        }
        return responses.get(reply_type, "")
