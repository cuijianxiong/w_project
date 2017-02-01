import web

urls = (
    '/aab', 'index'
)

class index:
    def GET(self):
        #i = web.input()
        print 'handle request'
        return "He"


def my_processor(handler): 
    print 'before handling'
    result = handler() 
    print 'after handling'
    return result

def before_handle():
    print 'before'

def after_handle():
    print 'after'

app = web.application(urls, globals())

app.add_processor(web.loadhook(before_handle))
app.add_processor(web.unloadhook(after_handle))

#app.add_processor(my_processor)

if __name__ == "__main__":

    app.run()
