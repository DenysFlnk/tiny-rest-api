from views import get_all_users, get_user, delete_user, update_user, create_user

ROOT_URL = '/users'
USER_URL = '/users/{user_id}'

def setup_routes(app):
    app.router.add_get(ROOT_URL, get_all_users)
    app.router.add_get(USER_URL, get_user)
    app.router.add_delete(USER_URL, delete_user)
    app.router.add_put(USER_URL, update_user)
    app.router.add_post(ROOT_URL, create_user)