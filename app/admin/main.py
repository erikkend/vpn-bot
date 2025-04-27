from fastapi import FastAPI
from sqladmin import Admin, ModelView

from app.database import engine

from app.models.user import User
from app.models.order import Order
from app.models.server import Server
from app.models.vpn_key import VPNKey
from app.models.subscription import Subscription


app = FastAPI()
admin = Admin(app, engine)


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.username]
    
class ServerAdmin(ModelView, model=Server):
    column_list = [Server.id, Server.server_ip, Server.title, Server.is_active]

admin.add_view(UserAdmin)
admin.add_view(ServerAdmin)
