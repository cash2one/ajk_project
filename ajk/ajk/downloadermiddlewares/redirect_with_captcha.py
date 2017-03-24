import logging
import random
import re
from six.moves.urllib.parse import urljoin
from scrapy.http import FormRequest,Request
from scrapy.downloadermiddlewares.redirect import RedirectMiddleware
from scrapy.utils.python import to_native_str
from scrapy.exceptions import IgnoreRequest, NotConfigured

logger = logging.getLogger(__name__)

class ajk_Redirect(RedirectMiddleware):
    """Handle redirection of requests based on response status and meta-refresh html tag"""

    def process_response(self, request, response, spider):
        #To determine whether the status code in the definition of the yuan ancestral
        #and in conjunction with the corresponding URL to record to error.txt
        if response.status in (302, 403, 404, 429, 500, 503):
            error = 'status:  (' + str(response.status) + ')  ' + request.url + '\n'
            file_text = open('error.txt', 'a+')
            file_text.write(error)
            file_text.close()

        if (request.meta.get('dont_redirect', False) or
                response.status in getattr(spider, 'handle_httpstatus_list', []) or
                response.status in request.meta.get('handle_httpstatus_list', []) or
                request.meta.get('handle_httpstatus_all', False)):
            return response

        allowed_status = (301, 302, 303, 307)
        if 'Location' not in response.headers or response.status not in allowed_status:
            return response

        

        # HTTP header is ascii or latin1, redirected url will be percent-encoded utf-8
        location = to_native_str(response.headers['location'].decode('latin1'))#latin1 西欧的一种编码格式基于ascill

        redirected_url = urljoin(request.url, location)# 构造一个新的URL

        if response.status in (301, 307) or request.method == 'HEAD':# 这为什么没有状态码302
            redirected = request.replace(url=redirected_url)
            return self._redirect(redirected, request, spider, response.status)

        # redirected url has two kinds of redirected url if it related to captcha input
        # the first type of url has captcha string in it
        # the second type of url has not, and is the objective url which we care more about
        if re.search('captcha',redirected_url):
            redirected = self._redirect_request_using_post(request,redirected_url)
            # 含有captcha的重定向URL
        else:
            redirected = self._redirect_request_using_get(request,redirected_url)

        return self._redirect(redirected, request, spider, response.status)

    def _redirect_request_using_post(self, request, redirect_url):
        # post with capcha, this function is not defaulted
        formdatapair = {
                        '败船假亮':'52f7011ddf5789684b0a83fada50cbc0',
                        'qzv4':'c87c56bfee54471460afb3d5b6ff010b',
                        '2TcQ':'2cf211764d36bb2def0311884eb509e7',
                        '伟季训控':'7490b1844f245a22a7078fb74fc5815c',
                        '9bvD':'a8165d8d48836bab686d8fef538fda0f',
                        '相由压员':'c68b4fca3fff4babb94d90a9608e8649',
                        '值美态黄':'c86399d1b0a80013cd5c92ff7f392fe9',
                        '准斤角降':'7df04c874ce7238b69e51f4b3e89998c',
                        '交权且儿':'720a3e646b15f55fd6601d6a5f816621',
                        '关点育重':'a53168ec54b800023608521572fe650d',
                        'f5xt':'458ba14ad20bf92b21d36d37ab9ef2e3',
                        'uBTy':'7c99727445d43197eaa07d375d46d2c1',
                        '3P4G':'ec3d0e0e8aefd610423dae216a3a2410',
                        'WqsI':'dadeb56ab3f3b74de8c727654b5b40af',
                        '为们地个':'5cf6ed27a5c0c9d50a4814b4b686d7c7'
                        }
        randomKey = random.choice(list(formdatapair.keys()))
        redirected = FormRequest(url=redirect_url, 
                                meta=request.meta,
                                headers=request.headers,
                                callback=request.callback,
                                formdata={'code':randomKey,'submit':'提交'},
                                cookies={ 'ajk_boostup_captcha':formdatapair[randomKey]},
                                body='')
                                # callback：shield
        request.dont_filter=True #禁用过滤
        redirected.meta.pop('proxy_need_change',None)
        redirected.headers.pop('Content-Type', None)
        redirected.headers.pop('Content-Length', None)
        return redirected
        #pop针对的是列表和字典对象

    def _redirect_request_using_get(self, request, redirect_url):
        redirected = Request(url=redirect_url,
                             method='GET',
                             meta=request.meta,
                             callback=request.callback,
                             headers=request.headers,
                             body='')
        request.dont_filter=True
        redirected.meta.pop('proxy_need_change',None)
        redirected.headers.pop('Content-Type', None)
        redirected.headers.pop('Content-Length', None)
        return redirected

    def _redirect(self, redirected, request, spider, reason):
        ttl = request.meta.setdefault('redirect_ttl', self.max_redirect_times)#最大的重定向次数
        redirects = request.meta.get('redirect_times', 0) + 1

        if ttl and redirects <= self.max_redirect_times:
            redirected.meta['redirect_times'] = redirects
            redirected.meta['redirect_ttl'] = ttl - 1
            redirected.meta['redirect_urls'] = request.meta.get('redirect_urls', []) + \
                [request.url]
            # if it has only two layers of redirects, we get rid of the third or more
            if redirected.meta['redirect_urls'].__len__()>2:
                redirected.meta['redirect_urls'].clear()
            redirected.dont_filter = request.dont_filter
            redirected.priority = request.priority + self.priority_adjust
            
            logger.debug("Redirecting (%(reason)s) to %(redirected)s from %(request)s",
                         {'reason': reason, 'redirected': redirected, 'request': request},
                         extra={'spider': spider})
            return redirected
        else:
            logger.debug("Discarding %(request)s: max redirections reached",
                         {'request': request}, extra={'spider': spider})
            raise IgnoreRequest("max redirections reached")