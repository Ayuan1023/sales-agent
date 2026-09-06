# -*- coding: utf-8 -*-
"""个性化邮件生成器 - 基于客户具体情况生成开发信（模板化模拟LLM生成）"""
from typing import Dict


class EmailGenerator:
    """个性化邮件生成器 - 基于线索信息生成定制化邮件"""

    def generate(self, lead: Dict, angle: str = "价值点") -> Dict:
        """
        生成个性化邮件
        angle: 价值点/客户案例/紧迫感/最后通知
        """
        company = lead["company_name"]
        industry = lead["industry"]
        dm = lead["decision_maker"]
        tech = ", ".join(lead["tech_stack"])

        subject_templates = {
            "价值点": f"{company}效率提升方案 - 针对{industry}行业",
            "客户案例": f"{industry}行业客户成功案例 - {company}参考",
            "紧迫感": f"限时：{company}专属优惠本月截止",
            "最后通知": f"最后机会：{company}合作邀请",
        }

        body_templates = {
            "价值点": f"""尊敬的{dm['name']}（{dm['title']}）：

您好！我是智能销售Agent，注意到{company}作为{industry}行业的{lead['company_size']}企业，技术栈涵盖{tech}。

我们的解决方案可以帮助{company}：
1. 提升销售效率300%，线索处理量从200条/人提升至20000条
2. 个性化邮件生成，回复率从15%提升至25%
3. 智能跟进序列，自动触达，无需人工干预

针对{industry}行业，我们已有多个成功案例。不知您本周是否有15分钟时间简要沟通？

祝商祺！
智能销售Agent""",

            "客户案例": f"""尊敬的{dm['name']}：

分享一个{industry}行业的客户成功案例：

某{lead['company_size']}的{industry}企业，使用我们的方案后：
- 线索转化率从5%提升至12%
- 销售周期缩短40%
- 单条线索成本降低60%

该客户技术栈同样包含{tech}，与{company}高度相似。我们相信类似的成果可以在{company}复现。

如需了解详细案例，欢迎回复本邮件，我将发送完整资料。

祝好！
智能销售Agent""",

            "紧迫感": f"""尊敬的{dm['name']}：

提醒您：针对{industry}行业的专属优惠本月底截止。

{company}可享受：
- 首月免费试用
- 年费8折优惠
- 专属客户成功经理一对一服务

此优惠仅限前20家{industry}企业，目前仅剩5个名额。

如{company}有意向，请在本月底前回复确认。

期待与您合作！
智能销售Agent""",

            "最后通知": f"""尊敬的{dm['name']}：

这是最后一次联系您。此前我曾向{company}介绍过我们的{industry}行业解决方案。

如果{company}目前没有相关需求，我将不再打扰。如果未来有需求，欢迎随时联系我。

感谢您的时间！

智能销售Agent
（退订请回复"退订"）""",
        }

        return {
            "subject": subject_templates.get(angle, subject_templates["价值点"]),
            "body": body_templates.get(angle, body_templates["价值点"]),
            "angle": angle,
            "personalized": True,
            "personalization_fields": ["company_name", "industry", "company_size", "tech_stack", "decision_maker"],
        }
