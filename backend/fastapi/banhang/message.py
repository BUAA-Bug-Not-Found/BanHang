from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from orm.database import get_db
import orm.schemas as schemas
import orm.crud as crud
from pydantic import BaseModel
from tools.check_user import check_user
from typing import List

router = APIRouter()

class ConversationShow(BaseModel):
	user_name: str
	user_id: int
	has_unread_mesage: bool

@router.post("/getReletedUser", tags=["Message"], response_model=List[ConversationShow])
@check_user
def get_recent_message_conversation(uid: int, db: Session = Depends(get_db)):
	db_conversations = crud.get_recent_message_conversation(db, uid)
	conversations = []
	for db_conversation in db_conversations:
		conversation = {}
		conversation['user_name'] = db_conversation.guest_user.username
		conversation['user_id'] = db_conversation.guest_user.id
		conversation['has_unread_mesage'] = db_conversation.is_read
		conversations.append(ConversationShow(**conversation))
	return conversation

class MessageGet(BaseModel):
	targetUserId: int

@router.post("/getHistoryMessage", tags=["Message"], response_model=List[schemas.MessageShow])
@check_user
def get_history_message(uid: int, message_get: MessageGet, db: Session = Depends(get_db)):
	db_conversation = crud.get_conversation(db, uid, message_get.targetUserId)
	messages = []
	for db_message in db_conversation.messages:
		message = {}
		message['senderName'] = db_message.sender.username
		message['senderId'] = db_message.sender_id
		message['receiverName'] = db_message.receiver.username
		message['receiverId'] = db_message.receiver_id
		message['content'] = db_message.content
		message['time'] = db_message.create_at
		messages.append(schemas.MessageShow(**message))
	return messages

class MessageCreate(BaseModel):
	targetUserId: int
	content: str

@router.post("/sendMessage", tags=["Message"])
@check_user
def send_message(uid: int, message_create: MessageCreate, db: Session = Depends(get_db)):
	host_user_id = uid
	guest_user_id = message_create.targetUserId
	db_host_conversation = crud.get_conversation(db, host_user_id, guest_user_id)
	if (host_user_id != guest_user_id):
		db_guest_conversation = crud.get_conversation(db, guest_user_id, host_user_id)
	if db_host_conversation == None:
		db_host_conversation = crud.create_conversation(db, host_user_id, guest_user_id)
		if (host_user_id != guest_user_id):
			db_guest_conversation = crud.create_conversation(db, guest_user_id, host_user_id)
	db_message = crud.create_message(db, sender_id=host_user_id, receiver_id=guest_user_id, content=message_create.content)
	try:
		db.add(db_message)
		db.commit()
		db.refresh(db_message)
		db_host_conversation.update_at = db_message.create_at
		db_host_conversation.messages.append(db_message)
		db_host_conversation.is_read = True
		db.add(db_host_conversation)
		if (host_user_id != guest_user_id):
			db_guest_conversation.update_at = db_message.create_at
			db_guest_conversation.messages.append(db_message)
			db_guest_conversation.is_read = False
			db.add(db_guest_conversation)
		db.commit()
		db.refresh(db_host_conversation)
	except Exception as e:
		db.rollback()
		db_host_conversation = None

	if db_host_conversation == None:
		return {"status": "error"}
	else:
		return {"status": "success"}
