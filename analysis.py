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


def plot_all_metrics(results):

    fig, axs = plt.subplots(2, 3, figsize=(12, 8))

    metrics = [
        ("Repository Age (days)", results["median_age_days"]),
        ("Merged PRs", results["median_merged_prs"]),
        ("Releases", results["median_releases"]),
        ("Last Update (days)", results["median_last_update_days"]),
        ("Closed Issue Ratio", results["median_issue_ratio"]),
    ]

    axs = axs.flatten()

    for i, (label, value) in enumerate(metrics):

        axs[i].bar(["median"], [value])
        axs[i].set_title(label)

        axs[i].text(0, value, f"{value:.2f}", ha="center", va="bottom")

    # remove subplot vazio
    fig.delaxes(axs[5])

    plt.tight_layout()

    plt.savefig("repository_metrics.png")

    plt.close()


def plot_top_languages(language_freq):

    top = language_freq.most_common(100)

    languages = [x[0] for x in top]
    counts = [x[1] for x in top]

    plt.figure(figsize=(12, 6))

    plt.bar(languages, counts)

    plt.title("Top 100 Programming Languages")
    plt.ylabel("Number of Repositories")

    plt.xticks(rotation=90)

    plt.tight_layout()

    plt.savefig("top_languages.png")

    plt.close()

# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":

    data = load_data("repos.csv")

    results, language_freq = compute_metrics(data)

    generate_analysis_csv(results, language_freq)

    plot_all_metrics(results)
    plot_top_languages(language_freq)