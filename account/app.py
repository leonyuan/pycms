import web
from pycms.account.view import signup, login, logout


urls = (
    '/signup', signup,
    '/login', login,
    '/logout', logout,
)

app_account = web.application(urls, locals())
