from read_file import groupby_yyyyMM, read_original_file


def test1():
    df2023 = read_original_file("2023전월세.csv")
    df2023 = groupby_yyyyMM(df2023)
    # temp = df2023.filter(df2023["계약년월"] == 202301)
    print(df2023)


if __name__ == "__main__":
    test1()
