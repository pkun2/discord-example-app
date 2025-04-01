import scrapy
from scrapy.pipelines.images import ImagesPipeline
import re

class HoloSchedulePipeline(ImagesPipeline):
    def process_item(self, item, spider):
        # 데이터를 정제
        item = self.clean_data(item)

        # 정제된 데이터를 파일에 저장
        with open('output.txt', 'a', encoding='utf-8') as f:
            f.write(str(item) + '\n')
        
        return item

    def clean_data(self, item):
        # 공백 제거
        item['name'] = item['name'].strip() if item['name'] else ''
        item['time'] = item['time'].strip() if item['time'] else ''
        
        # 정규 표현식을 사용하여 img 태그의 src 속성 추출
        img_src_pattern = r'<img\s+[^>]*src="([^"]+)"'
        time_pattern = r'(\d{2}:\d{2})'  # 시간 형식: 07:00
        time_match = re.search(time_pattern, item.get('time', ''))
        
        img_link_match = re.search(img_src_pattern, item['imgLink'])
        

        if time_match:
            item['time'] = time_match.group(1)
        else:
            item['time'] = ''

        if img_link_match:
            item['imgLink'] = img_link_match.group(1)
        else:
            item['imgLink'] = ''
        
        return item