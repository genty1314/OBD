#!/usr/bin/env Python
# coding: utf-8
#由sqlacodegen生成
#sqlacodegen --noviews --noconstraints --noindexes --outfile ./db.py mysql://root:root@localhost:3306/OBD  
#由于sqlacodegen无法识别外键，需要手动设置见t_role_has_authority和t_role_has_manager
#为方便使用，添加了部分代码

#import中添加了create_engine, ForeignKey, sessionmaker和DATABASE_CONNCT_SEETING
import datetime
from sqlalchemy import Column, DateTime, Integer, String, Table, text, create_engine, ForeignKey, and_, or_
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from methods.statics import DATABASE_CONNCT_SEETING as DCS

Base = declarative_base()
def column_dict(self): #去除
    model_dict = dict(self.__dict__)
    del model_dict['_sa_instance_state']
    for u in model_dict:
        if isinstance(model_dict[u],datetime.datetime): #datetime.datetime类型装换为str
            model_dict[u] = model_dict[u].strftime("%Y-%m-%d %H:%M:%S")
    return model_dict
Base.column_dict = column_dict
metadata = Base.metadata


class Authority(Base):
    __tablename__ = 'authority'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    codename = Column(String(100), nullable=False)

    roles = relationship('Role', secondary='role_has_authority')


class Manager(Base):
    __tablename__ = 'manager'

    id = Column(Integer, primary_key=True)
    email = Column(String(255), nullable=False)
    managername = Column(String(150), nullable=False)
    password = Column(String(128), nullable=False)
    profilephoto = Column(String(255), nullable=False, server_default=text("'images/default_profile_photo.png'"))
    is_active = Column(Integer, nullable=False, server_default=text("'0'"))
    level = Column(Integer, nullable=False, server_default=text("'1'"))
    create_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    last_login = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))

    roles = relationship('Role', secondary='role_has_manager')

class Obdnote(Base):
    __tablename__ = 'obdnote'

    id = Column(Integer, primary_key=True)
    obd_code = Column(String(255), nullable=False)
    note_category = Column(Integer, nullable=False, server_default=text("'1'"))
    note = Column(String(255), nullable=False)
    pic1_path = Column(String(255), nullable=False)
    pic2_path = Column(String(255), nullable=False)
    pic3_path = Column(String(255), nullable=False)

class Picture(Base):
    __tablename__ = 'picture'

    id = Column(Integer, primary_key=True)
    code = Column(String(255))
    name = Column(String(255))
    address = Column(String(255))
    GPS = Column(String(255))
    port_direction = Column(Integer)
    zero_port_pos = Column(Integer)
    port_sort = Column(Integer)
    picture_path = Column(String(255), nullable=False)
    confirmed_picture_path = Column(String(255))
    ports_occupy = Column(String(255))
    is_correct = Column(Integer, server_default=text("'1'"))
    uncorrect_msg = Column(String(255))
    create_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(DateTime)
    user_id = Column(Integer)
    manager_id = Column(Integer)


class Role(Base):
    __tablename__ = 'role'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    content = Column(String(255), nullable=False)


t_role_has_authority = Table(
    'role_has_authority', metadata,
    # Column('role_id', Integer, primary_key=True, nullable=False),    #原代码
    # Column('authority_id', Integer, primary_key=True, nullable=False)#原代码
    Column('role_id', Integer, ForeignKey("role.id")),                 #修改代码
    Column('authority_id', Integer, ForeignKey("authority.id"))        #修改代码
)


t_role_has_manager = Table(
    'role_has_manager', metadata,
    # Column('role_id', Integer, primary_key=True, nullable=False),     #源代码
    # Column('manager_id', Integer, primary_key=True, nullable=False)   #源代码
    Column('role_id', Integer, ForeignKey("role.id")),                  #修改代码
    Column('manager_id', Integer, ForeignKey("manager.id"))             #修改代码
)


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    email = Column(String(255), nullable=False)
    username = Column(String(150), nullable=False)
    password = Column(String(128), nullable=False)
    profilephoto = Column(String(255), nullable=False, server_default=text("'images/default_profile_photo.png'"))
    is_active = Column(Integer, nullable=False, server_default=text("'0'"))
    create_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    last_login = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))

class ZeroPortPo(Base):
    __tablename__ = 'zero_port_pos'

    id = Column(Integer, primary_key=True)
    post = Column(String(255), nullable=False)

db = create_engine(DCS)  #添加
session = sessionmaker(bind=db)#添加