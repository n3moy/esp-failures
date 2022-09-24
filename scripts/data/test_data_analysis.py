import os
import pandas as pd
# import numpy as np

REPORT_NAME = "test_nans.xlsx"


def collect_stats(
    data_path: str,
    description_path: str,
    output_path: str
):
    fnames = os.listdir(data_path)
    descr = pd.read_csv(description_path)
    features_groups = descr["Раздел"].unique().tolist()
    # analysis_cols = ["NaNs_" + group for group in features_groups]
    out_report = pd.DataFrame(columns=features_groups, index=fnames)
    group_to_features = {}
    group_num_features = {}

    for group in features_groups:
        vals = descr.query("Раздел == @group")["Название столбца"].values.tolist()
        group_to_features[group] = vals
        group_num_features[group] = len(vals)

    for fname in fnames:
        file_path = os.path.join(data_path, fname)
        test_file = pd.read_parquet(file_path)
        n_rows = test_file.shape[0]

        for group in features_groups:
            nan_cols_count = 0
            for col in group_to_features[group]:
                try:
                    nan_sum = test_file[col].isna().sum()
                    if nan_sum == n_rows:
                        nan_cols_count += 1
                except KeyError:
                    print(f"{col} not found in test file")
                    continue

            out_report.loc[fname, group] = nan_cols_count

    out_report.loc["ВСЕГО", :] = group_num_features
    # out_report.append(group_num_features, ignore_index=True)
    save_path = os.path.join(output_path, REPORT_NAME)
    out_report.to_excel(save_path)


if __name__ == "__main__":
    DATA_PATH = "../../data/test"
    DESCR_PATH = "../../reports/Описание признаков.csv"
    OUT_PATH = "../../reports"
    collect_stats(DATA_PATH, DESCR_PATH, OUT_PATH)
