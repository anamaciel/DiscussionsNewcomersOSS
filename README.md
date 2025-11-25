# Replication Package: GitHub Discussions in OSS Projects

## Study Information
This package supports the paper:  
**"Analysis of the Role of GitHub Discussions in Open Source Software Development Environment"**  

## 📂 Package Structure
```
.
├── data/ # Processed data
│   ├── discussions/ # Posts, comments, and answers (148K posts, 517K comments)
│   ├── issues_prs/ # Issues (1.6M) and pull requests (984K)
│   ├── contributors/ # Role classification (core, peripheral, etc.)
│   └── bots/
│       ├── known_bots.csv # List of 385 known bots (Chidambaram et al., 2023)
│       └── detected_bots/ # Bots identified by the "[bot]" suffix
├── scripts/ # Analysis scripts
│   ├── 1_data_processing.R
│   ├── 2_contributor_roles.R # RQ1
│   ├── 3_newcomer_onboarding.R # RQ2
│   ├── 4_activity_impact.R # RQ3
│   └── utils/ # Auxiliary functions
└── results/
    ├── tables/ # Statistical results (CSV)
    └── figures/ # Generated plots (PDF/PNG)
```

## Contents
### Data Files
- `discussions_data/`: Contains processed GitHub Discussions data (posts, comments, answers)
- `issues_prs_data/`: Includes issue and pull request records
- `contributors/`: Contributor classifications (core, peripheral, etc.)
- `bot_accounts.csv`: Identified bot accounts (385 known bots + [bot]-suffix accounts)

### Analysis Scripts (R)
1. `data_cleaning.R` - Filters and prepares raw data
2. `role_analysis.R` - Answers RQ1 (contributor roles in Discussions)
3. `onboarding_impact.R` - Answers RQ2 (newcomer onboarding changes)
4. `activity_analysis.R` - Answers RQ3 (issues/PRs activity impact)

### Output
- `tables/`: Statistical results in CSV format
- `figures/`: Generated plots (PDF/PNG)

## Replication Instructions
### 1. Requirements
- R (≥4.0) with these packages:
  ```r
  install.packages(c("lmerTest", "emmeans", "tidyverse", "lme4", "ggplot2"))
  ```

### 2. Execution Order
Run scripts sequentially:
```bash
Rscript data_cleaning.R
Rscript role_analysis.R
Rscript onboarding_impact.R
Rscript activity_analysis.R
```

### 3. Expected Outputs
- **RQ1**: ANOVA tables comparing contributor roles (Table 1-2 in paper)
- **RQ2**: RDD models for newcomer patterns (Table 6)
- **RQ3**: RDD models for activity changes (Table 7)

## Key Methodology Details
### Data Collection
285 GitHub projects meeting:
- ≥1,000 stars
- ≥1,000 commits (last in 2023)
- Created before 2019
- Using GitHub Discussions

### Statistical Models
Regression Discontinuity Design (RDD):
```math
y_i = α + β·time_i + γ·intervention_i + δ·time_after_intervention_i + η·controls_i + ε_i
```
- Excluded 30 days around Discussions adoption
- Controlled for project/language variability

### Bot Filtering
- Official GitHub bots ([bot]-suffix)
- Known bots list from Chidambaram et al. (2023)

### Notes
- Raw data was collected via GitHub API (REST + GraphQL) 
- All temporal analyses use 12-month windows
- Contributor roles are project-specific (a core dev in one project may be peripheral in another)

## License
CC-BY 4.0 International
