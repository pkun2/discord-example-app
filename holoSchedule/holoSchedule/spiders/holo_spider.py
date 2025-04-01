import re
import scrapy
import chardet
from holoSchedule.items import HoloscheduleItem

class HoloSpider(scrapy.Spider):
    name = "test"

    def start_requests(self):
        url = "https://schedule.hololive.tv/lives/all"
        cookies = {
            'timezone': 'Asia/Seoul'
        }

        yield scrapy.Request(url, cookies=cookies, callback=self.parse)

    def parse(self, response):
        encoding = chardet.detect(response.body)['encoding']
        body = response.body.decode(encoding, errors='ignore')
        selector = scrapy.Selector(text=body)
        
        # 모든 컨테이너를 크롤링링
        containers = selector.xpath('//*[@id="all"]/div')
        
        current_day = None
        
        for container in containers:
            # 날짜 정보가 있는지 확인
            day_info = container.xpath('./div/div[1]/div/div/text()').get()
            
            if day_info and day_info.strip():
                day_text = day_info.strip()
                # 정규표현식으로 날짜 형식 확인 (MM/DD (요일))
                date_match = re.match(r'(\d{2}/\d{2})\s*\(([月火水木金土日])\)', day_text)
                
                if date_match:
                    # 날짜 컨테이너를 발견했으면 현재 날짜를 업데이트
                    current_day = day_text
            
            # 이벤트 컨테이너인지 확인 (이벤트는 div[2] 아래에 있음)
            events = container.xpath('./div/div[2]/div/div')
            
            if events and current_day:  # 이벤트가 있고 현재 날짜가 설정되어 있으면
                for event in events:
                    item = HoloscheduleItem()
                    item['day'] = current_day  # 현재 추적 중인 날짜 정보 추가
                    item['name'] = event.xpath('.//a/div/div/div[1]/div/div[2]/text()').get()
                    item['time'] = event.xpath('.//a/div/div/div[1]/div/div[1]').get()
                    item['imgLink'] = event.xpath('.//a/div/div/div[2]/img').get()
                    
                    item['youtubelink'] = event.xpath('.//a/@href').get()
                    yield item

# name: /div[1]/a/div/div/div[1]/div/div[2]/text()
# time: /div[1]/a/div/div/div[1]/div/div[1]/text()
# //*[@id="all"]/div[5]/div/div[2]/div/div[1]/a/div/div/div[1]/div/div[1]
# //*[@id="all"]/div[5]/div/div[2]/div/div[1]/a/div/div/div[1]/div/div[1]/text()
# //*[@id="all"]/div[5]/div/div[2]/div/div[1]/a/div/div/div[1]/div/div[1]/img
# imgLink: /div[1]/a/div/div/div[2]/img
# youtubelink:/div[1]/a/@href

# day //*[@id="all"]/div[1]/div/div[1]/div/div
# //*[@id="all"]/div[5]/div/div[2]/div/div[1]/a/div/div/div[1]/div/div[1]/text()
# //*[@id="all"]/div[1]/div/div[2]/div/div[1]/a/div/div/div[1]/div/div[2]
# //*[@id="all"]/div[1]/div/div[2]/div/div[2]/a/div/div/div[1]/div/div[2]
# //*[@id="all"]/div[2]/div/div[2]/div/div[1]/a/div/div/div[1]/div/div[2]
# //*[@id="all"]/div[2]/div/div[2]/div/div[2]/a/div/div/div[1]/div/div[2]
# //*[@id="all"]/div[2]/div/div[2]/div/div[3]/a/div/div/div[1]/div/div[2]
# //*[@id="all"]/div[5]/div/div[2]/div/div[1]/a/div/div/div[1]/div/div[2]