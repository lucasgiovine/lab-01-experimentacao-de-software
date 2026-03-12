import csv
from statistics import median
from collections import Counter
import matplotlib.pyplot as plt


# -----------------------------
# CARREGAR CSV
# -----------------------------
def load_data(csv_file):

    age_days = []
    merged_prs = []
    releases = []
    last_update_days = []
    issue_ratio = []
    languages = []

    with open(csv_file, newline="", encoding="utf-8") as f:

        reader = csv.DictReader(f)

        for row in reader:

            age_days.append(float(row["age_days"]))
            merged_prs.append(float(row["merged_prs"]))
            releases.append(float(row["releases"]))
            last_update_days.append(float(row["last_update_days"]))
            issue_ratio.append(float(row["closed_issue_ratio"]))

            lang = row["language"]

            if lang and lang.strip() != "":
                languages.append(lang)

    return {
        "age_days": age_days,
        "merged_prs": merged_prs,
        "releases": releases,
        "last_update_days": last_update_days,
        "issue_ratio": issue_ratio,
        "languages": languages
    }


# -----------------------------
# CALCULAR MÉTRICAS
# -----------------------------
def compute_metrics(data):

    results = {}

    results["median_age_days"] = median(data["age_days"])
    results["median_merged_prs"] = median(data["merged_prs"])
    results["median_releases"] = median(data["releases"])
    results["median_last_update_days"] = median(data["last_update_days"])
    results["median_issue_ratio"] = median(data["issue_ratio"])

    language_freq = Counter(data["languages"])

    return results, language_freq


# -----------------------------
# GERAR CSV DE RESULTADOS
# -----------------------------
def generate_analysis_csv(results, language_freq):

    with open("analysis_results.csv", "w", newline="", encoding="utf-8") as f:

        writer = csv.writer(f)

        writer.writerow(["metric", "value"])

        writer.writerow(["median_repo_age_days", results["median_age_days"]])
        writer.writerow(["median_merged_prs", results["median_merged_prs"]])
        writer.writerow(["median_releases", results["median_releases"]])
        writer.writerow(["median_last_update_days", results["median_last_update_days"]])
        writer.writerow(["median_closed_issue_ratio", results["median_issue_ratio"]])

        writer.writerow([])
        writer.writerow(["language", "frequency"])

        for lang, count in language_freq.most_common():
            writer.writerow([lang, count])


# -----------------------------
# HISTOGRAMA PARA RQs
# -----------------------------
def plot_rq_distribution(data, median_value, title, xlabel, filename):

    plt.figure(figsize=(8,5))

    plt.hist(data, bins=30)

    plt.axvline(
    x=median_value,
    color="#FF0000",
    linestyle="--",
    linewidth=3,
    zorder=10,
    label=f"Median: {median_value:.2f}"
)

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel("Number of repositories")

    plt.legend()

    plt.tight_layout()

    plt.savefig(filename)

    plt.close()

    plt.figure(figsize=(8,5))

    plt.hist(data, bins=30)

    plt.axvline(
        median_value,
        linestyle="dashed",
        label=f"Median: {median_value:.2f}"
    )

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel("Number of repositories")

    plt.legend()

    plt.tight_layout()

    plt.savefig(filename)

    plt.close()


# -----------------------------
# TOP LINGUAGENS
# -----------------------------
def plot_top_languages(language_freq):

    top = language_freq.most_common(10)

    languages = [x[0] for x in top]
    counts = [x[1] for x in top]

    plt.figure(figsize=(10,6))

    plt.bar(languages, counts)

    plt.title("Top 10 Programming Languages")
    plt.ylabel("Number of repositories")

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.savefig("top_languages.png")

    plt.close()


# -----------------------------
# MAIN (ANÁLISE)
# -----------------------------
if __name__ == "__main__":

    data = load_data("repos.csv")

    results, language_freq = compute_metrics(data)

    plt.style.use("default")

    generate_analysis_csv(results, language_freq)

    # RQ1 — idade dos repositórios
    plot_rq_distribution(
        data["age_days"],
        results["median_age_days"],
        "RQ1 – Repository Age Distribution",
        "Repository age (days)",
        "rq1_repo_age.png"
    )

    # RQ2 — contribuição externa
    plot_rq_distribution(
        data["merged_prs"],
        results["median_merged_prs"],
        "RQ2 – Merged PRs Distribution",
        "Merged pull requests",
        "rq2_merged_prs.png"
    )

    # RQ3 — releases
    plot_rq_distribution(
        data["releases"],
        results["median_releases"],
        "RQ3 – Releases Distribution",
        "Number of releases",
        "rq3_releases.png"
    )

    # RQ4 — frequência de atualização
    plot_rq_distribution(
        data["last_update_days"],
        results["median_last_update_days"],
        "RQ4 – Last Update Distribution",
        "Days since last update",
        "rq4_last_update.png"
    )

    # RQ6 — proporção de issues fechadas
    plot_rq_distribution(
        data["issue_ratio"],
        results["median_issue_ratio"],
        "RQ6 – Closed Issue Ratio Distribution",
        "Closed issue ratio",
        "rq6_issue_ratio.png"
    )

    # linguagens
    plot_top_languages(language_freq)

    print("Análise e gráficos gerados com sucesso!")