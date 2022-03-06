from w3lib.http import basic_auth_header
from scrapy.utils.project import get_project_settings


class ProxyMiddleware(object):
    def process_request(self, request, spider):
        settings = get_project_settings()
        request.meta['proxy'] = settings.get('PROXY_HOST') + ':' + settings.get('PROXY_PORT')
        request.headers["Proxy-Authorization"] = basic_auth_header(settings.get('PROXY_USER'), settings.get('PROXY_PASSWORD'))
        spider.log('Proxy : %s' % request.meta['proxy'])
