import requests
import os
import csv
import time
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

token = os.getenv("GITHUB_TOKEN")

GITHUB_API = "https://api.github.com/graphql"

headers = {
    "Authorization": f"Bearer {token}"
}

# -----------------------------
# QUERY PARA LISTAR REPOSITÓRIOS
# -----------------------------
list_query = """
query ($cursor: String) {
  search(query: "stars:>10000 sort:stars-desc", type: REPOSITORY, first: 100, after: $cursor) {
    pageInfo {
      endCursor
      hasNextPage
    }
    nodes {
      ... on Repository {
        name
        owner { login }
      }
    }
  }
}
"""

# -----------------------------
# QUERY PARA DETALHES
# -----------------------------
detail_query = """
query ($owner: String!, $name: String!) {
  repository(owner: $owner, name: $name) {
    name
    createdAt
    pushedAt
    primaryLanguage { name }
    releases { totalCount }
    pullRequests(states: MERGED) { totalCount }
    closedIssues: issues(states: CLOSED) { totalCount }
    totalIssues: issues { totalCount }
  }
}
"""


def run_query(query, variables):

    retries = 0

    while retries < 5:

        response = requests.post(
            GITHUB_API,
            json={"query": query, "variables": variables},
            headers=headers
        )

        if response.status_code == 200:
            return response.json()

        print("Erro:", response.status_code, "- tentativa", retries + 1)

        retries += 1
        time.sleep(5 * retries)

    raise Exception("Falha após várias tentativas")


# -----------------------------
# COLETAR LISTA DE REPOSITÓRIOS
# -----------------------------
def get_repo_list(num_repos):

    repos = []
    cursor = None

    while len(repos) < num_repos:

        print("Buscando lista:", len(repos))

        variables = {"cursor": cursor}

        data = run_query(list_query, variables)

        nodes = data["data"]["search"]["nodes"]

        repos.extend(nodes)

        page_info = data["data"]["search"]["pageInfo"]

        cursor = page_info["endCursor"]

        if not page_info["hasNextPage"]:
            break

        time.sleep(1)

    return repos[:num_repos]


# -----------------------------
# COLETAR DETALHES
# -----------------------------
def get_repo_details(repo_list):

    results = []

    for i, repo in enumerate(repo_list):

        if i % 10 == 0:
            print("Coletando:", i)

        variables = {
            "owner": repo["owner"]["login"],
            "name": repo["name"]
        }

        data = run_query(detail_query, variables)

        repo_data = data["data"]["repository"]

        results.append(repo_data)

        time.sleep(0.5)

    return results


# -----------------------------
# GERAR CSV
# -----------------------------
def generate_csv(repos):

    with open("repos.csv", "w", newline="", encoding="utf-8") as f:

        writer = csv.writer(f)

        writer.writerow([
            "repo",
            "age_days",
            "merged_prs",
            "releases",
            "last_update_days",
            "language",
            "closed_issue_ratio"
        ])

        for repo in repos:

            created = datetime.fromisoformat(repo["createdAt"].replace("Z", ""))
            pushed = datetime.fromisoformat(repo["pushedAt"].replace("Z", ""))

            age_days = (datetime.now() - created).days
            last_update_days = (datetime.now() - pushed).days

            prs = repo["pullRequests"]["totalCount"]
            releases = repo["releases"]["totalCount"]

            closed_issues = repo["closedIssues"]["totalCount"]
            total_issues = repo["totalIssues"]["totalCount"]

            language = None
            if repo["primaryLanguage"]:
                language = repo["primaryLanguage"]["name"]

            issue_ratio = 0
            if total_issues > 0:
                issue_ratio = closed_issues / total_issues

            writer.writerow([
                repo["name"],
                age_days,
                prs,
                releases,
                last_update_days,
                language,
                issue_ratio
            ])


# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":

    NUM_REPOS = 1000

    try:

        repo_list = get_repo_list(NUM_REPOS)

        print("Repos coletados:", len(repo_list))

        repo_details = get_repo_details(repo_list)

        generate_csv(repo_details)

        print("CSV gerado com sucesso!")

    except Exception as e:
        print("Erro:", e)