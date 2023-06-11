from models import User

# checking the session stage of current user 
def check_stage(msg):
    id = msg.from_user.id
    user = User.select().where(User.user_id == id).get()
    return True if user.stage == 'get_weather' or user.stage == 'get_forecast' else False

