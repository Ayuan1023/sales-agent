# -*- coding: utf-8 -*-
"""智能销售Agent - 评测脚本"""
import sys, os, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from src.agent.agent import SalesAgent

TEST_SCENARIOS = [
    {"id": 1, "type": "新线索富集", "action": "new_lead", "company": "阿里巴巴", "contact": "张总"},
    {"id": 2, "type": "新线索富集", "action": "new_lead", "company": "腾讯科技", "contact": "李总"},
    {"id": 3, "type": "线索评分", "action": "new_lead", "company": "字节跳动", "contact": "王总"},
    {"id": 4, "type": "邮件生成", "action": "new_lead", "company": "美团点评", "contact": "赵总"},
    {"id": 5, "type": "回复-感兴趣", "action": "reply", "reply": "我很感兴趣，我们可以聊聊价格和方案"},
    {"id": 6, "type": "回复-拒绝", "action": "reply", "reply": "不需要，谢谢，我们已经有供应商了"},
    {"id": 7, "type": "回复-待定", "action": "reply", "reply": "我考虑一下，后续再联系"},
    {"id": 8, "type": "回复-问问题", "action": "reply", "reply": "你们的产品价格是多少？支持哪些功能？"},
    {"id": 9, "type": "会议预约", "action": "meeting", "slot": "slot_1"},
    {"id": 10, "type": "跟进邮件", "action": "followup"},
    {"id": 11, "type": "多轮跟进", "action": "followup_multi", "count": 3},
    {"id": 12, "type": "CRM同步", "action": "check_crm"},
    {"id": 13, "type": "ROI统计", "action": "check_roi"},
]

def run_evaluation():
    agent = SalesAgent()
    results = []
    lead_id = None

    for scenario in TEST_SCENARIOS:
        start = time.time()
        success = True
        detail = ""
        try:
            if scenario["action"] == "new_lead":
                r = agent.process_new_lead(scenario["company"], scenario.get("contact", ""))
                lead_id = r["lead_id"]
                detail = f"评分:{r['score']['total_score']} 等级:{r['score']['grade']}"
            elif scenario["action"] == "reply":
                if not lead_id:
                    r = agent.process_new_lead("测试公司" + str(scenario["id"]))
                    lead_id = r["lead_id"]
                r = agent.handle_reply(lead_id, scenario["reply"])
                detail = f"类型:{r['classification']['reply_label']} 置信度:{r['classification']['confidence']}"
            elif scenario["action"] == "meeting":
                if not lead_id:
                    r = agent.process_new_lead("会议测试公司")
                    lead_id = r["lead_id"]
                r = agent.schedule_meeting(lead_id, scenario["slot"])
                detail = f"时间:{r['scheduled_time']}"
            elif scenario["action"] == "followup":
                if not lead_id:
                    r = agent.process_new_lead("跟进测试公司")
                    lead_id = r["lead_id"]
                r = agent.send_followup(lead_id)
                detail = f"第{r['step']}封 角度:{r['angle']}"
            elif scenario["action"] == "followup_multi":
                for i in range(scenario["count"]):
                    r = agent.send_followup(lead_id)
                detail = f"已发送{scenario['count']}封跟进"
            elif scenario["action"] == "check_crm":
                leads = agent.get_leads()
                detail = f"CRM中{len(leads)}条线索"
            elif scenario["action"] == "check_roi":
                stats = agent.get_roi_stats()
                detail = f"线索:{stats['total_leads']} 回复率:{stats['reply_rate']}%"
        except Exception as e:
            success = False
            detail = f"错误: {str(e)}"

        latency = (time.time() - start) * 1000
        results.append({"id": scenario["id"], "type": scenario["type"], "success": success,
                        "latency_ms": round(latency, 2), "detail": detail})

    passed = sum(1 for r in results if r["success"])
    accuracy = passed / len(results)
    avg_latency = sum(r["latency_ms"] for r in results) / len(results)

    report = {"total_scenarios": len(results), "passed": passed, "accuracy": round(accuracy, 4),
              "avg_latency_ms": round(avg_latency, 2), "results": results}
    os.makedirs("eval_output", exist_ok=True)
    with open("eval_output/evaluation_results.json", "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"=== 智能销售Agent 评测结果 ===")
    print(f"测试场景: {len(results)}")
    print(f"通过率: {accuracy*100:.1f}% ({passed}/{len(results)})")
    print(f"平均延迟: {avg_latency:.2f}ms")
    for r in results:
        print(f"  [{'PASS' if r['success'] else 'FAIL'}] #{r['id']} {r['type']}: {r['detail']} ({r['latency_ms']}ms)")
    return report

if __name__ == "__main__":
    run_evaluation()
