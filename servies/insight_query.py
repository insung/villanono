from datetime import datetime


def get_insight_query(
    begin_date: datetime,
    selected_si: str,
    selected_gu: str,
    selected_dong: str | None,
    selected_built_year: datetime | None,
    selected_size: str | None,
) -> str:
    begin_yyyyMM = int(begin_date.strftime("%Y%m"))

    if selected_dong:
        query = f"시 == '{selected_si}' & 구 == '{selected_gu}' & 동 == '{selected_dong}' & 계약년월 >= {begin_yyyyMM}"
    else:
        query = f"시 == '{selected_si}' & 구 == '{selected_gu}' & 계약년월 >= {begin_yyyyMM}"

    if selected_built_year:
        query = query + f" & 건축년도 >= {selected_built_year.year}"

    if selected_size:
        query = query + f" & 전용면적_그룹 == '{selected_size}'"

    return query
