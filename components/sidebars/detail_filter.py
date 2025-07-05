from datetime import datetime, timedelta

import streamlit

today = datetime.today()

#### choices ####
options_datatype = [("매매", "buysell"), ("전세", "rent"), ("월세", "rent2")]
choice_datatype = ["매매", "전세", "월세"]

options_size = [
    ("전체", 0),
    ("10평대 (33㎡미만)", 33),
    ("20평대 (66㎡미만)", 66),
    ("30평대 (99㎡미만)", 99),
    ("40평대 이상 (99㎡이상)", 1653),
]

options_built_year = [
    ("전체", None),
    ("~ 2년", today - timedelta(days=730)),
    ("~ 4년", today - timedelta(days=1460)),
    ("~ 10년", today - timedelta(days=3650)),
    ("~ 20년", today - timedelta(days=7300)),
    ("~ 30년", today - timedelta(days=10950)),
]

options_amount = [
    5_000,
    100_000_000,
    150_000_000,
    200_000_000,
    250_000_000,
    300_000_000,
    350_000_000,
    400_000_000,
    500_000_000,
    800_000_000,
    1_000_000_000,
    1_500_000_000,
    2_000_000_000,
    2_500_000_000,
    3_000_000_000,
]

# 2) 숫자값 → 라벨 매핑
options_amount_label = {
    5_000: "5천",
    100_000_000: "1억",
    150_000_000: "1.5억",
    200_000_000: "2억",
    250_000_000: "2.5억",
    300_000_000: "3억",
    350_000_000: "3.5억",
    400_000_000: "4억",
    500_000_000: "5억",
    800_000_000: "8억",
    1_000_000_000: "10억",
    1_500_000_000: "15억",
    2_000_000_000: "20억",
    2_500_000_000: "25억",
    3_000_000_000: "30억",
}

# 3) select_slider 호출


def set_detail_filter(st: streamlit):
    # 거래방식 (매매/전세/월세)
    selected_datatype = st.segmented_control(
        label="거래방식",
        options=choice_datatype,
        default=choice_datatype,
        selection_mode="multi",
        # format_func=lambda x: x[0],
    )
    # 가격대 (slide 로)
    begin_amount, end_amount = st.select_slider(
        "가격대",
        options=options_amount,
        value=(options_amount[4], options_amount[6]),
        format_func=lambda x: options_amount_label[x],  # 화면엔 라벨만!
    )

    # 면적
    _, st.session_state.selected_size = st.selectbox(
        label="면적",
        options=options_size,
        format_func=lambda x: x[0],
    )

    # 건축년도
    _, st.session_state.selected_built_year = st.selectbox(
        label="건축년도",
        options=options_built_year,
        help="건축년도는 현재 날짜로부터의 경과 시간을 기준으로 계산됩니다. 예를 들어, 건축년도가 10년인 경우, 이는 현재 날짜로부터 10년 전에 지어진 건물까지 포함하여 조회됩니다.",
        format_func=lambda x: x[0],
    )
