import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import datetime
import re

# =====================================================================
# 🎯 [수정하는 곳] 여기에 원하는 퀴즈를 추가하거나 삭제하세요!
# =====================================================================
# 사용 방법:
# 1. 퀴즈를 추가하려면 아래 양식에 맞춰 한 줄을 복사해서 밑에 붙여넣으세요.
# 2. "name" 에는 웹페이지 화면에 보여질 앱 이름을 적으세요.
# 3. "keyword" 에는 구글 뉴스에서 검색할 단어를 적으세요.
# ※ 주의사항: 맨 마지막 줄을 제외하고, 각 줄 끝에는 반드시 쉼표(,)가 있어야 합니다.

QUIZ_LIST = [
    {"name": "H.Point (H포인트)", "keyword": "H포인트 정답"},
    {"name": "KB Pay (KB페이)", "keyword": "KB페이 정답"},

]
# =====================================================================


def get_latest_quiz_info(keyword):
    try:
        # 한글 검색어가 깨지지 않도록 변환
        encoded_keyword = urllib.parse.quote(keyword)
        url = f"https://news.google.com/rss/search?q={encoded_keyword}+when:1d&hl=ko&gl=KR&ceid=KR:ko"
        
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        xml_data = urllib.request.urlopen(req).read()
        root = ET.fromstring(xml_data)
        
        for item in root.findall('.//item'):
            title = item.find('title').text
            # 제목 뒤에 붙는 언론사 이름( - OO뉴스) 제거
            title = title.split(' - ')[0] 
            
            if len(title) > 35:
                title = title[:35] + "..."
            return f"뉴스 힌트: {title}"
                
        return "오늘자 정답 뉴스가 없습니다."
        
    except Exception as e:
        return "뉴스 연결 에러 발생"

# 1. 한국 표준시(KST)로 현재 시간 가져오기
now = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
current_time = now.strftime("%Y년 %m월 %d일 %H시 %M분 업데이트")

# 2. 위에서 작성한 퀴즈 목록(QUIZ_LIST)을 바탕으로 HTML 뼈대 자동으로 만들기
quiz_html_blocks = ['<div id="quiz-list">']

for quiz in QUIZ_LIST:
    answer_text = get_latest_quiz_info(quiz["keyword"])
    card_html = f'''
        <div class="quiz-card">
            <span class="app-name">{quiz["name"]}</span>
            <span class="answer">{answer_text}</span>
        </div>'''
    quiz_html_blocks.append(card_html)
    print(f"체크 완료: {quiz['name']}")

quiz_html_blocks.append('</div>')
final_quiz_html = "\n".join(quiz_html_blocks)

# 3. 기존 index.html 파일 읽어오기
with open("index.html", "r", encoding="utf-8") as f:
    html_content = f.read()

# 4. 상단 업데이트 시간 변경
html_content = re.sub(
    r'<div class="date">.*?</div>',
    f'<div class="date">{current_time}</div>',
    html_content
)

# 5. 여러 개로 늘어난 퀴즈 정답판 덮어쓰기 (re.DOTALL로 여러 줄 교체)
html_content = re.sub(
    r'<div id="quiz-list">.*?</div>',
    final_quiz_html,
    html_content,
    flags=re.DOTALL
)

# 6. 완성된 내용을 index.html에 최종 저장
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"전체 업데이트 완료: {current_time}")
