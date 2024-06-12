import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 한글 폰트 설정
plt.rc("font", family="Malgun Gothic")

# 마이너스 기호가 깨지는 문제 해결
plt.rcParams["axes.unicode_minus"] = False

# 파일 경로 설정
file_path_expense = "data/가구의_월평균_소득별_학생_1인당_월평균_사교육비_20240609023723.csv"
file_path_grade = "data/학생_성적_구간별_학생_1인당_월평균_사교육비_20240609023827.csv"

# 데이터 로드
df_expense = pd.read_csv(file_path_expense, encoding="utf-8", header=1)
df_grade = pd.read_csv(file_path_grade, encoding="utf-8", header=1)

# 열 이름 변경
df_expense.columns = [
    "과목 및 유형", "평균", "300만원 미만", "200만원 미만", "200-300만원",
    "300-400만원", "400-500만원", "500-600만원", "600-700만원", "700-800만원", "800만원 이상"
]
df_grade.columns = [
    "과목 및 유형", "평균", "상위10% 이내", "11-30%", "31-60%", "61-80%", "81-100%"
]

# 데이터 추출
df_expense_needed = df_expense[df_expense["과목 및 유형"].str.contains("과목: 일반교과 사교육|국어|영어|수학|사회, 과학")]
df_grade_needed = df_grade[df_grade["과목 및 유형"].str.contains("과목: 일반교과 사교육|국어|영어|수학|사회, 과학")]

# 열 이름 변경
df_expense_needed = df_expense_needed.rename(columns={"평균": "평균(만원)"})
df_grade_needed = df_grade_needed.rename(columns={"평균": "평균(만원)"})

# 성적 상위와 하위 학생들의 일반교과 사교육비 비교
high_grade_levels = ["상위10% 이내", "11-30%"]
low_grade_levels = ["61-80%", "81-100%"]

# 평균 계산
df_high_grade = df_grade_needed[["과목 및 유형"] + high_grade_levels]
df_high_grade = df_high_grade.melt(id_vars=["과목 및 유형"], var_name="성적구간", value_name="사교육비(만원)")\
    .groupby("과목 및 유형")["사교육비(만원)"].mean().reset_index()

df_low_grade = df_grade_needed[["과목 및 유형"] + low_grade_levels]
df_low_grade = df_low_grade.melt(id_vars=["과목 및 유형"], var_name="성적구간", value_name="사교육비(만원)")\
    .groupby("과목 및 유형")["사교육비(만원)"].mean().reset_index()

# 데이터 병합
df_grade_diff = pd.merge(df_high_grade, df_low_grade, on="과목 및 유형", suffixes=("_상위", "_하위"))
df_grade_diff["차이"] = df_grade_diff["사교육비(만원)_상위"] - df_grade_diff["사교육비(만원)_하위"]
df_grade_diff = df_grade_diff.sort_values(by="차이", ascending=False)

# 데이터 시각화
plt.figure(figsize=(10, 6))
sns.barplot(data=df_grade_diff, x="과목 및 유형", y="차이")
plt.title("성적이 높은 학생들이 일반교과 사교육에 투자하는 과목별 사교육비 차이")
plt.xlabel("과목 및 유형")
plt.ylabel("사교육비 차이 (만원)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 결과 출력
print("성적이 높은 학생들이 일반교과 사교육에 투자하는 과목별 사교육비 차이:")
print(df_grade_diff[["과목 및 유형", "차이"]])

# 성적이 낮은 학생들이 일반교과 사교육에 투자하는 과목별 사교육비
df_grade_diff["차이_하위"] = df_grade_diff["사교육비(만원)_하위"] - df_grade_diff["사교육비(만원)_상위"]
df_grade_diff_low = df_grade_diff.sort_values(by="차이_하위", ascending=False)

plt.figure(figsize=(10, 6))
sns.barplot(data=df_grade_diff_low, x="과목 및 유형", y="차이_하위")
plt.title("성적이 낮은 학생들이 일반교과 사교육에 투자하는 과목별 사교육비 차이")
plt.xlabel("과목 및 유형")
plt.ylabel("사교육비 차이 (만원)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 결과 출력
print("성적이 낮은 학생들이 일반교과 사교육에 투자하는 과목별 사교육비 차이:")
print(df_grade_diff_low[["과목 및 유형", "차이_하위"]])
