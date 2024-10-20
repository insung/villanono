import os
import uuid
from genericpath import exists

import pandas

from util import makedir_if_not_exists, read_divisions

__si = "서울특별시"
__readable_path = os.path.join("data", "original_to_csv", __si)
__size_ranges = [0, 33, 66, 99, 1653]
__size_labels = [
    "10평대",
    "20평대",
    "30평대",
    "40평대 이상",
]


def run_original_buysell_to_csv():
    makedir_if_not_exists(__readable_path)

    for year in range(2006, 2025):
        file_path = f"{year}_연립다세대(매매).csv"

        with open(os.path.join("data", "original", __si, file_path), "r") as infile:
            content = infile.read()

        temp_outputfile_path = os.path.join("data", "temp2", f"{uuid.uuid4()}.csv")

        with open(temp_outputfile_path, "w", encoding="utf-8") as outfile:
            outfile.write(content)

        df = pandas.read_csv(temp_outputfile_path, skiprows=15)
        os.remove(temp_outputfile_path)
        df.to_csv(os.path.join(__readable_path, file_path), index=False)


def run_readable_csv_to_db():
    sigudong = read_divisions()

    for year in range(2006, 2025):
        file_path = f"{year}_연립다세대(매매).csv"

        df = pandas.read_csv(os.path.join(__readable_path, file_path))

        df["거래금액(만원)"] = df["거래금액(만원)"].str.replace(",", "").astype(int)
        df.loc[:, "계약일자"] = df["계약년월"].astype(str) + df["계약일"].astype(
            str
        ).str.zfill(2)
        df["계약일자"] = pandas.to_datetime(df["계약일자"], format="%Y%m%d")

        df.columns = [
            "NO",
            "시군구",
            "번지",
            "본번",
            "부번",
            "건물명",
            "전용면적",
            "대지권면적",
            "계약년월",
            "계약일",
            "거래금액(만원)",
            "층",
            "매수자",
            "매도자",
            "건축년도",
            "도로명",
            "해제사유발생일",
            "거래유형",
            "중개사소재지",
            "등기일자",
            "계약일자",
        ]

        df[["시", "구", "동"]] = df["시군구"].str.split(" ", expand=True)
        df = df.drop(columns=["NO", "시군구"])

        cols = ["시", "구", "동"] + [
            col for col in df.columns if col not in ["시", "구", "동"]
        ]

        # 컬럼 순서 변경
        df = df[cols]

        df["전용면적_그룹"] = pandas.cut(
            df["전용면적"],
            bins=__size_ranges,
            labels=__size_labels,
            right=False,
        )

        for si_items in sigudong.items():
            for gu_dict in si_items[1].items():
                gu = gu_dict[0]

                result = df.query(f"구 == '{gu}'")

                result_file_path = os.path.join(
                    "data", "temp3", __si, f"{gu}_연립다세대(매매).csv"
                )

                print("processing", year, gu)

                if exists(result_file_path):
                    old = pandas.read_csv(result_file_path)
                    result = pandas.concat([old, result])

                    result.to_csv(
                        result_file_path,
                        index=False,
                    )
                else:
                    result.to_csv(
                        result_file_path,
                        index=False,
                    )


run_readable_csv_to_db()
