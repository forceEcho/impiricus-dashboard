from fastapi.testclient import TestClient
from sqlmodel import Session
import csv
from app.models import Physician, Message, ClassificationRule, RuleKeyword
from datetime import datetime
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent
MESSAGE_DATA_CSV=BASE_DIR/"messages.csv"
PHYSICIAN_DATA_CSV=BASE_DIR/"physicians.csv"
RULES_DATA_JSON=BASE_DIR/"compliance_policies.json"

def test_read_physicians(
    client: TestClient, db: Session
) -> None:
    with open(PHYSICIAN_DATA_CSV, newline='') as csvfile:
        reader = csv.DictReader(csvfile)  
        for row in reader:
            physician = Physician(
                physician_id=int(row['physician_id']),
                npi=row['npi'],
                first_name=row['first_name'],
                last_name=row['last_name'],
                specialty=row['specialty'],
                state=row['state'],
                consent_opt_in=bool(row['consent_opt_in'].lower()),
                preferred_channel=row['preferred_channel']              
            )
            db.add(physician)
    db.commit()
    response = client.get(
        f"/physicians/?state=NJ&specialty=Cardiology",
    )
    assert response.status_code == 200
    content = response.json()
    assert content["count"] == 1
    assert content["data"][0]["first_name"] == "Sam"
    assert content["data"][0]["last_name"] == "Patel"


def test_read_messages(
    client: TestClient, db: Session
) -> None:
    with open(MESSAGE_DATA_CSV, newline='') as csvfile:  
        reader = csv.DictReader(csvfile)  
        for row in reader:
            latency_str=row.get('response_latency_sec',0.0 )
            if latency_str=="":
                latency_float=0.0
            else:
                latency_float=float(latency_str) 
            message = Message(
                message_id= int(row['message_id']),
                physician_id=int(row['physician_id']),
                channel=row['channel'],
                direction=row['direction'],
                timestamp=datetime.fromisoformat(row['timestamp']),
                message_text=row['message_text'],
                campaign_id=row['campaign_id'],
                topic=row['topic'],
                compliance_tag=row['compliance_tag'],
                sentiment=row['sentiment'],
                delivery_status=row['delivery_status'],
                response_latency_sec=latency_float
            )  
            db.add(message)
    db.commit()
    response = client.get(
        f"/messages/?physician=116&fromDate=2025-07-25T00:00:00&toDate=2025-07-25T23:59:59",
    )
    assert response.status_code == 200
    content = response.json()
    assert content["count"] == 1
    assert content["data"][0]["message_text"]=="Schedule a rep connect call next week." 

def test_classify_message(
    client: TestClient, db: Session
) -> None:
    with open(RULES_DATA_JSON, "r") as f:  
        rules_data = json.load(f)  
        for rule in rules_data["rules"]:
            # Insert rule  
            rule_obj = ClassificationRule(  
                id=rule["id"],  
                name=rule["name"],  
                action=rule.get("action"),  
                requires_append=rule.get("requires_append")  
            )  
            db.add(rule_obj)  
            # Insert keywords  
            for kw in rule["keywords_any"]:  
                keyword_obj = RuleKeyword(  
                    keyword=kw,  
                    rule_id=rule["id"],  
                )  
                db.add(keyword_obj)
    db.commit()
    response = client.post(
        f"/classify/10193",
    )
    assert response.status_code == 200
    content = response.json()
    assert content["message"] == "Include safety statement when mentioning dosing See PI for full safety info."