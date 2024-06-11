from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from orm.database import get_db
import orm.schemas as schemas
import orm.crud as crud
from pydantic import BaseModel, field_validator
from typing import List
from bs4 import BeautifulSoup
from tools.review import review_text
from typing import Optional
from tools.check_user import authorize


router = APIRouter()

class BadgeBase(BaseModel):
    badgeName: str
    badgeDesc: str
    badgeColor: str
    badgeUrl: str

class BadgeShow(BadgeBase):
    badgeId: int
    badgeCreaterId: int
    badgeCost: int

def get_badge_from_db_badge(db_badge):
    badge = {}
    badge['badgeName'] = db_badge.short_name
    badge['badgeDesc'] = db_badge.full_name
    badge['badgeColor'] = db_badge.background_color
    badge['badgeUrl'] = db_badge.icon_url
    badge['badgeId'] = db_badge.id
    badge['badgeCreaterId'] = db_badge.creater_id
    badge['badgeCost'] = db_badge.cost
    return badge

@router.post("/getBadges")
def get_all_badges(db: Session = Depends(get_db)):
    badges = []
    db_badges = crud.get_badges(db)
    for db_badge in db_badges:
        badges.append(BadgeShow(**get_badge_from_db_badge(db_badge)))
    return {"response": "success", "badges": badges}

class BadgeId(BaseModel):
    badgeId: int

class UserId(BaseModel):
    userId: int

@router.post("/getBadgesByUserId")
def get_badges_by_user_id(user_id: UserId, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(db, user_id.userId)
    if db_user == None:
        return {"response": "error", "description": "No corresponding user ID exists"}
    badges = []
    for db_badge in db_user.badges:
        badges.append(BadgeShow(**get_badge_from_db_badge(db_badge)))
    return {"response": "success", "badges": badges}

@router.post("/buyBadge")
def buy_badge(badge_id: BadgeId, current_user: Optional[dict] = Depends(authorize), db: Session = Depends(get_db)):
    if current_user == None:
        return {"response": "error", "description": "Please login first"}
    db_badge = crud.get_badge_by_id(db, badge_id.badgeId)
    if db_badge == None:
        return {"response": "error", "description": "No corresponding badge ID exists"}
    if crud.get_user_badge_by_id(db, current_user['uid'], badge_id.badgeId) != None:
        return {"response": "error", "description": "You already have this badge"}
    db_user = crud.get_user_by_id(db, current_user['uid'])
    if db_user.privilege == 0 and db_user.coin < db_badge.cost:
        return {"response": "error", "description": "You didn't have enough coin."}
    if crud.buy_badge(db, db_user, db_badge):
        return {"response": "success"}
    else:
        return {"response": "error", "description": ""}

@router.post("/uploadBadge")
def upload_badge(badge: BadgeBase, current_user: Optional[dict] = Depends(authorize), db: Session = Depends(get_db)):
    if current_user == None:
        return {"response": "error", "description": "Please login first"}
    db_badge = crud.create_badge(db, creater_id=current_user['uid'],
                      short_name=badge.badgeName,
                      full_name=badge.badgeDesc,
                      background_color=badge.badgeColor,
                      icon_url=badge.badgeUrl)
    if db_badge != None:
        return {"response": "success"}
    else:
        return {"response": "error", "description": ""}

@router.post("/refundBadge")
def refund_badge(badge_id: BadgeId, current_user: Optional[dict] = Depends(authorize), db: Session = Depends(get_db)):
    if current_user == None:
        return {"response": "error", "description": "Please login first"}
    if crud.get_user_badge_by_id(db, current_user['uid'], badge_id.badgeId) == None:
        return {"response": "error", "description": "You didn't have this badge"}
    if crud.refund_user_badge_by_id(db, current_user['uid'], badge_id.badgeId):
        return {"response": "success"}
    else:
        return {"response": "error", "description": ""}