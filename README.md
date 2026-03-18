# Python: AI APIs for ChatGPT and Gemini
### March 16, 2026

## 0. Introduction

### A. The `main` programs produces .txt output in markdown formats

### B. The Web prompts and the API prompts produce different responses.
- See I.F

### C. To convert the response documents to .html documents: `md_to_html_scripts`
1. The following programs were created by ChatGPT
2. `pretty-markdown-viewer.html` produces .webarchive files from the markdowns
3. `webarchive_to_html.py` converts to html, producing a file
    - To create this program:
        - Prompt: "How do I open a local webarchive file in Win 11"
        - Then agree to Chat's offer to write the code in python
        - Additional prompt: "yea. do the next step"
    - With the .webarchive files in ".../Documents/"
    - `uv run webarchive_to_html.py ".../Documents/chat_trieste.webarchive" -o ".../Documents/chat_trieste"`
    - `uv run webarchive_to_html.py ".../Documents/gem_trieste.webarchive" -o ".../Documents/gem_trieste"`
        - double-click `index.html` in the output file to open in the browser
        - `assets` includes code for the .html file
    - Copies of these output folders appear here in `output_files/trieste`
4. `md_to_html.py`
    - One step from markdown to html
    - But the results are cruder than the two-step (2. & 3. above)

## I. Entry scripts

### A. `main_chatgpt.py` - explore

1. https://developers.openai.com/api/docs (API pull-down menu at top of window)
2. https://python.useinstructor.com/integrations/openai-responses/
3. https://github.com/Jaimboh/OpenAI-Responses-API/blob/main/06-web-search.py
4. https://medium.com/@odhitom09/openai-responses-api-a-comprehensive-guide-ad546132b2ed
5. https://developers.openai.com/api/reference/python/resources/responses/methods/retrieve

### B. `main_chat_gub.py` - working script

### C. `main_chat_gub_report.py` - makes response more readable

### D. `main_chat_trieste.py` - working script
- `output_files/trieste/chat...`

### E. `main_gemini` - explore
1. https://ai.google.dev/gemini-api/docs/quickstart
2. https://ai.google.dev/gemini-api/docs
3. https://ai.google.dev/gemini-api/docs/tools
4. https://ai.google.dev/gemini-api/docs/langgraph-exampl
5. gemini api how to provided input file to a request

### F. `main_gemini_sp500.py` - working script
1. NB: the three prompts yield no results in this program
    - denied access to SP data
    - cannot find the specific series in FactSet. John Butters data
2. The three prompts do yield results in the web tool (thinking, not fast)
    - The web tool's setting, thinking, might default to high
    - The API specified `thinking_level= 'high'`
    - https://ai.google.dev/gemini-api/docs/thinking
3. The API's response suggests using FactSet (see III.G below)
4. I prompted Gemini to use FactSet in the API and on the web
5. Only the web tool produced results
6. API would not infer data from public docs, even with thinking_level= 'high'
    - see output_files/sp_500/gem_sp500_response_2026_03_16.txt

### G. `main_gemini_trieste.py` - working script 
- `output_files/trieste/gem...`

### H. `pretty-markdown-viewer.html` - converts .txt files to webarchives
1. open this file with a browser
2. open the `response` file from AI in the resulting web page
3. converts response to a webarchive and saves it
4. webarchive can be opened as a pretty webpage by Safari

### I. `webarchive_to_html.py` - converts webarchive to .html for other browsers
1. Results appear in `output_files/trieste/...`
    - `chat_trieste`
    - `gem_trieste`
2. Double-click `index.html`

### J. `md_to_html.py` - produces html without the intermediate .webarchive step
1. One step instead of two to the html document
2. But the result looks cruder than the two-step (H. & I.) procedure


## II. Prompts

### A. `main_chat_gub.py`
Fetch candidates, parties, top 5 issues, and websites for all candidates
https://github.com/openai/openai-python for the API

```
Who are the candidates running for governor of the US State of Maine in 2026? Create a table in markdown format 
    with 4 columns and a row for each candidate. The 4 columns for each candidate should be labeled: 
    "name", "party affiliation", "top 5 issues", "web sites".
    In each row, separate the entries for the 4 columns with the "|" symbol.
        
    For the "name" column of the markdown output table:
    The content input csv file shows an initial list of candidates. There might be more candidates. Scrape the web sites 
    of the Portland Press Herald to find any other candidates who do not appear in the content input csv file. 
    Also, scrape the web sites of the Portland Press Herald to find the names of candidates who have withdrawn 
    from running for governor.
        
    For the "party affiliation" column of the markdown output table: 
    The second column of the content input csv file shows the candidate's party affiliation. 
    If this information is not available in the input csv file, inspect the candidate's home web page shown in the 
    content input csv file to extract the candidate's party affiliation. If the home web page is not available in the 
    input csv file, search the web for the candidate's home web page and extract the candidate's party affiliation.
        
    For the "top 5 issues" column of the markdown output table:
    Extract the top 5 issues for each candidate by reading the content of the candidate's statement shown in the 
    content csv input file, by reading the content of the candidate's home web page, by reading the content 
    of the web addresses shown in the websites column of the content input csv file, and by reading the content of 
    relevant Portland Press Herald profiles and articles that you find by searching the web.
        
    For the "web sites" column of the markdown output table:
    For each candidate, show a list of web addresses that contains the web address for the candidate's homepage followed 
    by other web addresses that show the candidate's top 5 issues.
```

### B. `main_gemini_sp500.py`
Fetch analysts' consensus bottom-up projections of quarterly earnings for the S&P indexes:
1. Please make two tables. The first table should have 12 columns and 4 rows. The 12 columns should represent all 4 quarters for the 3 years 2025, 2026, and 2027. The 4 rows should contain either actual quarterly reported earnings per share or analysts' current consensus bottom-up projections of quarterly reported earnings per share for the standard & poor's 500 index, 400 index, 600 index, and 1500 index for all 4 quarters for the 3 years 2025, 2026, and 2027. The second table should have 12 columns and 11 rows. The 12 columns should represent all 4 quarters for the 3 years 2025, 2026, and 2027. The 11 rows should contain quarterly actual or consensus bottom-up projections of quarterly reported per share for the 11 sectors of the S&P 500 for all 4 quarters for the 3 years 025, 2026, and 2027. Please only use data from S&P Global Market Intelligence.
2. Please make two tables. The first table should have 12 columns and 4 rows. The 12 columns should represent all 4 quarters for the 3 years 2025, 2026, and 2027. The 4 rows should contain either actual quarterly operating earnings per share or analysts' current consensus bottom-up projections of quarterly operating earnings per share for the standard & poor's 500 index, 400 index, 600 index, and 1500 index for all 4 quarters for the 3 years 2025, 2026, and 2027. The second table should have 12 columns and 11 rows. The 12 columns should represent all 4 quarters for the 3 years 2025, 2026, and 2027. The 11 rows should contain quarterly actual or consensus bottom-up projections of quarterly operating earnings per share for the 11 sectors of the S&P 500 for all 4 quarters for the 3 years 025, 2026, and 2027. Please only use data from S&P Global Market Intelligence.
3. Please make two tables. The first table should have 12 columns and 4 rows. The 12 columns should represent all 4 quarters for the 3 years 2025, 2026, and 2027. The 4 rows should contain either actual quarterly revenues per share or analysts' current consensus bottom-up projections of quarterly revenues per share for the standard & poor's 500 index, 400 index, 600 index, and 1500 index for all 4 quarters for the 3 years 2025, 2026, and 2027. The second table should have 12 columns and 11 rows. The 12 columns should represent all 4 quarters for the 3 years 2025, 2026, and 2027. The 11 rows should contain quarterly actual or consensus bottom-up projections of quarterly revenues for the 11 sectors of the S&P 500 for all 4 quarters for the 3 years 025, 2026, and 2027. Please only use data from S&P Global Market Intelligence.

### C. `main_chat_trieste.py` `main_gemini_trieste.py`
```
I am a tourist traveling to Trieste, Italy for the first time. Please make 3 tables.
    The first table should show hotels. 
    Each hotel's information should appear in a separate row of the the table, and the table should have 11 columns that show: 
    name; address; rating; typical room daily rate in US dollars; proximity to Trieste center in miles; 
    if member of a hotel group name of group brand; prominent nearby attractions; exposure to noise; has free wifi yes or no; 
    has free breakfast yes or no; has restaurant yes or no. 
    This first table should show only the top 12 hotels, and should order these top 12 hotels, 
    from the highest rated in the first row to the lowest rated in the last row. 
    The second table should show important attractions near the Trieste. 
    Each attraction's details should appear in a separate row of the table, and the table should have 6 columns that show: 
    name, importance of attraction, distance from Trieste center in miles; 
    home web site for the attraction. description of attraction, names of nearby restaurants. 
    The second table should order the attractions, from the most important attraction in the first row to the least important in the last row. 
    The third table should show highly-rated restaurants near Trieste. 
    Each restaurant's details should appear in a separate row of the table, and the table should have 7 columns that show: 
    name, address, home web site, rating of the restaurant, description of cuisine, distance from Trieste center in miles; 
    names of nearby attractions. The table should order the restaurants, from the highest rating in the first row to the lowest rating in the last row. 
    The user's uploaded Trieste_travel_sites.txt file contains a list of web sites to include in your search. 
    Please show these sites explicitly in your sources listed in your response, if you used information from these sites. 
    Please search additional relevant websites. Please show the web addresses of all sources that you used to make each table.
    Please format your entire response using markdown.
```

## III. TIPS and Extensions

### A. tutorial for using chatgpt

    - https://realpython.com/chatgpt-api-python/

### B. openai api key
1. `openai.com`
    - login to API platform (pull-down)
    - with Apple
2. Dashboard (upper right) if necessary
3. (Settings) Gear icon (upper right)
4. API Keys (in left gutter, near top)
5. Copy and store key in `environment.py` inside the uv project file

### C. chatgpt table extractor
1. https://chatgpt.com/g/g-HBmy1I0iS-table-extractor
2. Extract values from PDF or images into CSV files. If there are several tables in the file, precise exactly which table (table number, title and page) you want to extract data from.

### D. using gemini
1. duckduckgo search: "python gemini api cookbook"
    - https://ai.google.dev/gemini-api/cookbook
    - https://github.com/google-gemini/cookbook
    - https://ai.google.dev/gemini-api/docs
    - ...
2. duckduckgo search: "python prompt for gemini"
    - https://ai.google.dev/gemini-api/docs/prompting-strategies
    - https://projectpy.com/building-a-python-guide-for-text-generation-with/
    - ...

### E. format responses
1. see I.G. above
2. TODO: experiment with other formats for AI's response files

### F. crontab
1. Does not reference this project
2. `main_gemini_sp500.py` was the only candidate, but the API would not fetch
3. ChatGPT (API and web tool) would not fetch for lack of an access key

### G. web addresses
1. FactSet Earnings Insight Report
    - https://advantage.factset.com/hubfs/Website/Resources%20Section/Research%20Desk/Earnings%20Insight/EarningsInsight_021326.pdf
    - https://insight.factset.com

