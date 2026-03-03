def query_example():
  """
  This is just an example query to showcase the format of submission
  Please format the query in Bigquery console and paste it here.
  Submission starts from query_one.
  """
  return """
SELECT
 repo_name,
 author.name AS author_name,
FROM
 `bigquery-public-data.github_repos.sample_commits`;
  """

def query_one():
    """Query one"""
    return """
SELECT author.name AS name, COUNT(*) AS count
FROM `bigquery-public-data.github_repos.sample_commits`
GROUP BY author.name, author.email
ORDER BY count DESC
LIMIT 10
    """

def query_two():
    """Query two"""
    return """
SELECT license, COUNT(*) AS count
FROM `bigquery-public-data.github_repos.licenses`
GROUP BY license
ORDER BY count DESC
LIMIT 10
    """

def query_three():
    """Query three"""
    return """
SELECT
  CASE
    WHEN license LIKE '%gpl%' THEN 'gpl'
    WHEN license LIKE '%bsd%' THEN 'bsd'
    WHEN license LIKE '%mit%' THEN 'mit'
    ELSE 'other'
  END AS family,
  COUNT(*) AS count
FROM `bigquery-public-data.github_repos.licenses`
GROUP BY family
ORDER BY count DESC
    """

def query_four():
    """Query four"""
    return """
SELECT lang.name AS name, COUNT(*) AS count
FROM `bigquery-public-data.github_repos.languages`, UNNEST(language) AS lang
GROUP BY name
ORDER BY count DESC
LIMIT 10
    """

def query_five():
    """Query five"""
    return """
WITH repo_totals AS (
  SELECT repo_name,
    lang.name AS name,
    lang.bytes AS bytes,
    SUM(lang.bytes) OVER (PARTITION BY repo_name) AS total_bytes
  FROM `bigquery-public-data.github_repos.languages`, UNNEST(language) AS lang
)
SELECT name, COUNT(*) AS count
FROM repo_totals
WHERE bytes >= 0.5 * total_bytes
GROUP BY name
ORDER BY count DESC, name DESC
    """

def query_six():
    """Query six"""
    return """
SELECT lang.name AS name, MAX_BY(l.repo_name, r.watch_count) AS repo_name
FROM `bigquery-public-data.github_repos.languages` l, UNNEST(l.language) AS lang
JOIN `bigquery-public-data.github_repos.sample_repos` r
ON l.repo_name = r.repo_name
GROUP BY lang.name
ORDER BY name DESC
    """

def query_seven():
    """Query seven"""
    return """
WITH top_repos AS (
  SELECT repo_name
  FROM `bigquery-public-data.github_repos.sample_repos`
  ORDER BY watch_count DESC
  LIMIT 100
)
SELECT lang.name AS name, COUNT(*) AS occurance
FROM `bigquery-public-data.github_repos.languages` l, UNNEST(l.language) AS lang
JOIN top_repos t ON l.repo_name = t.repo_name
GROUP BY lang.name
ORDER BY occurance DESC, name DESC
    """

def query_eight():
    """Query eight"""
    return """
WITH repo_commits AS (
  SELECT repo_name, COUNT(*) AS commit_count
  FROM `bigquery-public-data.github_repos.sample_commits`
  GROUP BY repo_name
)
SELECT lang.name AS name, MAX_BY(l.repo_name, rc.commit_count) AS repo_name
FROM `bigquery-public-data.github_repos.languages` l, UNNEST(l.language) AS lang
JOIN repo_commits rc ON l.repo_name = rc.repo_name
GROUP BY lang.name
ORDER BY MAX(rc.commit_count) DESC, name DESC
    """

def query_nine():
    """Query nine"""
    return """
SELECT EXTRACT(YEAR FROM committer.date) AS year, COUNT(*) AS count
FROM `bigquery-public-data.github_repos.sample_commits`
GROUP BY year
ORDER BY year DESC
    """

def query_ten():
    """Query ten"""
    return """
SELECT EXTRACT(DAYOFWEEK FROM committer.date) AS day_num, COUNT(*) AS count
FROM `bigquery-public-data.github_repos.sample_commits`
GROUP BY day_num
ORDER BY count DESC
    """

def query_eleven():
    """Query eleven"""
    return """
WITH repo_commits AS (
  SELECT repo_name, COUNT(*) AS commit_count
  FROM `bigquery-public-data.github_repos.sample_commits`
  GROUP BY repo_name
),
buckets AS (
  SELECT
    CASE
      WHEN rc.commit_count >= 1000 THEN 'high'
      WHEN rc.commit_count >= 100 THEN 'medium'
      ELSE 'low'
    END AS activity_level,
    r.watch_count
  FROM repo_commits rc
  JOIN `bigquery-public-data.github_repos.sample_repos` r
  ON rc.repo_name = r.repo_name
),
levels AS (
  SELECT 'high' AS activity_level, 1 AS sort_order
  UNION ALL SELECT 'medium', 2
  UNION ALL SELECT 'low', 3
)
SELECT l.activity_level,
  AVG(b.watch_count) AS avg_watch,
  APPROX_QUANTILES(b.watch_count, 2)[OFFSET(1)] AS median_watch
FROM levels l
LEFT JOIN buckets b ON l.activity_level = b.activity_level
GROUP BY l.activity_level, l.sort_order
ORDER BY l.sort_order
    """


def query_twelve():
    """Query twelve"""
    return """
WITH author_repo AS (
  SELECT
    author.name AS author_name,
    author.email AS author_email,
    repo_name,
    COUNT(*) AS repo_commits
  FROM `bigquery-public-data.github_repos.sample_commits`
  GROUP BY author.name, author.email, repo_name
),
author_totals AS (
  SELECT
    author_name,
    author_email,
    SUM(repo_commits) AS commit_count
  FROM author_repo
  GROUP BY author_name, author_email
  ORDER BY commit_count DESC
  LIMIT 10
)
SELECT
  t.author_name,
  t.commit_count,
  MAX_BY(a.repo_name, a.repo_commits) AS repo_name
FROM author_totals t
JOIN author_repo a
  ON t.author_name = a.author_name
  AND t.author_email = a.author_email
GROUP BY t.author_name, t.commit_count
ORDER BY t.commit_count DESC
    """

def query_thirteen():
    """Query thirteen"""
    return """
SELECT
  repo_name,
  ROUND(
    COUNTIF(author.name = committer.name AND author.email = committer.email)
    / COUNT(*),
    2
  ) AS ratio
FROM `bigquery-public-data.github_repos.sample_commits`
GROUP BY repo_name
ORDER BY repo_name DESC
    """

def query_fourteen():
    """Query fourteen"""
    return """
WITH top_authors AS (
    SELECT repo_name, MAX_BY(author_name, cnt) AS author_name
    FROM (
        SELECT repo_name, author.name AS author_name, COUNT(*) AS cnt
        FROM `bigquery-public-data.github_repos.sample_commits`
        GROUP BY repo_name, author.name, author.email
    )
    GROUP BY repo_name
),
top_committers AS (
    SELECT repo_name, MAX_BY(committer_name, cnt) AS committer_name
    FROM (
        SELECT repo_name, committer.name AS committer_name, COUNT(*) AS cnt
        FROM `bigquery-public-data.github_repos.sample_commits`
        GROUP BY repo_name, committer.name, committer.email
    )
    GROUP BY repo_name
),
top_languages AS (
    SELECT repo_name, MAX_BY(lang.name, lang.bytes) AS language
    FROM `bigquery-public-data.github_repos.languages`, UNNEST(language) AS lang
    GROUP BY repo_name
)
SELECT a.repo_name, a.author_name, c.committer_name, l.language
FROM top_authors a
JOIN top_committers c ON a.repo_name = c.repo_name
JOIN top_languages l ON a.repo_name = l.repo_name
ORDER BY a.repo_name DESC
    """

def query_fifteen():
    """Query fifteen"""
    return """
WITH mit_repos AS (
    SELECT l.repo_name, l.license, r.watch_count
    FROM `bigquery-public-data.github_repos.licenses` l
    JOIN `bigquery-public-data.github_repos.sample_repos` r ON l.repo_name = r.repo_name
    WHERE l.license = 'mit' AND r.watch_count >= 8000
),
author_commits AS (
    SELECT repo_name, author.name AS author_name, COUNT(*) AS cnt
    FROM `bigquery-public-data.github_repos.sample_commits`
    GROUP BY repo_name, author.name, author.email
)
SELECT m.repo_name, m.license, m.watch_count, MAX_BY(a.author_name, a.cnt) AS author_name
FROM mit_repos m
JOIN author_commits a ON m.repo_name = a.repo_name
GROUP BY m.repo_name, m.license, m.watch_count
ORDER BY m.repo_name DESC
    """
