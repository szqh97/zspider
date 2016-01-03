#!/usr/bin/env python
# -*- coding: utf-8 -*-
import httplib2

url = 'https://www.zhihu.com/people/excited-vczh'
url = 'https://www.zhihu.com/people/excited-vczh/followees'

headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Accept-Encoding': 'gzip, deflate",
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive', 
        'Cookie': '_za=345605f6-eefa-4af6-a945-f2b790d12061; _ga=GA1.2.322499337.1436092356; q_c1=4b1955e3c8aa45ba930b1f40abe7c4ca|1449306839000|1436092370000; z_c0="QUFEQTVjMGVBQUFYQUFBQVlRSlZUVGl2clZieTl6NmN1Z19JX0oxczJubWh0QmIyRGoxRjRnPT0=|1451631160|c67789a061fac4d814e558bf5e0964e398efa6e4"; __utma=51854390.322499337.1436092356.1451631139.1451637264.14; __utmz=51854390.1451637264.14.8.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/people/excited-vczh/followees; __utmv=51854390.100-1|2=registration_date=20131007=1^3=entry_date=20131007=1; _xsrf=3130d2c61e1c6d68615d5046fa9d1714; cap_id="YThhNjgyNmUxYzYxNDJkM2JmNjk1MzU5OGVhNzA5NjE=|1451631135|c1a47afe58d0fdbcba7f0f524ca913809b709b79"; __utmc=51854390',
        'Host': 'www.zhihu.com',
        'Referer': 'https://www.zhihu.com/people/szqh97/followees',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0'
        }

cookie = '_za=345605f6-eefa-4af6-a945-f2b790d12061; _ga=GA1.2.322499337.1436092356; q_c1=4b1955e3c8aa45ba930b1f40abe7c4ca|1449306839000|1436092370000; z_c0="QUFEQTVjMGVBQUFYQUFBQVlRSlZUVGl2clZieTl6NmN1Z19JX0oxczJubWh0QmIyRGoxRjRnPT0=|1451631160|c67789a061fac4d814e558bf5e0964e398efa6e4"; __utma=51854390.322499337.1436092356.1451631139.1451637264.14; __utmz=51854390.1451637264.14.8.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/people/excited-vczh/followees; __utmv=51854390.100-1|2=registration_date=20131007=1^3=entry_date=20131007=1; _xsrf=3130d2c61e1c6d68615d5046fa9d1714; cap_id="YThhNjgyNmUxYzYxNDJkM2JmNjk1MzU5OGVhNzA5NjE=|1451631135|c1a47afe58d0fdbcba7f0f524ca913809b709b79"; __utmc=51854390'
headers = {
        'Host': 'www.zhihu.com',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Referer': 'https://www.zhihu.com/people/excited-vczh/followees',
        'Cookie': cookie,
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0'
        }
#curl 'https://www.zhihu.com/people/excited-vczh/followees' -H 'Host: www.zhihu.com' -H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' -H 'Accept-Language: en-US,en;q=0.5' -H 'Accept-Encoding: gzip, deflate' -H 'Referer: https://www.zhihu.com/people/excited-vczh/followees' -H 'Cookie: _za=345605f6-eefa-4af6-a945-f2b790d12061; _ga=GA1.2.322499337.1436092356; q_c1=4b1955e3c8aa45ba930b1f40abe7c4ca|1449306839000|1436092370000; z_c0="QUFEQTVjMGVBQUFYQUFBQVlRSlZUVGl2clZieTl6NmN1Z19JX0oxczJubWh0QmIyRGoxRjRnPT0=|1451631160|c67789a061fac4d814e558bf5e0964e398efa6e4"; __utma=51854390.322499337.1436092356.1451631139.1451637264.14; __utmz=51854390.1451637264.14.8.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/people/excited-vczh/followees; __utmv=51854390.100-1|2=registration_date=20131007=1^3=entry_date=20131007=1; _xsrf=3130d2c61e1c6d68615d5046fa9d1714; cap_id="YThhNjgyNmUxYzYxNDJkM2JmNjk1MzU5OGVhNzA5NjE=|1451631135|c1a47afe58d0fdbcba7f0f524ca913809b709b79"; __utmc=51854390' -H 'Connection: keep-alive' -H 'Cache-Control: max-age=0'

    # -H 'Host: www.zhihu.com' -H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' -H 'Accept-Language: en-US,en;q=0.5' -H 'Accept-Encoding: gzip, deflate' -H 'Referer: https://www.zhihu.com/people/excited-vczh/followees' -H 'Cookie: _za=345605f6-eefa-4af6-a945-f2b790d12061; _ga=GA1.2.322499337.1436092356; q_c1=4b1955e3c8aa45ba930b1f40abe7c4ca|1449306839000|1436092370000; z_c0="QUFEQTVjMGVBQUFYQUFBQVlRSlZUVGl2clZieTl6NmN1Z19JX0oxczJubWh0QmIyRGoxRjRnPT0=|1451631160|c67789a061fac4d814e558bf5e0964e398efa6e4"; __utma=51854390.322499337.1436092356.1451631139.1451637264.14; __utmz=51854390.1451637264.14.8.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/people/excited-vczh/followees; __utmv=51854390.100-1|2=registration_date=20131007=1^3=entry_date=20131007=1; _xsrf=3130d2c61e1c6d68615d5046fa9d1714; cap_id="YThhNjgyNmUxYzYxNDJkM2JmNjk1MzU5OGVhNzA5NjE=|1451631135|c1a47afe58d0fdbcba7f0f524ca913809b709b79"; __utmc=51854390' -H 'Connection: keep-alive'

http = httplib2.Http(disable_ssl_certificate_validation=True)

resp, content = http.request(url, headers=headers)
print resp
print content
