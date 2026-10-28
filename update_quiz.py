import urllib.request
import xml.etree.ElementTree as ET
import datetime
import re

def get_latest_quiz_info():
    try:
        # 기계가 읽도록 공식 제공되는 구글 뉴스 RSS 활용 (최근 1일 이내 '캐시워크 정답' 검색)
        url = "https://news.google.com/rss/search?q=%EC%BA%90%EC%8B%9C%EC%9B%8C%ED%81%AC+%EC%A0%95%EB%8B%B5+when:1d&hl=ko&gl=KR&ceid=KR:ko"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        xml_data = urllib.request.urlopen(req).read()
        
        # XML 데이터 파싱
        root = ET.fromstring(xml_data)
        
        # 첫 번째 뉴스 기사 제목 가져오기
        for item in root.findall('.//item'):
            title = item.find('title').text
            if '캐시워크' in title or '정답' in title:
                # 제목 뒤에 붙는 언론사 이름( - OO뉴스) 제거
                title = title.split(' - ')[0] 
                
                if len(title) > 35:
                    title = title[:35] + "..."
                return f"뉴스 힌트: {title}"
                
        return "오늘자 새로운 정답 뉴스가 없습니다."
        
    except Exception as e:
        return f"뉴스 연결 에러: {e}"

# 1. 한국 표준시(KST)로 현재 시간 가져오기
now = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
current_time = now.strftime("%Y년 %m월 %d일 %H시 %M분 업데이트")

# 2. 크롤링으로 실제 정답 힌트 가져오기
answer_text = get_latest_quiz_info()

# 3. 기존 index.html 파일 읽어오기
with open("index.html", "r", encoding="utf-8") as f:
    html_content = f.read()

# 4. 시간 변경
html_content = re.sub(
    r'<div class="date">.*?</div>',
    f'<div class="date">{current_time}</div>',
    html_content
)

# 5. 정답 문구 변경
html_content = re.sub(
    r'<span class="answer">.*?</span>',
    f'<span class="answer">{answer_text}</span>',
    html_content
)

# 6. 변경된 내용 덮어쓰기
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"업데이트 완료: {current_time} / {answer_text}")
