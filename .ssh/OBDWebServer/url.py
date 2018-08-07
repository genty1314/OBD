#!/usr/bin/env Python
# coding=utf-8
"""
the url structure of website
"""
######  BASE   ###################################
from handlers.base import BaseHandler
from handlers.base import check_codeHandler

###### MANAGER ###################################
from handlers.manager.manager import ManagerLoginHandler
from handlers.manager.manager import ManagerLogoutHandler
from handlers.manager.manager import ManagerIndexHandler
from handlers.manager.manager import ManagerEditLevelHandler
from handlers.manager.manager import ManagerInformationHandler
from handlers.manager.manager import ManagerPicManagementHandler
from handlers.manager.manager import ManagerManagementList

from handlers.manager.manager import ManagerUserManagementHandler
from handlers.manager.manager import UserGetOBDList
from handlers.manager.manager import ManagerGetOBDList
from handlers.manager.manager import ManagerUserActiveHandler
from handlers.manager.manager import ManagerUserAddHandler
from handlers.manager.manager import ManagerUserEditHandler

from handlers.manager.manager import ManagerManagementHandler
from handlers.manager.manager import ManagerAddHandler
from handlers.manager.manager import ManagerEditHandler
from handlers.manager.manager import ManagerActiveHandler
from handlers.manager.picture import ManagerPictures
from handlers.manager.picture import ManagerPicturesEdit
from handlers.manager.picture import ManagerPicturesPatchOutput
from handlers.manager.picture import ManagerPicturesConfirm
######  USER   ###################################
from handlers.user.user import UserLoginHandler
from handlers.user.user import UserLogoutHandler
from handlers.user.user import UserInformationHandler
from handlers.user.user import UserRegisterHandler
from handlers.user.user import UserCheckEmailHandler
from handlers.user.user import UserIndexHandler
from handlers.user.user import UserOBDListHandler
from handlers.user.user import UserConfirmHandler
from handlers.user.picture import UserPictureConfirm
from handlers.user.picture import UserOBDNoteSubmit


url = [
    (r'/check_code',check_codeHandler),
    #前台url
    (r'/',UserIndexHandler),
    (r'/userlogin',UserLoginHandler),
    (r'/userlogout',UserLogoutHandler),
    (r'/userinfo',UserInformationHandler),
    (r'/userregister',UserRegisterHandler),
    (r'/check_email',UserCheckEmailHandler),

    (r'/useobdlistpage',UserOBDListHandler),


    (r'/useconfirmpage',UserConfirmHandler),    
    (r'/useconfirmpic',UserPictureConfirm),


    
    (r'/obdnote',UserOBDNoteSubmit),

    #后台url
    (r'/manager', ManagerIndexHandler),
    (r'/managerlogin', ManagerLoginHandler),
    (r'/managereditlevel', ManagerEditLevelHandler),
    (r'/managerlogout', ManagerLogoutHandler),
    (r'/managerinfo',ManagerInformationHandler),


    (r'/picmanagement',ManagerPicManagementHandler),
    (r'/managergetobdlist',ManagerGetOBDList),

    (r'/manageraddpics',ManagerPictures),
    (r'/managereditpic',ManagerPicturesEdit),
    (r'/managerpatchpic',ManagerPicturesPatchOutput),
    (r'/managerconfirmpic',ManagerPicturesConfirm),
    
    (r'/usermanagement',ManagerUserManagementHandler),
    (r'/usergetobdlist',UserGetOBDList),
    (r'/useractive',ManagerUserActiveHandler),
    (r'/useraddpage',ManagerUserAddHandler),
    (r'/usereditpage',ManagerUserEditHandler),

    (r'/managermanagement',ManagerManagementHandler),
    (r'/managermanagementgetobdlist',ManagerManagementList),
    (r'/manageractive',ManagerActiveHandler),
    (r'/manageraddpage',ManagerAddHandler),
    (r'/managereditpage',ManagerEditHandler),

    #访问错误url
    (r".*", BaseHandler),
]

