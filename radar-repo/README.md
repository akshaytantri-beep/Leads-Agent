# RADAR: AI Lead Discovery and Scoring

RADAR tells a small B2B sales team who to call first. Every morning one crew finds Indian small and medium businesses that are showing signs they are ready to buy. A second crew scores each lead against the ideal customer profile and sends the team one ranked sheet and one email. No prospect is contacted without a human approving it.

I designed both crews in CrewAI Studio; this repository holds the exported projects. Built on a zero budget, using a free tier search API.

## The business problem

A small sales team cannot research hundreds of companies by hand. It needs a short, ranked list of businesses that both fit the profile and are likely to buy now, refreshed every day.

## How it works

```
08:45 daily (CrewAI schedule)
        |
        v
LEAD DISCOVERY  (lead_discovery/)
1. Find 15 to 20 Indian SMEs in Healthcare, Manufacturing, Education or Tech
   showing buying signals: funding, hiring, expansion, digital projects
2. Research their decision makers and estimate company size
3. Write leads.csv, keeping only facts found in the research
4. Save a dated copy to OneDrive leads/archive/, then save leads/leads.csv
        |
        |  the new leads.csv triggers the next crew
        v
LEAD SCORING  (lead_scoring/)
1. Lead Data Analyst          checks the file for missing or incomplete records
2. RADAR Scoring Specialist   scores each lead and labels it HOT, WARM or WATCH
3. Sales Intelligence Reporter  writes a Google Sheet, shares it, sends ONE summary email
        |
        v
Sales team reviews HOT leads and approves any outreach
```

## Scoring rules

| Criterion | Points |
| --- | --- |
| Industry: Healthcare, Manufacturing, Education, Technology | 30; other industries 10 |
| Seniority: CEO, Founder, Co-Founder, Managing Director, CTO, CMO, COO, Operations Head | 35; Director, VP or Head of 25; Manager 15; other 5 |
| Company size: 50 to 500 employees | 35; 501 to 1,000: 25; 10 to 49: 15; other 5; not a number: 5 and flagged |

Total score ranges from 20 to 100. HOT is 71 or more, WARM is 40 to 70, WATCH is below 40. The scorer writes out all three part scores, so every total can be checked by hand. A row with missing or extra values is not scored and is marked FIX DATA.

## Design choices

- **Buying signals, not just fit.** Discovery looks for companies likely to buy now, not every company in the target industries.
- **Human in the loop.** The agents never contact a prospect. The email says plainly that human approval is required before any outreach.
- **No guessed contact details.** An email is recorded only if it appears on a public page, with that page's URL in Email_Source. Otherwise the field stays blank and the lead is flagged for manual lookup.
- **Consistent scores.** All three scoring agents run at temperature 0, so the same lead gets the same score every run, and the email's HOT count matches the list it sends.
- **No size, no HOT.** A lead whose company size is not a number scores 5 for size, so it cannot reach HOT on a guess.
- **A daily record.** Each day's leads are archived before leads.csv is replaced.
- **No secrets or personal data in the repo.** Keys and recipients come from environment variables; the sample leads are fictional.

## Changes made after review

The exported crews were reviewed before publishing. The following were changed:
- Discovery no longer asks for a fixed 30 or more leads, which encouraged padding.
- Company size is now an employee count, so it matches the scoring bands.
- Emails must come from a public page with a source URL; they are never guessed.
- Each day's file is archived.
- All three scoring agents run at temperature 0. An earlier run reported 4 HOT leads in the subject and listed 5 in the body, and scored several leads below what the rubric gives.
- Scores now show their three parts, founders count as top seniority, and the size bands no longer overlap at 500.
- The report must use the sheet link returned by the tool and must not claim attachments, after an earlier run reported a CSV attachment that was never sent.
- The score range was corrected to 20 to 100.
- Hard-coded email addresses were moved to an environment variable.

## Run it

Requires Python 3.10 to 3.13 and [uv](https://docs.astral.sh/uv/). Each crew is its own CrewAI project.

```bash
pip install uv
cd lead_discovery      # or lead_scoring
crewai install
cp ../.env.example .env   # add your keys
crewai run
```

The OneDrive, Google Sheets, Gmail and Google Drive steps use CrewAI platform apps, so they need a CrewAI account with those integrations connected. The 08:45 schedule and the OneDrive file trigger are set on the CrewAI platform. `sample_data/leads.csv` shows the file format the two crews share.

## Testing

Each crew has smoke tests that build the crew and check its wiring without calling any API:

```bash
cd lead_scoring        # or lead_discovery
uv run --with pytest pytest
```

What has been checked: both crews install from their lock files, build without errors, and run until their first call to the language model. What needs real credentials to check: the language model calls, Serper search and the CrewAI platform apps for OneDrive, Google Sheets, Gmail and Google Drive.

## Project layout

```
lead_discovery/src/indian_msme_lead_discovery/
  config/agents.yaml    the discovery agent
  config/tasks.yaml     the four discovery steps
  crew.py               model, search and page reading tools
lead_scoring/src/radar_lead_scoring/
  config/agents.yaml    the three scoring agents
  config/tasks.yaml     the three tasks and the scoring rules
  crew.py               models, apps and the sequential process
*/tests/test_crew.py    smoke tests for each crew
sample_data/leads.csv   fictional leads in the shared format
```
