import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import numpy as np

def load_and_preprocess_data(expense_path, income_path):
    # 데이터 로드 및 전처리
    df_income_expense = pd.read_csv(expense_path, encoding="utf-8")

    # 필요없는 행 제거 (첫 번째 행 제거)
    df_income_expense = df_income_expense.drop(index=0)

    # 열 이름 변경
    df_income_expense.columns = [
        "과목 및 유형",
        "평균",
        "200만원 미만",
        "200-300만원",
        "300-400만원",
        "400-500만원",
        "500-600만원",
        "600-700만원",
        "700-800만원",
        "800만원 이상",
        "여분",
    ]

    # '사교육비' 행 선택
    df_income_expense = df_income_expense[df_income_expense["과목 및 유형"] == "사교육비"]

    # 데이터 변환 (소득 구간을 행으로 변환)
    df_income_expense = df_income_expense.melt(
        id_vars=["과목 및 유형"], var_name="소득수준", value_name="월평균 사교육비"
    )

    # '월평균 사교육비' 컬럼을 숫자로 변환
    df_income_expense["월평균 사교육비"] = df_income_expense["월평균 사교육비"].astype(float)

    # '평균' 행 제거
    df_income_expense = df_income_expense[df_income_expense["소득수준"] != "평균"]

    # NaN 값 처리 (제거)
    df_income_expense.dropna(inplace=True)

    # 상관관계 분석을 위한 데이터 병합
    df_income_expense = df_income_expense[["소득수준", "월평균 사교육비"]].rename(
        columns={"월평균 사교육비": "소득수준_월평균 사교육비"}
    )

    # 범주형 변수 인코딩
    df_income_expense["소득수준"] = df_income_expense["소득수준"].astype("category").cat.codes

    return df_income_expense

def train_model(df):
    # 데이터 분할
    X = df[["소득수준"]]
    y = df["소득수준_월평균 사교육비"]

    # 데이터 정규화
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    X = pd.DataFrame(X_scaled, columns=X.columns)

    # 선형 회귀 모델
    lr_model = LinearRegression()
    lr_model.fit(X, y)

    return lr_model, scaler

def predict_education_expense(lr_model, scaler, income_level):
    income_levels = [
        "200만원 미만",
        "200-300만원",
        "300-400만원",
        "400-500만원",
        "500-600만원",
        "600-700만원",
        "700-800만원",
        "800만원 이상",
    ]

    if income_level not in income_levels:
        raise ValueError(
            f"소득 수준 '{income_level}'이(가) 유효하지 않습니다. 가능한 값: {income_levels}"
        )

    income_level_encoded = income_levels.index(income_level)
    input_data = scaler.transform([[income_level_encoded]])
    input_data = pd.DataFrame(input_data, columns=["소득수준"])
    prediction = lr_model.predict(input_data)

    return prediction[0]

def calculate_additional_support(lr_model, scaler):
    low_income_levels = ["200만원 미만", "200-300만원"]

    low_income_expenses = [
        predict_education_expense(lr_model, scaler, level) for level in low_income_levels
    ]
    low_income_average = np.mean(low_income_expenses)
    average_expense = predict_education_expense(lr_model, scaler, "500-600만원")

    additional_support = average_expense - low_income_average
    return additional_support

def calculate_average_income(df_income):
    average_income_row = df_income[(df_income["가계수지항목별"] == "소득")]

    if not average_income_row.empty:
        average_income_2023 = average_income_row["2023.4/4"].astype(float).values[0]
        average_income_2024 = average_income_row["2024.1/4"].astype(float).values[0]
        average_income = (average_income_2023 + average_income_2024) / 2
        return average_income
    else:
        raise ValueError("평균 소득 데이터를 찾을 수 없습니다.")

# 경로 설정
file_path_expense = "data/가구의_월평균_소득별_학생_1인당_월평균_사교육비_20240609023723.csv"
file_path_income = "data/소득10분위별_가구당_가계수지__전국_1인이상__20240609023453.csv"

# 데이터 로드 및 전처리
df_income_expense = load_and_preprocess_data(file_path_expense, file_path_income)
lr_model, scaler = train_model(df_income_expense)

# 소득 데이터 로드
df_income = pd.read_csv(file_path_income, encoding="utf-8")
average_income = calculate_average_income(df_income)
print(f"평균 소득: {average_income:.2f}원")

# 저소득층 가구에 대한 추가 지원 금액 계산
additional_support = calculate_additional_support(lr_model, scaler)

# 결과 출력
predicted_expense = predict_education_expense(lr_model, scaler, "500-600만원")
print(f"평균 소득에 대한 예측 사교육비: {predicted_expense:.2f}만원")
print(f"저소득층 가구에 대한 사교육비 추가 지원 금액: {additional_support:.2f}만원")
