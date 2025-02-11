from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# User Schema
class UserSchema(BaseModel):
    user_id: str  # WhatsApp number or unique ID
    name: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

# Expense Schema
class ExpenseSchema(BaseModel):
    user_id: str
    category: str
    subcategory: Optional[str] = None  # Now optional
    description: Optional[str] = None  # Now optional
    amount: float
    date: datetime = Field(default_factory=datetime.utcnow)

# Query Schema (For logging user queries)
class QuerySchema(BaseModel):
    user_id: str
    query_text: str  # The user's raw message
    response: str  # Generated response
    timestamp: datetime = Field(default_factory=datetime.utcnow)
