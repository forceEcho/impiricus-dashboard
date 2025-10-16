from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import  select

from app.api.deps import SessionDep
from app.models import Message, ClassificationRule, RuleKeyword, ClassMessage, RuleCreateRequest

router = APIRouter(prefix="/classify")


@router.post("/{message_id}", response_model=ClassMessage)
async def classify_message(
    *, session: SessionDep, message_id: int
) -> Any:
    """
    Classify message.
    """
    message = session.get(Message, message_id)
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    

    statement=( 
        select(ClassificationRule)
        .join(RuleKeyword, RuleKeyword.rule_id == ClassificationRule.id)
        .where(RuleKeyword.keyword==message.topic)
    )
    classRule= session.exec(statement).first()
    if classRule:
        res=classRule.name
        if classRule.action:
            res+= " " + classRule.action
        if classRule.requires_append:
            res += " " + classRule.requires_append
    else:
        res="No classification rule found"
    
    
    return_message=ClassMessage(message=res)

    return return_message

#Not needed except for testing purposes
@router.post("/rule/", response_model=ClassificationRule)
async def classification_add(
    *, session: SessionDep, rule_in: RuleCreateRequest
) -> Any:  
    rule = ClassificationRule(  
        id=rule_in.id,  
        name=rule_in.name,  
        action=rule_in.action,  
        requires_append=rule_in.requires_append,  
    )  
    session.add(rule)  
   
    for kw in rule_in.keywords_any:  
        keyword_entry = RuleKeyword(  
            keyword=kw,  
            rule_id=rule_in.id  
        )  
        session.add(keyword_entry)  
  
    session.commit()

    return rule