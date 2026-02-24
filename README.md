# Python Prompt AI APIs

## I. Entry scripts
- `main_chatgpt.py` - explore
    - https://developers.openai.com/api/docs
    - https://python.useinstructor.com/integrations/openai-responses/
    - https://github.com/Jaimboh/OpenAI-Responses-API/blob/main/06-web-search.py
    - https://medium.com/@odhitom09/openai-responses-api-a-comprehensive-guide-ad546132b2ed

- `main_chat_gub.py` - working script
- `main_gemini` - explore
- `main_gemini_sp.py` - working script


## II. `main_chat_gub.py`
Fetch candidates, parties, top 5 issues, and websites for all candidates
https://github.com/openai/openai-python for the API


## II. `main_gemini_sp.py`
Fetch analysts' consensus bottom-up projections of quarterly earnings for the S&P indexes:
1. Please make two tables. The first table should have 12 columns and 4 rows. The 12 columns should represent all 4 quarters for the 3 years 2025, 2026, and 2027. The 4 rows should contain either actual quarterly reported earnings per share or analysts' current consensus bottom-up projections of quarterly reported earnings per share for the standard & poor's 500 index, 400 index, 600 index, and 1500 index for all 4 quarters for the 3 years 2025, 2026, and 2027. The second table should have 12 columns and 11 rows. The 12 columns should represent all 4 quarters for the 3 years 2025, 2026, and 2027. The 11 rows should contain quarterly actual or consensus bottom-up projections of quarterly reported per share for the 11 sectors of the S&P 500 for all 4 quarters for the 3 years 025, 2026, and 2027.
2. Please make two tables. The first table should have 12 columns and 4 rows. The 12 columns should represent all 4 quarters for the 3 years 2025, 2026, and 2027. The 4 rows should contain either actual quarterly operating earnings per share or analysts' current consensus bottom-up projections of quarterly operating earnings per share for the standard & poor's 500 index, 400 index, 600 index, and 1500 index for all 4 quarters for the 3 years 2025, 2026, and 2027. The second table should have 12 columns and 11 rows. The 12 columns should represent all 4 quarters for the 3 years 2025, 2026, and 2027. The 11 rows should contain quarterly actual or consensus bottom-up projections of quarterly operating earnings per share for the 11 sectors of the S&P 500 for all 4 quarters for the 3 years 025, 2026, and 2027.
3. Please make two tables. The first table should have 12 columns and 4 rows. The 12 columns should represent all 4 quarters for the 3 years 2025, 2026, and 2027. The 4 rows should contain either actual quarterly revenues per share or analysts' current consensus bottom-up projections of quarterly revenues per share for the standard & poor's 500 index, 400 index, 600 index, and 1500 index for all 4 quarters for the 3 years 2025, 2026, and 2027. The second table should have 12 columns and 11 rows. The 12 columns should represent all 4 quarters for the 3 years 2025, 2026, and 2027. The 11 rows should contain quarterly actual or consensus bottom-up projections of quarterly revenues for the 11 sectors of the S&P 500 for all 4 quarters for the 3 years 025, 2026, and 2027.

### III. TIPS and Extensions
#### A. tutorial for using chatgpt
https://realpython.com/chatgpt-api-python/

#### B. openai api key
1. `openai.com`
    - login to API platform (pull-down)
    - with Apple
2. Dashboard (upper right) if necessary
3. (Settings) Gear icon (upper right)
4. API Keys (in left gutter, near top)
5. Copy and store key in `environment.py` inside the uv project file

#### C. chatgpt table extractor
- https://chatgpt.com/g/g-HBmy1I0iS-table-extractor
- Extract values from PDF or images into CSV files. If there are several tables in the file, precise exactly which table (table number, title and page) you want to extract data from.

#### D. using gemini
1. duckduckgo search: "python gemini api cookbook"
    - https://ai.google.dev/gemini-api/cookbook
    - https://github.com/google-gemini/cookbook
    - https://ai.google.dev/gemini-api/docs
    - ...
2. ddg search: "python prompt for gemini"
    - https://ai.google.dev/gemini-api/docs/prompting-strategies
    - https://projectpy.com/building-a-python-guide-for-text-generation-with/
    - ...

#### E. crontab
1. spaces in crontab
    - separate *, 2, *, *, and *
    - separate a, b, c, and d
2. a uv project may be run from any directory by using commands like b, c, and d above.
3. `crontab -e` opens the crontab file in a vim editor.
    - the editor opens in command mode
    - `i` opens the insert mode, which permits editing
    - `esc` returns to command mode
    - in command mode, 
        - `:w` saves the file
        - `:q` closes the file
        - `:wq` saves and closes
4. In main.py(), each CLI command is a list that contains two str:
    - first, the command itself which is the full path to `brew` (use `which brew`)
    - second, any args `brew` requires
5. If upgrade fails (e.g. permission for ghostscript), run `brew doctor`

#### F. web addresses
1. FactSet Earnings Insight Report
    - https://advantage.factset.com/hubfs/Website/Resources%20Section/Research%20Desk/Earnings%20Insight/EarningsInsight_021326.pdf
    - https://insight.factset.com

