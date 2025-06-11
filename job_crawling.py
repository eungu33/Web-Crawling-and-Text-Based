import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import koreanize_matplotlib


# 크롬 드라이버 설정
options = Options()
options.add_argument("--headless")  # 브라우저 없이 실행
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")


service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

 
# 여러 페이지 크롤링
total_pages = 20  # 원하는 페이지 수


name = []
job_title = []
salary = []
career = []
local = []

for page in range(1, total_pages + 1):
    url = f"https://www.work24.go.kr/wk/a/b/1200/retriveDtlEmpSrchList.do?occupation= \
            135100%2C135101%2C135200&resultCnt=10&currentPageNo={page}&pageIndex={page} \
            &sortField=DATE&sortOrderBy=DESC"
    driver.get(url)

    try:
        tbody = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "box_group_wrap"))
        )
        print(f"✅ {page} 페이지 로드 성공!")

        rows = tbody.find_elements(By.TAG_NAME, "tr")  # <tr> 요소 리스트 가져오기


        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")  # <td> 요소 가져오기
            if len(cols) >= 3:
                company1 = cols[0].text.strip().split('\n')  # 회사 정보
                company2 = cols[1].text.strip().split('\n')  # 연봉 정보
                
                name.append(company1[0])
                job_title.append(company1[1:-1])
                salary.append(company2[0])
                career.append(company2[1])
                local.append(company2[-1])



    except Exception as e:
        print(f"❌ {page} 페이지 크롤링 실패:", e)

import re

local = [title.replace('등', '') for title in local]
#print('\n')
#print("회사명\n", name,'\n,\n')
#print("직무\n", job_title,'\n,\n')
#print("연봉\n", salary,'\n,\n')
#print("경력 정보\n", career,'\n,\n')
#print("지역\n", local)



# 크롤러 종료
driver.quit()



exportDF = pd.DataFrame(columns=['회사명','직무','연봉','경력','지역'])
exportDF['회사명']=name
exportDF['직무']=job_title
exportDF['연봉']=salary
exportDF['경력']=career
exportDF['지역']=local

#print(exportDF)

# CSV 파일로 저장
#exportDF.to_csv("채용공고.csv", index=False, encoding="utf-8-sig")
#print("채용공고.csv 파일 저장 완")


#--------------------------------------------------------------------
# 1. 직무
# 직무직무직무직무직무직무직무직무직무직무직무직무직무직무직무직무직무직무직무직무직무직무직무직무직무직무직무직무직무직무직무직무직무직무직무직무

import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from PIL import Image
import numpy as np
from	wordcloud	import	STOPWORDS
# CSV 불러오기
#  직무 컬럼
df = pd.read_csv("data/채용공고_다중페이지.csv")

# 컬럼을 하나의 문자열로 합치기
text_data = " ".join(df["직무"].astype(str))

STOPWORDS.add('채용')
STOPWORDS.add('및')
STOPWORDS.add('부문별')
STOPWORDS.add('상반기')
STOPWORDS.add('사원')
STOPWORDS.add('직원')
STOPWORDS.add('모십니다')
STOPWORDS.add('경력')
STOPWORDS.add('신입')
STOPWORDS.add('직군')







# 3) 마스크 이미지 로드 (흑백 변환)
mask_image = Image.open("data/light.png").convert("L")
mask_array = np.array(mask_image)

# 4) 워드클라우드 생성 (STOPWORDS 없음)
wordcloud = WordCloud(
    font_path="malgun.ttf",   # Windows 기준, 맑은 고딕 폰트
    background_color="white", # 배경색
    mask=mask_array,          # 마스크 적용
    stopwords=STOPWORDS,
    width=800,
    height=600
).generate(text_data)

# 5) 시각화
plt.figure(figsize=(10, 8))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()

# ---------------------------------------------------------------
# 2.  연봉
# 연봉연봉연봉연봉연봉연봉연봉연봉연봉연봉연봉연봉연봉연봉연봉연봉연봉연봉연봉연봉연봉연봉연봉연봉연봉연봉연봉연봉연봉연봉연봉연봉연봉연봉연봉연봉연봉연봉

from collections import Counter

freq = Counter(salary)


# 4. 마스크 이미지 준비 (전구 그림인 light.png).
#    흰색 배경 + 검정 전구라면 전구 내부가 빈 공간이 될 수 있어
#    필요하다면 ImageOps.invert()로 반전하여 사용
#mask = np.array(Image.open("data/light.png"))

# 5. 워드클라우드 생성
wordcloud = WordCloud(
    font_path="malgun.ttf",  # (Windows) 맑은고딕 사용, Mac은 "/System/Library/Fonts/AppleGothic.ttf" 등
    width=800,
    height=400,
    background_color="white",
    #mask=mask_array
).generate_from_frequencies(freq)

# 6. 결과 시각화
#plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()


# ---------------------------------------------------------------
# 3. 지역
# 지역지역지역지역지역지역지역지역지역지역지역지역지역지역지역지역지역지역지역지역지역지역지역지역지역지역지역지역지역지역지역

import re
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from PIL import Image
from wordcloud import WordCloud

# 1. 지역 리스트를 문자열로 변환
local_text = " ".join(local)

# 2. 정규식: 2글자 이상 지역명만 추출
pattern = re.compile(r"[가-힣]{2,}(?:시|구|군|동|읍|면)?")
nouns = pattern.findall(local_text)  # 지역명 리스트 추출

# 3. 단어 빈도수 계산
word_count = Counter(nouns)

# 4. 마스크 이미지 로드 (흰색 배경, 검정색 전구 모양)
mask = np.array(Image.open("data/지도.jpg"))

# 5. 워드클라우드 생성
wordcloud = WordCloud(
    font_path="malgun.ttf",  # Windows: "malgun.ttf", Mac: "AppleGothic"
    width=800,
    height=400,
    mask=mask,  # 마스크 적용
    background_color="white",  # 배경을 흰색으로 설정
    colormap="inferno"  # 색상 테마 적용
).generate_from_frequencies(word_count)

# 6. 워드클라우드 출력
plt.figure(figsize=(10, 8))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()

# ----------------------------------------------------------------------

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
from collections import Counter
from PIL import Image
from wordcloud import WordCloud

#############################
# 1. "연봉" 문자열 파싱 함수
#############################
def parse_salary_to_yearly(line: str):
    """
    주어진 급여 문자열(line)을 읽어 '연봉' 최솟값, 최댓값(단위: 만원)을 반환.
    - "회사내규" → None
    - "3,100 만원 ~ 3,200 만원"  -> (3100, 3200)
    - "2,600 만원 이상"          -> (2600, None)
    - "월급 230 만원 ~ 350 만원" -> (230*12, 350*12) = (2760, 4200)
    - "시급 10,500 원 이상"      -> (10,500×209×12)/10000 = (연봉 만원)
    """
    line = line.strip()
    if "회사내규" in line:
        return None
    
    # 시급
    if "시급" in line:
        # 예) "시급 10,500 원 이상"
        numbers = re.findall(r"\d+,?\d+", line)  # ['10,500']
        if not numbers:
            return None
        s_min = float(numbers[0].replace(",", ""))  # 시급(원)
        yearly_min = s_min * 209 * 12 / 10000       # 만원 환산
        # "이상"이라고 가정, 최대값은 None
        return (round(yearly_min), None)
    
    # 월급
    if "월급" in line:
        # 예) "월급 230 만원 ~ 350 만원" or "월급 250 만원 이상"
        numbers = re.findall(r"\d+,?\d+", line)
        if not numbers:
            return None
        if "~" in line:   # 구간
            if len(numbers) >= 2:
                mn = float(numbers[0].replace(",", ""))
                mx = float(numbers[1].replace(",", ""))
                return (mn * 12, mx * 12)
            else:
                return None
        elif "이상" in line:
            mn = float(numbers[0].replace(",", ""))
            return (mn * 12, None)
        else:
            # 단일값
            mn = float(numbers[0].replace(",", ""))
            return (mn * 12, mn * 12)

    # 연봉 or 그냥 "n,nnn 만원" 형태
    numbers = re.findall(r"\d+,?\d+", line)  # ['3,100','3,200'] 등
    if not numbers:
        return None
    
    if "~" in line:   # 예) "3,100 만원 ~ 3,200 만원"
        if len(numbers) >= 2:
            mn = float(numbers[0].replace(",", ""))
            mx = float(numbers[1].replace(",", ""))
            return (mn, mx)
        else:
            return None
    elif "이상" in line:  # 예) "2,600 만원 이상"
        mn = float(numbers[0].replace(",", ""))
        return (mn, None)
    else:
        # 단일값
        mn = float(numbers[0].replace(",", ""))
        return (mn, mn)

#############################
# 2. CSV 불러와서 파싱
#############################
df = pd.read_csv("data/채용공고_다중페이지.csv")

# "연봉" 컬럼이 존재한다고 가정
salary_col = df["연봉"].fillna("회사내규에 따름")  # 혹시 NaN 있으면 임시처리

parsed_data = []
for raw_line in salary_col:
    result = parse_salary_to_yearly(raw_line)
    if result is not None:
        min_v, max_v = result
        parsed_data.append((raw_line, min_v, max_v))
    else:
        parsed_data.append((raw_line, None, None))

parsed_df = pd.DataFrame(parsed_data, columns=["raw_text","min_salary","max_salary"])

#############################
# 3. 간단한 히스토그램 시각화 (최소 연봉 기준)
#############################
valid = parsed_df.dropna(subset=["min_salary"])  # 숫자 있는 것만
min_vals = valid["min_salary"]

plt.figure(figsize=(10,5))
plt.hist(min_vals, bins=15, edgecolor='black')
plt.title("데이터 관련 직무 연봉")
plt.xlabel("연봉 (만원, min)")
plt.ylabel("Count")
plt.show()


# -------------------------------------------------------------------


df = pd.read_csv("data/채용공고_다중페이지.csv")

# 컬럼을 하나의 문자열로 합치기
text_data = " ".join(df["경력"].astype(str))


# 5. 워드클라우드 생성
wordcloud = WordCloud(
    font_path="malgun.ttf",  # (Windows) 맑은고딕 사용, Mac은 "/System/Library/Fonts/AppleGothic.ttf" 등
    width=800,
    height=400,
    background_color="white",
    #mask=mask_array
).generate_from_frequencies(text_data)

# 6. 결과 시각화
#plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()
