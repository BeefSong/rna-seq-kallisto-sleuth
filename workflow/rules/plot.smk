rule interactive_plots:
    input:
        tsv="results/tables/diffexp/{model}.transcripts.diffexp.tsv",
    output:
        volcano_plot=directory(
            report(
                "results/plots/interactive/volcano/{model}/",
                caption="../report/plot-volcano.rst",
                patterns=["{name}.html"],
                category="Volcano plots",
            )
        ),
    params:
        model=get_model,
        sig_level_volcano=config["diffexp"]["sig-level"]["volcano-plot"],
    conda:
        "../envs/plotly.yaml"
    log:
        "logs/plotly/{model}.volcano.log",
    script:
        "../scripts/volcano-plot.py"
