import pandas as pd
import matplotlib.pyplot as plt

# 한글 폰트 및 마이너스 기호 표시 설정
plt.rc("font", family="Malgun Gothic")
plt.rcParams["axes.unicode_minus"] = False

# 파일 경로 설정
file_path_expense = "data/가구의_월평균_소득별_방과후학교__EBS_교재__어학연수_참여율_20240609024147.csv"
file_path_region = "data/지역별_학생_1인당_월평균_사교육비_20240609023851.csv"

# 데이터 로드
df_expense = pd.read_csv(file_path_expense, encoding="utf-8", header=1)
df_region = pd.read_csv(file_path_region, encoding="utf-8", header=1)

# 열 이름 변경
df_expense.columns = [
    "유형", "평균", "300만원 미만", "200만원 미만", "200-300만원",
    "300-400만원", "400-500만원", "500-600만원", "600-700만원", "700-800만원", "800만원 이상"
]
df_region.columns = [
    "과목 및 유형", "평균", "대도시", "서울", "광역시", "대도시이외", "중소도시", "읍면지역"
]

# '방과후학교(유상+무상)', '방과후학교', 'EBS 교재', '어학연수' 행 선택
df_expense_filtered = df_expense[df_expense["유형"].isin(["방과후학교(유상+무상)", "방과후학교", "EBS 교재"])]
df_region_filtered = df_region[df_region["과목 및 유형"] == "사교육비"]

# 데이터 변환 (소득 구간을 행으로 변환)
df_expense_filtered = df_expense_filtered.melt(id_vars=["유형"], var_name="소득수준", value_name="참여율")
df_region_filtered = df_region_filtered.melt(id_vars=["과목 및 유형"], var_name="지역", value_name="월평균 사교육비")

# '참여율' 컬럼을 숫자로 변환
df_expense_filtered["참여율"] = df_expense_filtered["참여율"].astype(str).str.replace("%", "").astype(float)
df_region_filtered["월평균 사교육비"] = df_region_filtered["월평균 사교육비"].astype(float)

# 분석을 위한 데이터 결합
df_expense_filtered = df_expense_filtered.pivot(index="유형", columns="소득수준", values="참여율").reset_index()
df_region_filtered = df_region_filtered.pivot(index="과목 및 유형", columns="지역", values="월평균 사교육비").reset_index()

# 저소득층 지원을 위한 분석
low_income_levels = ["200만원 미만", "200-300만원"]
average_income_level = "평균"

# 저소득층의 참여율 평균 계산
low_income_participation = df_expense_filtered[low_income_levels].mean(axis=1)

# 평균 소득 가구의 참여율 계산
average_income_participation = df_expense_filtered[average_income_level]

# 추가 지원이 필요한 항목 계산
additional_support_expense = average_income_participation - low_income_participation
df_expense_filtered["추가 지원 필요"] = additional_support_expense * df_region_filtered[df_region_filtered["과목 및 유형"] == "사교육비"]["평균"].values[0] / 100

# 저소득층의 방과후학교 및 EBS 교재 지원 필요 계산
support_needed = df_expense_filtered[df_expense_filtered["유형"].isin(["방과후학교", "EBS 교재"])]
support_needed = support_needed[["유형", "추가 지원 필요"]]

# 결과 출력
print("저소득층 가구의 추가 지원 필요 항목:")
print(support_needed)

# 지역별 지원 분석
average_expense = df_region_filtered[df_region_filtered["과목 및 유형"] == "사교육비"]["평균"].values[0]
eup_myeon_expense = df_region_filtered[df_region_filtered["과목 및 유형"] == "사교육비"]["읍면지역"].values[0]

# 추가 지원 필요 금액 계산
additional_support_region = average_expense - eup_myeon_expense

# 결과 출력
print(f"읍면지역에 대한 추가 지원 필요 금액: {additional_support_region:.2f}만원")

# 저소득층 가구를 위한 사교육비 추가 지원 필요 항목 시각화
ax = support_needed.plot(kind="bar", x="유형", y="추가 지원 필요", legend=False)
plt.title("저소득층 가구의 추가 지원 필요 항목")
plt.xlabel("유형")
plt.ylabel("추가 지원 필요 금액 (만원)")
plt.xticks(rotation=0)  # x축 레이블을 가로로 설정
plt.show()

# 읍면지역 학생들에 대한 추가 지원 필요 금액 시각화
plt.bar(["평균", "읍면지역"], [average_expense, eup_myeon_expense], color=["blue", "red"])
plt.title("평균 소득 가구와 읍면지역의 사교육비 비교")
plt.xlabel("지역")
plt.ylabel("월평균 사교육비 (만원)")
plt.show()
