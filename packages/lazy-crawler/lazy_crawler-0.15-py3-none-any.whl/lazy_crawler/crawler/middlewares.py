# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from lazy_crawler.lib.user_agent import get_user_agent
import time
from scrapy.exceptions import IgnoreRequest
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message


class CrawlerSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


"""Set User-Agent header per spider or use a default value from settings"""


class RandomUserAgentMiddleware(object):
    """This middleware allows spiders to override the user_agent"""

    def __init__(self, user_agent=""):
        self.user_agent = get_user_agent("random")

    @classmethod
    def from_crawler(cls, crawler):
        o = cls(crawler.settings["USER_AGENT"])
        crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
        return o

    def spider_opened(self, spider):
        self.user_agent = getattr(spider, "user_agent", self.user_agent)

    def process_request(self, request, spider):
        if self.user_agent:
            request.headers.setdefault(b"User-Agent", self.user_agent)


# you can find list of user-agent in https://www.useragentstring.com/pages/useragentstring.php


class CustomRetryMiddleware(RetryMiddleware):
    def __init__(self, settings):
        super().__init__(settings)
        self.ignore_status_codes = [430, 503]
        self.retry_interval_map = {430: 240, 503: 480}

    def process_response(self, request, response, spider):
        if response.status in self.ignore_status_codes:
            self.logger.info(
                f"Ignoring response {response.url} with status code {response.status}"
            )
            time.sleep(self.retry_interval_map[response.status])
            return self._retry_request(
                request, response=response, reason=response_status_message(response)
            )

        return response

    def process_exception(self, request, exception, spider):
        if isinstance(exception, self.EXCEPTIONS_TO_RETRY) and not isinstance(
            exception, IgnoreRequest
        ):
            return self._retry_request(request, reason=str(exception), spider=spider)
        raise exception

    def _retry_request(self, request, response=None, reason=None, spider=None):
        retryreq = request.copy()
        retryreq.meta["retry_times"] = request.meta.get("retry_times", 0) + 1
        retryreq.dont_filter = True
        return retryreq
