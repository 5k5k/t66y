import urllib2
import re
import urlparse

from Craw import Craw


def download(url, user_agent='morladim', num_reties=2):
    print "Downloading: ", url
    headers = {'User-agent': user_agent}
    request = urllib2.Request(url, headers=headers)
    try:
        html = urllib2.urlopen(request).read()
    except urllib2.URLError as e:
        print "Download error ", e.reason
        html = None
        if num_reties > 0:
            if hasattr(e, "code") and 500 <= e.code < 600:
                return download(url, user_agent, num_reties - 1)
    return html


def link_crawler(seed_url, link_regex,max_depth = 50):
    print 'seed_url ', seed_url
    crawl_queue = [seed_url]
    seen = set(crawl_queue)
    while crawl_queue:
        url = crawl_queue.pop()
        print 'url ', url
        html = download(url)
        # print "html ", html
        for link in get_links(html):
            if re.match(link_regex, link):
                link = urlparse.urljoin(seed_url, link)
                if link not in seen:
                    seen.add(link)
                    crawl_queue.append(link)


def get_links(html):
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    print 'html ', html
    return webpage_regex.findall(html)


# link_crawler('http://www.maritech.cn', '/(index|view)')

# delay = 1000
# throttle = Craw(delay)
# throttle.wait()





link_crawler('https://example.webscraping.com', '/(index|view)')
