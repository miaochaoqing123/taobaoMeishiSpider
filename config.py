MONGO_URL ='localhost'
MONGO_DB = 'taobao'
MONGO_TABLE = 'product'

# 可以去看官网看源码:
"""
--disk-cache=[true|false] enables disk cache (at desktop services cache storage location, default is false). Also accepted: [yes|no].

--load-images=[true|false] load all inlined images (default is true). Also accepted: [yes|no].
"""
SERVICE_ARGS = ['--load-images=false','--disk-cache=true']