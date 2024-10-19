from etl.insight_buysell_etl import InsightBuySellETL


class InsightBuySellBuiltYearETL(InsightBuySellETL):
    def __init__(self, si: str, gu: str, dong: str, year: int, built_year: int):
        super().__init__(si, gu, dong, year)
        self.built_year = built_year

    def get_filename(self) -> str:
        return f"{self.year}_매매_{self.built_year}.csv"

    def get_extract_query(self):
        return f"시군구 == '{self.si} {self.gu} {self.dong}' & 건축년도 == {self.built_year}"
