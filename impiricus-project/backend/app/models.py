from typing import List
from sqlmodel import Field, SQLModel
from datetime import datetime

# Shared properties
class PhysicianBase(SQLModel):
    npi: str | None = Field(default=None, max_length=255)
    first_name: str | None = Field(default=None, max_length=255)
    last_name: str | None = Field(default=None, max_length=255)
    specialty: str = Field(min_length=1, max_length=255)
    state: str = Field(min_length=2, max_length=2)
    consent_opt_in: bool | None = Field(default=None)
    preferred_channel: str | None = Field(default=None)



# Properties to receive on item creation
class PhysicianCreate(PhysicianBase):
    pass


# Properties to receive on item update
class PhysicianUpdate(PhysicianBase):
    npi: str | None = Field(default=None, max_length=255)
    first_name: str | None = Field(default=None, max_length=255)
    last_name: str | None = Field(default=None, max_length=255)
    specialty: str | None = Field(default=None, max_length=255)
    state: str | None = Field(default=None, max_length=2)
    consent_opt_in: bool | None = Field(default=None)
    preferred_channel: str | None = Field(default=None)


# Database model, database table inferred from class name
class Physician(PhysicianBase, table=True):
    physician_id: int | None = Field(default=None, primary_key=True) 


# Properties to return via API, id is always required
class PhysicianPublic(PhysicianBase):
    physician_id: int


class PhysiciansPublic(SQLModel):
    data: list[PhysicianPublic]
    count: int

class MessageBase(SQLModel): 
    physician_id: int = Field(foreign_key="physician.physician_id", index=True)
    channel: str | None = Field(default=None, max_length=255)
    direction: str | None = Field(default=None, max_length=255)  
    message_text: str = Field(min_length=1, max_length=255)
    campaign_id: str | None = Field(default=None, max_length=255)
    topic: str = Field(min_length=1, max_length=255)
    compliance_tag: str | None = Field(default=None, max_length=255)
    sentiment: str | None = Field(default=None, max_length=255)
    delivery_status: str | None = Field(default=None, max_length=255)
    response_latency_sec: float | None = Field(default=None)

class Message(MessageBase, table=True):
    message_id: int | None = Field(default=None, primary_key=True)
    timestamp: datetime | None = Field(default_factory=datetime.utcnow, index=True)

class MessageCreate(MessageBase) :
    pass

class MessageUpdate(MessageBase) :
    physician_id: int | None = Field(default=None,foreign_key="physician.physician_id", index=True)
    channel: str | None = Field(default=None, max_length=255)
    direction: str | None = Field(default=None, max_length=255)  
    message_text: str | None= Field(default=None,max_length=255)
    campaign_id: str | None = Field(default=None, max_length=255)
    topic: str  | None = Field(default=None,max_length=255)
    compliance_tag: str | None = Field(default=None, max_length=255)
    sentiment: str | None = Field(default=None, max_length=255)
    delivery_status: str | None = Field(default=None, max_length=255)
    response_latency_sec: float | None = Field(default=None)

class MessagePublic(MessageBase) : 
    message_id: int
    timestamp: datetime

class MessagesPublic(SQLModel) :
    data: list[MessagePublic]
    count: int


class ClassificationRule(SQLModel, table=True):  
    id: str = Field(primary_key=True)  
    name: str =Field(max_length=255)
    action: str | None = Field(default=None, max_length=255)
    requires_append: str | None = Field(default=None, max_length=255) 

class ClassificationRules(SQLModel) :
    rules: List[ClassificationRule]
  
class RuleKeyword(SQLModel, table=True):  
    keyword: str = Field(primary_key=True, max_length=255)  
    rule_id: str = Field(foreign_key="classificationrule.id")  

class ClassMessage(SQLModel) :
    message: str

class RuleCreateRequest(SQLModel):  
    id: str  
    name: str  
    keywords_any: List[str]  
    action: str | None = None  
    requires_append: str | None = None  