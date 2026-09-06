# 智能销售 Agent — 架构设计

## 系统架构图
```mermaid
graph TB
    subgraph 线索流水线
        Enrich[线索富集<br/>行业/规模/融资/技术栈/决策人]
        Score[线索评分<br/>A/B/C级多维度加权]
    end
    subgraph 沟通自动化
        Gen[个性化邮件生成<br/>LLM非模板生成]
        Sequence[跟进序列<br/>第1/4/8/15天]
        Reply[回复处理<br/>感兴趣/拒绝/待定/问问题]
        Meeting[会议预约<br/>推荐时间+日历邀请]
    end
    subgraph CRM同步
        SQLite[(SQLite模拟CRM)]
        Sync[同步日志]
    end
    subgraph ROI分析
        Dashboard[ROI Dashboard<br/>线索数/触达数/回复率/转化率]
    end
    Enrich --> Score --> Gen --> Sequence --> Reply --> Meeting
    Reply -->|感兴趣| Meeting
    Reply -->|问问题| Gen
    Enrich -.-> SQLite
    Gen -.-> SQLite
    Reply -.-> SQLite
    SQLite --> Dashboard
```

## 核心模块
1. 线索富集：模拟收集公司信息（标注模拟数据）
2. 线索评分：多维度加权A/B/C级评分
3. 个性化邮件生成：基于客户具体情况生成
4. 多轮跟进序列：3-5封邮件，不同角度
5. 邮件回复处理：自动分类+自动响应
6. 会议预约：推荐时间+模拟日历
7. CRM同步：SQLite存储+同步日志
8. ROI Dashboard：实时统计
