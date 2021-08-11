from string import Template
import pandas as pd
from io import StringIO


def main(snakemake):

    # read vega js file with template vars
    # `$url`, `$sig_level`, `$beta_column` and `$beta_se_column`
    with open(snakemake.input.spec, "rt") as f:
        spec = Template(f.read())

    sig_level = snakemake.params.sig_level_volcano
    primary_var = snakemake.params.primary_variable

    # find column that matches primary variable
    df: pd.DataFrame = pd.read_csv(snakemake.input.tsv, sep="\t")
    primary_cols = [
        c
        for c in list(df.columns)
        if c.startswith(f"b_{primary_var}") and not c.endswith("_se")
    ]
    assert len(primary_cols) == 1
    beta_col = primary_cols[0]
    df = df[["ens_gene", "ext_gene", "target_id", "qval", beta_col, beta_col + "_se"]]
    data = StringIO()
    df.to_csv(data, sep="\t", index=False)

    # update the spec with concrete values
    json = spec.safe_substitute(
        data=data.getvalue().replace("\t", r"\t").replace("\n", r"\n"),
        sig_level=sig_level,
        beta_column=beta_col,
        beta_se_column=beta_col + "_se",
    )

    with open(snakemake.output.json, "wt") as f:
        f.write(json)


if __name__ == "__main__":
    main(snakemake)
