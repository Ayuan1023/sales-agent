# 智能销售 Agent

基于AI的全链路销售自动化系统，覆盖线索富集、评分、邮件生成、跟进序列、回复处理、会议预约、CRM同步、ROI分析。

## 功能特性
- 线索富集（模拟数据，8字段）
- 6维度加权评分（A/B/C级）
- 个性化邮件生成（4种角度）
- 多轮跟进序列（第1/4/8/15天）
- 回复自动分类（感兴趣/拒绝/待定/问问题）
- 会议预约（推荐时间+日历邀请）
- CRM同步（SQLite+同步日志）
- ROI Dashboard（实时统计）

## 快速开始
\`\`\`bash
pip install -r requirements.txt
python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000
\`\`\`

## 评测结果
- 场景通过率：100% (13/13)
- 单元测试：18/18通过
- 平均延迟：172ms

## License
MIT
