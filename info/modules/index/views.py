from info import redis_store
from . import index_blu



@index_blu.route("/")
def index():
    redis_store.set("class","30000")
    redis_store.set("nnnnn", "888888888888888888")
    return 'iiiiiiiiii'