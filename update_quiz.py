import urllib.request
import datetime
import re

def get_latest_quiz_info():
    try:
        # 사람들이 실시간으로 정답을 공유하는 커뮤니티 (뽐뿌 앱테크 게시판) 접속
        url = "https://www.ppomppu.co.kr/zboard/zboard.php?id=apptech"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36'
        }
        req = urllib.request.Request(url, headers=headers)
        
        # 해당 사이트는 euc-kr 인코딩을 사용하므로 맞춰서 디코딩 (글자 깨짐 방지)
        html = urllib.request.urlopen(req).read().decode('euc-kr', errors='ignore')
        
        # 게시글 제목 추출 (해당 커뮤니티의 제목 태그 구조)
        titles = re.findall(r'<font class=list_title>(.*?)</font>', html)
        
        for title in titles:
            # 캐시워크, 토스, 정답 등의 키워드가 포함된 글만 필터링
            if '캐시' in title or '토스' in title or '정답' in title:
                # 불필요한 HTML 태그 및 띄어쓰기 기호 정리
                title = re.sub(r'<[^>]+>', '', title) 
                title = title.replace('&nbsp;', ' ').strip()
                
                if len(title) > 35:
                    title = title[:35] + "..."
                return f"커뮤니티 공유 힌트: {title}"
                
        return "새로운 정답 글이 올라오기를 기다리는 중입니다."
        
    except Exception as e:
        return f"커뮤니티 접속 에러 발생: {e}"

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
