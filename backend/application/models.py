from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy
import functools
from flask import request, jsonify
import jwt
from .config import Config
engine = None
Base = declarative_base()
db = SQLAlchemy()
from datetime import datetime

class User(db.Model):
    __tablename__='user'
    user_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    user_name=db.Column(db.String(100),unique=True,nullable=False)
    #name=db.Column(db.String(100),nullable=False)
    password=db.Column(db.String(100),nullable=False)
    email_id=db.Column(db.String(100),unique=True,nullable=False)
    role_id=db.Column(db.Integer,nullable=False) #Role ID for students is 1, for Support Agents is 2, Admins is 3, Manager is 4.
    responses = db.relationship('Response', back_populates='responder', lazy='subquery')
    tickets = db.relationship('Ticket',  back_populates='creator', lazy='subquery')
    discourse_username = db.Column(db.String(100),nullable=False)
    discourse_userid = db.Column(db.Integer,nullable=False)

class Response(db.Model):
    response_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.ticket_id'))
    response = db.Column(db.String(200), nullable=False) 
    responder_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    response_timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    parent_list = db.relationship('Ticket',back_populates='responses', lazy='subquery')
    responder = db.relationship('User', back_populates='responses', lazy='subquery')

class Ticket(db.Model):
    ticket_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    title=db.Column(db.String(100),nullable=False)
    description=db.Column(db.String(100),nullable=False)
    creation_date=db.Column(db.DateTime,nullable=False, default=datetime.utcnow())
    creator_id=db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    number_of_upvotes=db.Column(db.Integer,default=0)
    is_read=db.Column(db.Boolean,nullable=False)
    is_open=db.Column(db.Boolean,nullable=False)
    is_offensive=db.Column(db.Boolean,nullable=False)
    is_FAQ=db.Column(db.Boolean,nullable=False)
    responses = db.relationship('Response', back_populates='parent_list', lazy='subquery')
    creator = db.relationship('User', back_populates='tickets', lazy='subquery')
    rating = db.Column(db.Integer)
    
    discourse_post_id = db.Column(db.Integer, nullable=False)
    
    
 
class DiscoursePost(db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    avatar_template = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.String(100), nullable=False)
    raw = db.Column(db.String(100), nullable=False)
    cooked = db.Column(db.String(100), nullable=False)
    post_number = db.Column(db.Integer, nullable=False)
    post_type = db.Column(db.Integer, nullable=False)
    updated_at = db.Column(db.String(100), nullable=False)
    reply_count = db.Column(db.Integer, nullable=False)
    reply_to_post_number = db.Column(db.String(100), nullable=False)
    quote_count = db.Column(db.Integer, nullable=False)
    incoming_link_count = db.Column(db.Integer, nullable=False)
    reads = db.Column(db.Integer, nullable=False)
    readers_count = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Integer, nullable=False)
    yours = db.Column(db.Boolean, nullable=False)
    topic_id = db.Column(db.Integer, nullable=False)
    topic_slug = db.Column(db.String(100), nullable=False)
    display_username = db.Column(db.String(100), nullable=False)
    primary_group_name = db.Column(db.String(100), nullable=False)
    flair_name = db.Column(db.String(100), nullable=False)
    flair_url = db.Column(db.String(100), nullable=False)
    flair_bg_color = db.Column(db.String(100), nullable=False)
    flair_color = db.Column(db.String(100), nullable=False)
    flair_group_id = db.Column(db.String(100), nullable=False)
    version = db.Column(db.Integer, nullable=False)
    can_edit = db.Column(db.Boolean, nullable=False)
    can_delete = db.Column(db.Boolean, nullable=False)
    can_recover = db.Column(db.Boolean, nullable=False)
    can_see_hidden_post = db.Column(db.Boolean, nullable=False)
    can_wiki = db.Column(db.Boolean, nullable=False)
    user_title = db.Column(db.String(100), nullable=False)
    bookmarked = db.Column(db.Boolean, nullable=False)
    moderator = db.Column(db.Boolean, nullable=False)
    admin = db.Column(db.Boolean, nullable=False)
    staff = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    draft_sequence = db.Column(db.Integer, nullable=False)
    hidden = db.Column(db.Boolean, nullable=False)
    trust_level = db.Column(db.Integer, nullable=False)
    deleted_at = db.Column(db.String(100), nullable=False)
    user_deleted = db.Column(db.Boolean, nullable=False)
    edit_reason = db.Column(db.String(100), nullable=False)
    can_view_edit_history = db.Column(db.Boolean, nullable=False)
    wiki = db.Column(db.Boolean, nullable=False)
    reviewable_id = db.Column(db.String(100), nullable=False)
    reviewable_score_count = db.Column(db.Integer, nullable=False)
    reviewable_score_pending_count = db.Column(db.Integer, nullable=False)
    mentioned_users = db.Column(db.String(100), nullable=False)

class Category(db.Model):
    category = db.Column(db.String(50), primary_key=True)

class FAQ(db.Model):
    ticket_id = db.Column(db.Integer,db.ForeignKey('ticket.ticket_id'),primary_key=True)
    category = db.Column(db.String, db.ForeignKey('category.category'))
    is_approved = db.Column(db.Boolean,nullable=False)
    ticket = db.relationship('Ticket', backref='faq')

class Flagged_Post(db.Model):
      ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.ticket_id'), primary_key = True)
      flagger_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
      creator_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
      is_approved = db.Column(db.Boolean, nullable = False, default = False)
      is_rejected = db.Column(db.Boolean, nullable = False, default = False)

def token_required(function):
	@functools.wraps(function)
	def loggedin(*args,**kwargs):
		auth_token=None
		try:
			auth_token = request.headers['secret_authtoken']
		
		except:
			return jsonify({"status":'unsuccessful, missing the authtoken'})
		
		try: 
			output = jwt.decode(auth_token,Config.SECRET_KEY,algorithms=["HS256"])
			#print(output)
			user = User.query.filter_by(user_id = output["user_id"]).first()
		except:
			return jsonify({"status":"failure, your token details do not match"})
		
		return function(user,*args,**kwargs)
	return loggedin
