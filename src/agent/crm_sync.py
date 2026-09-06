# -*- coding: utf-8 -*-
"""CRM同步器 - SQLite模拟CRM，所有线索和沟通记录自动写入"""
import sqlite3
import os
from datetime import datetime
from typing import Dict, List, Optional
from src.config import CRM_DB_PATH


class CRMSync:
    """SQLite模拟CRM同步器"""

    def __init__(self, db_path: str = None):
        self.db_path = db_path or CRM_DB_PATH
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_db()

    def _init_db(self):
        """初始化数据库表"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS leads (
            id TEXT PRIMARY KEY, company_name TEXT, industry TEXT,
            company_size TEXT, funding_stage TEXT, tech_stack TEXT,
            decision_maker TEXT, score REAL, grade TEXT,
            status TEXT DEFAULT 'new', created_at TEXT, updated_at TEXT
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS communications (
            id TEXT PRIMARY KEY, lead_id TEXT, type TEXT,
            subject TEXT, body TEXT, direction TEXT,
            reply_type TEXT, created_at TEXT,
            FOREIGN KEY (lead_id) REFERENCES leads(id)
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS sync_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entity_type TEXT, entity_id TEXT, action TEXT,
            timestamp TEXT, details TEXT
        )''')
        conn.commit()
        conn.close()

    def upsert_lead(self, lead: Dict, score: Dict) -> str:
        """写入/更新线索"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        now = datetime.now().isoformat()
        lead_id = lead.get("id", f"lead_{abs(hash(lead['company_name'])) % 100000}")
        c.execute('''INSERT OR REPLACE INTO leads VALUES (?,?,?,?,?,?,?,?,?,?,?,?)''',
                  (lead_id, lead["company_name"], lead["industry"], lead["company_size"],
                   lead["funding_stage"], ",".join(lead["tech_stack"]),
                   lead["decision_maker"]["name"], score["total_score"], score["grade"],
                   lead.get("status", "new"), now, now))
        self._log(c, "lead", lead_id, "upsert", f"评分:{score['total_score']} 等级:{score['grade']}")
        conn.commit()
        conn.close()
        return lead_id

    def add_communication(self, lead_id: str, comm_type: str, subject: str,
                          body: str, direction: str, reply_type: str = "") -> str:
        """写入沟通记录"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        comm_id = f"comm_{abs(hash(lead_id + subject + datetime.now().isoformat())) % 1000000}"
        now = datetime.now().isoformat()
        c.execute('''INSERT INTO communications VALUES (?,?,?,?,?,?,?,?)''',
                  (comm_id, lead_id, comm_type, subject, body[:500], direction, reply_type, now))
        self._log(c, "communication", comm_id, "create", f"类型:{comm_type} 方向:{direction}")
        conn.commit()
        conn.close()
        return comm_id

    def update_lead_status(self, lead_id: str, status: str):
        """更新线索状态"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("UPDATE leads SET status=?, updated_at=? WHERE id=?",
                  (status, datetime.now().isoformat(), lead_id))
        self._log(c, "lead", lead_id, "status_update", f"新状态:{status}")
        conn.commit()
        conn.close()

    def get_leads(self, grade: str = None) -> List[Dict]:
        """获取线索列表"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        if grade:
            c.execute("SELECT * FROM leads WHERE grade=? ORDER BY score DESC", (grade,))
        else:
            c.execute("SELECT * FROM leads ORDER BY score DESC")
        rows = [dict(r) for r in c.fetchall()]
        conn.close()
        return rows

    def get_communications(self, lead_id: str) -> List[Dict]:
        """获取线索的沟通记录"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT * FROM communications WHERE lead_id=? ORDER BY created_at", (lead_id,))
        rows = [dict(r) for r in c.fetchall()]
        conn.close()
        return rows

    def get_sync_log(self, limit: int = 20) -> List[Dict]:
        """获取同步日志"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT * FROM sync_log ORDER BY id DESC LIMIT ?", (limit,))
        rows = [dict(r) for r in c.fetchall()]
        conn.close()
        return rows

    def _log(self, cursor, entity_type: str, entity_id: str, action: str, details: str):
        cursor.execute('''INSERT INTO sync_log (entity_type, entity_id, action, timestamp, details)
                          VALUES (?,?,?,?,?)''',
                       (entity_type, entity_id, action, datetime.now().isoformat(), details))
