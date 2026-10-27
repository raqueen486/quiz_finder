import urllib.request
import datetime
import re

def get_latest_quiz_info():
    try:
        # 네이버에 '캐시워크 정답' 검색
        url = "https://search.naver.com/search.naver?query=%EC%BA%90%EC%8B%9C%EC%9B%8C%ED%81%AC+%EC%A0%95%EB%8B%B5"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        html = urllib.request.urlopen(req).read().decode('utf-8')
        
        # 검색 결과 중 첫 번째 글 제목(보통 정답이 포함됨) 추출
        matches = re.findall(r'class=".*?total_tit.*?".*?>(.*?)</a>', html)
        if matches:
            # 불필요한 태그 제거 및 길이 조절
            title = re.sub(r'<[^>]+>', '', matches[0])
            if len(title) > 35:
                title = title[:35] + "..."
            return f"최신 힌트: {title}"
        return "최신 정답을 찾는 중입니다..."
    except Exception as e:
        return "정답 업데이트 지연 중"

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
