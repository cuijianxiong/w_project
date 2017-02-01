import web
import test_sub
urls = (
  "/blog", test_sub.app_blog,
  "/(.*)", "index"
)

class index:
    def GET(self, path):
        return "hello " + path

app = web.application(urls, locals())
def my_processor(handler): 
    print 'before handling'
    result = handler() 
    print 'after handling'
    return result

app.add_processor(my_processor)

if __name__ == "__main__":
    app.run()
