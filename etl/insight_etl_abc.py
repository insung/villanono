import os
import uuid
from abc import ABC, abstractmethod

import pandas

from util import makedir_if_not_exists


class InsightETLABC(ABC):
    __size_ranges = [0, 33, 66, 99, 1653]
    __size_labels = [
        "10평대",
        "20평대",
        "30평대",
        "40평대 이상",
    ]
    __size_rnages_filenames = {
        "all": None,
        "under_20": "10평대",
        "under_30": "20평대",
        "under_40": "30평대",
        "over_40": "40평대 이상",
    }
    __aggregate = {
        "거래금액(만원)": [
            "count",
            "mean",
            "std",
            "min",
            lambda x: x.quantile(0.25),
            "median",
            lambda x: x.quantile(0.75),
            "max",
        ]
    }
    __insight_describe_columns = [
        "계약년월",
        "거래량(건)",
        "평균(만원)",
        "표준편차(만원)",
        "최소(만원)",
        "25%",
        "50%",
        "75%",
        "최대(만원)",
    ]
    dir_data_original = os.path.join("data", "original")
    dir_data_temp = os.path.join("data", "temp")
    dir_data_output = os.path.join("data", "ouput")

    @abstractmethod
    def get_columns(self) -> list[str]:
        raise NotImplementedError

    @abstractmethod
    def get_filename(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_path_data_original(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_dir_data_temp(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_dir_data_output(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_extract_query(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_extract_sales_column(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_extract_size_column_index(self) -> int:
        raise NotImplementedError

    def extract(self):
        df1 = self.__read_original_file(self.get_path_data_original())
        df2 = df1.query(self.get_extract_query())
        df2[self.get_extract_sales_column()] = (
            df2[self.get_extract_sales_column()].str.replace(",", "").astype(int)
        )
        temp_path = os.path.join(self.get_dir_data_temp(), self.get_filename())
        self.__extract_groupby_size(
            df2, self.get_extract_size_column_index(), temp_path
        )

    def transform(self):
        for key, value in self.__size_rnages_filenames.items():
            self.__transform(value, key)

    def __transform(self, column_alias: str, dir_lastname: str):
        temp_path = os.path.join(self.get_dir_data_temp(), self.get_filename())
        df = self.__file_to_dataframe(temp_path, column_alias, self.get_columns())
        size_selected_path = os.path.join(self.get_dir_data_output(), dir_lastname)
        makedir_if_not_exists(size_selected_path)
        output_path = os.path.join(size_selected_path, self.get_filename())
        df.to_csv(output_path, index=False)

    def __read_original_file(self, file_path: str, skiprows=15) -> pandas.DataFrame:
        with open(file_path, "r") as infile:
            content = infile.read()

        temp_outputfile_path = os.path.join("data", "temp", f"{uuid.uuid4()}.csv")

        with open(temp_outputfile_path, "w", encoding="utf-8") as outfile:
            outfile.write(content)

        df = pandas.read_csv(temp_outputfile_path, skiprows=skiprows)
        os.remove(temp_outputfile_path)
        return df

    def __file_to_dataframe(
        self, path_data_temp: str, selected_size: str | None, columns: list[str]
    ):
        df = pandas.read_csv(path_data_temp)
        df.columns = columns

        if selected_size is None:
            temp = df.groupby(["계약년월"], as_index=False).agg(self.__aggregate)
        else:
            temp = (
                df.query(f"전용면적_그룹 == '{selected_size}'")
                .groupby(["계약년월"], as_index=False)
                .agg(self.__aggregate)
            )
        temp.columns = self.__insight_describe_columns
        temp["평균(만원)"] = temp["평균(만원)"].round(2)
        return temp

    def __extract_groupby_size(
        self, df: pandas.DataFrame, size_index: int, temp_output_file_path: str
    ):
        original_data_list = []

        df.loc[:, "계약일자"] = df["계약년월"].astype(str) + df["계약일"].astype(
            str
        ).str.zfill(2)
        df["계약일자"] = pandas.to_datetime(df["계약일자"], format="%Y%m%d")
        col_name = df.columns.values[size_index]  # 전용면적
        df["전용면적_그룹"] = pandas.cut(
            df[col_name],
            bins=self.__size_ranges,
            labels=self.__size_labels,
            right=False,
        )
        original_data_list.append(df)

        # merge with old
        pandas.concat(original_data_list).to_csv(temp_output_file_path)
