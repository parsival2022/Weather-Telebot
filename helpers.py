from models import User

# class that performing varios checking 
# for instance the current user`s session stage 
class Checker:
    def __init__(self, mode: list):
        self.mode = mode

    def check_stage(self, msg):
        id = msg.from_user.id
        user = User.select().where(User.user_id == id).get()
        return True if user.stage in self.mode else False
    
    @classmethod
    def simple_check(cls, member, list):
        return True if member in list else False
    
# function that returns current user from database and id from message
def get_user_and_id(msg):
    id = msg.from_user.id
    user = User.select().where(User.user_id == id).get()
    return id, user
