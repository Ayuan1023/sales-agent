# -*- coding: utf-8 -*-
"""API请求/响应模型 - Pydantic V2"""
from pydantic import BaseModel, Field
from typing import List, Dict, Optional


class LeadRequest(BaseModel):
    company_name: str = Field(..., description="公司名称")
    contact_name: str = Field(default="", description="联系人姓名")
    model_config = {"json_schema_extra": {"example": {"company_name": "字节跳动", "contact_name": "张总"}}}


class ReplyRequest(BaseModel):
    lead_id: str
    reply_text: str


class MeetingRequest(BaseModel):
    lead_id: str
    slot_id: str = "slot_1"


class HealthResponse(BaseModel):
    status: str
    version: str = "1.0.0"
    modules: Dict[str, bool]
