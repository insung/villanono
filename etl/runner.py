from etl.insight_buysell_built_year_etl import InsightBuySellBuiltYearETL
from etl.insight_buysell_etl import InsightBuySellETL
from etl.insight_rent_etl import InsightRentETL
from util import read_divisions


def run():
    sigudong = read_divisions()

    for year in range(2006, 2024 + 1):
        # extract_division_data(data_file_path, __output_division_path)

        for si_items in sigudong.items():
            for gu_dict in si_items[1].items():
                for dong in gu_dict[1]:
                    si = si_items[0]
                    gu = gu_dict[0]

                    etl = InsightBuySellETL(si, gu, dong, year)
                    etl.extract()
                    etl.transform()


def run2():
    etl = InsightRentETL("서울특별시", "서대문구", "북가좌동", 2024)
    etl.extract()
    etl.transform()


def run3():
    etl = InsightBuySellBuiltYearETL("서울특별시", "서대문구", "북가좌동", 2024, 2015)
    etl.extract()
    etl.transform()


run3()
