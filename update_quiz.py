import datetime
import re

# 1. 한국 표준시(KST)로 현재 시간 가져오기
now = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
current_time = now.strftime("%Y년 %m월 %d일 %H시 %M분 업데이트")

# 2. 기존 index.html 파일 읽어오기
with open("index.html", "r", encoding="utf-8") as f:
    html_content = f.read()

# 3. HTML 내용 안의 '준비 중입니다' 시간을 현재 시간으로 교체
html_content = re.sub(
    r'<div class="date">.*?</div>',
    f'<div class="date">{current_time}</div>',
    html_content
)

# 4. '업데이트 예정' 부분을 테스트 문구로 교체 (나중에 진짜 정답 크롤링 코드로 바꿀 부분)
html_content = re.sub(
    r'<span class="answer">.*?</span>',
    f'<span class="answer">자동 업데이트 성공! 🎉</span>',
    html_content
)

# 5. 수정된 내용을 index.html에 다시 덮어쓰기
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"업데이트 완료: {current_time}")
