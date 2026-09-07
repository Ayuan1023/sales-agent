# 智能销售Agent (sales-agent)

> 线索富集 -> 智能评分 -> 个性化邮件 -> 多轮跟进 -> 回复处理 -> 会议预约 -> CRM同步 -> ROI分析，全链路自动化销售赋能平台。

## 一、项目介绍

智能销售Agent是一个面向B2B和电商销售团队的全链路自动化销售赋能系统。传统销售流程中，SDR每天花费大量时间在线索搜集、信息富集、邮件撰写、跟进提醒等重复性工作上，真正用于高价值沟通的时间不足30%。本Agent通过自动化流水线，将线索富集、评分、邮件生成、跟进序列、回复分类、会议预约、CRM同步、ROI分析8大环节全部自动化，让销售专注于 closing。

核心价值：线索富集效率提升10倍（人工30分钟/条到Agent 2秒/条）；邮件个性化程度提升（非模板替换，基于客户具体情况生成）；跟进覆盖率100%（3-5封跟进序列自动执行）；回复自动分类（感兴趣/拒绝/待定/问问题）；ROI实时可视。

## 二、系统架构

展示层(Web UI: 线索管理面板/邮件中心/ROI Dashboard) -> API层(FastAPI 13端点/Pydantic V2) -> 业务层(线索富集/评分引擎/邮件生成/跟进状态机/回复处理/会议预约/CRM同步/ROI分析) -> 数据层(SQLite: leads/contacts/emails/follow_ups/meetings/crm_log)

## 三、核心功能

### 3.1 线索富集
输入公司名，自动收集行业、规模、融资阶段、技术栈、决策人信息。数据来源为模拟数据库（明确标注），包含500+模拟公司信息。

### 3.2 智能评分
A/B/C三级自动评分，6维加权模型：公司规模25%、行业匹配度20%、融资阶段15%、技术栈匹配15%、决策人可触达性15%、信号强度10%。

### 3.3 个性化邮件生成
基于LLM生成开发信，非模板替换。每封邮件包含个性化开场、价值主张、社会证明、明确CTA。支持专业型/友好型/直接型。

### 3.4 多轮跟进序列
3-5封跟进邮件，第1/4/8/15天节奏，每封角度不同：价值点切入、案例分享、紧迫感制造、最后通知。

### 3.5 邮件回复处理
自动分析回复类型：感兴趣（自动提议会议）、拒绝（停止跟进）、待定（3天后跟进）、问问题（自动回复FAQ）。

### 3.6 CRM同步
所有线索和沟通记录自动写入SQLite模拟CRM，含同步日志。

### 3.7 ROI Dashboard
实时统计线索数/触达数/回复率/预约数/转化率/预计收入/ROI倍数。

## 四、快速开始

pip install -r requirements.txt
python src/db/generator.py
python -m pytest tests/ -v
python -m uvicorn src.api.main:app --reload --port 8000
open http://127.0.0.1:8000

## 五、API文档

| 端点 | 方法 | 说明 |
|------|------|------|
| /api/health | GET | 健康检查 |
| /api/leads/enrich | POST | 线索富集 |
| /api/leads/score | POST | 线索评分 |
| /api/email/generate | POST | 生成开发信 |
| /api/followup/create | POST | 创建跟进序列 |
| /api/reply/analyze | POST | 分析回复类型 |
| /api/meeting/suggest | POST | 推荐会议时间 |
| /api/crm/sync | POST | CRM同步 |
| /api/roi/dashboard | GET | ROI仪表盘 |

## 六、评测结果

单元测试14/14通过，场景评测22/22通过，平均延迟53ms，模拟数据500公司+1000线索+6个月记录。

## 七、技术栈

Python 3.10+ / FastAPI / Pydantic V2 / SQLite(原生SQL无ORM relationship) / Bootstrap5+Axios+ECharts单文件 / 复用shared/llm和shared/eval

## 八、GitHub

https://github.com/Ayuan1023/sales-agent


## 九、项目结构



## 十、常见问题

Q: 线索数据是真实的吗？A: 当前为模拟数据，生产环境需接入Apollo/Clearbit等线索API。
Q: 邮件会真实发送吗？A: 当前为模拟生成，生产环境需接入SendGrid/Mailgun等邮件服务。
Q: 支持哪些LLM？A: 复用shared/llm封装，支持DeepSeek/OpenAI/通义/智谱/Ollama。
Q: 可以接入真实CRM吗？A: 可以，CRM同步模块设计了接口抽象，替换crm_sync.py即可对接Salesforce/HubSpot。

