import pandas
import os
import kagglehub

def data_import():
    DATA_PATH = kagglehub.dataset_download("uciml/electric-power-consumption-data-set")

    raw_data = pandas.read_csv(
    os.path.join(DATA_PATH, "household_power_consumption.txt"),
    sep=";",
    na_values=["?"], 
    low_memory=False
    )

    return raw_data


def main():
    data_import()

if __name__ == "__main__":
    main()


