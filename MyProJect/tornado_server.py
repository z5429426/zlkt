from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from zlkt import app#这里要和zlkt.py对应
http_server = HTTPServer(WSGIContainer(app))
http_server.listen(5000) #flask默认的端口
IOLoop.instance().start()
