from flask import Flask, render_template, request
import yfinance as yf

app = Flask(__name__)

# 주식 티커에 대한 섹터, 산업 및 풀네임 정보 가져오기
def get_stock_info(ticker):
    stock = yf.Ticker(ticker)
    name = stock.info.get('longName', '정보 없음')  # 주식 풀네임 추가
    sector = stock.info.get('sector', '정보 없음')
    industry = stock.info.get('industry', '정보 없음')
    return name, sector, industry

# 점수 계산 함수
def calculate_score(interest_rate_current, interest_rate_previous, cpi_current, ism_index, gdp_growth, interest_rate_diff_current, interest_rate_diff_previous):
    weights = {
        "rate": 0.35,
        "cpi": 0.30,
        "ism": 0.15,
        "gdp": 0.15,
        "rate_diff": 0.05
    }
    score = 50  # 기본 점수

    if interest_rate_current > interest_rate_previous:
        score -= 10 * weights["rate"]
    else:
        score += 10 * weights["rate"]

    if cpi_current > 3:
        score -= 15 * weights["cpi"]
    elif cpi_current < 2:
        score += 5 * weights["cpi"]
    else:
        score += 3 * weights["cpi"]

    if ism_index > 50:
        score += 10 * weights["ism"]
    else:
        score -= 10 * weights["ism"]

    if gdp_growth > 3:
        score += 10 * weights["gdp"]
    else:
        score -= 5 * weights["gdp"]

    if interest_rate_diff_current > interest_rate_diff_previous:
        score -= 5 * weights["rate_diff"]
    else:
        score += 5 * weights["rate_diff"]

    return score

@app.route('/', methods=['GET', 'POST'])
def index():
    # 고정된 경제 지표 값
    economic_indicators = {
        'interest_rate_current': 4.5,
        'interest_rate_previous': 4.75,
        'cpi_current': 3.0,
        'ism_index': 48.4,
        'gdp_growth': 2.8,
        'interest_rate_diff_current': 4.25,
        'interest_rate_diff_previous': 4.5
    }

    # 사용자가 티커를 입력한 경우 처리
    if request.method == 'POST':
        ticker = request.form['ticker']
        name, sector, industry = get_stock_info(ticker)  # 수정된 함수 호출
        score = calculate_score(
            economic_indicators['interest_rate_current'], 
            economic_indicators['interest_rate_previous'],
            economic_indicators['cpi_current'],
            economic_indicators['ism_index'],
            economic_indicators['gdp_growth'],
            economic_indicators['interest_rate_diff_current'],
            economic_indicators['interest_rate_diff_previous']
        )
        score_percentage = max(0, min(100, score))

        return render_template(
            'index.html',
            ticker=ticker,
            name=name,  # 주식 풀네임 추가
            sector=sector,
            industry=industry,
            score=score_percentage,
            economic_indicators=economic_indicators
        )

    # GET 요청 시 렌더링
    return render_template('index.html', economic_indicators=economic_indicators)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
