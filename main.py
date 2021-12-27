import web
from handle import Handle

urls = (
    '/bot', 'Handle',
)



if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()



