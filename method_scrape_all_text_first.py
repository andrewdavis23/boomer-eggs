import urllib.request
import scrapy
import pandas as pd
import re
from datetime import datetime

# Trim html tags
def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', str(raw_html))
  return cleantext

# Returns the selector object that xpaths will extract from
def create_selector(url):
    # get web page
    fp = urllib.request.urlopen(url)
    mybytes = fp.read()

    # decode
    html = mybytes.decode("utf8")
    fp.close()

    # create selector object
    sel = scrapy.Selector(text=html)
    return sel

# Create a list of all tickers from text file
with open("c:/Users/nuajd15/Documents/scrapers/mutualFunds/USD_MF.txt", "r") as grilled_cheese:
	tickers_raw = grilled_cheese.readlines()
clean_me = lambda x : x.replace("\n","")
ticker_list = list(map(clean_me, tickers_raw))

# Errors for later printing/writing
errors = []
def error(s):
    time = str(datetime.now())
    errors.append(time+' '+s)
    print('>>> '+time+s)

# Modify ticket list for reruns/tests
ticker_list = ticker_list[800:900]

# PAGENAME_data functions create col,val vals
def summary_data(ticker):
    vals = []
    cols = []
    url = "https://finance.yahoo.com/quote/"+ticker

    path = '//td//text()'
    sel = create_selector(url)
    extract = sel.xpath(path).extract()

    # pop the second set of stars after morning star, sustainability rating not text (ironically unsustainably)
    extract.pop(extract.index('Morningstar Rating')+2)
    extract.remove('Sustainability Rating')
    
    # one table on page, no header
    start = extract.index('Previous Close')

    row_len = 15
    j = start
    k = start + 1
    for i in range(row_len):
            cols.append(extract[j])
            vals.append(extract[k])
            j+=2
            k+=2
    return cols, vals

def profile_data(ticker):
    cols = []
    vals = []
    url = "https://finance.yahoo.com/quote/"+ticker+"/profile?p="+ticker

    path = '//span/text()'
    sel = create_selector(url)
    extract = sel.xpath(path).extract()

    # [table_name,#rows,#extract_method(if-else)]
    profile_page = [['Fund Overview',7,1],['Fund Operations',4,1],['Fees & Expenses',9,2]]

    for table in profile_page:
        start = extract.index(table[0])
        row = table[1]
        method = table[2]
        if method == 1:
            j = start + 1
            k = j + 1
            for i in range(row):
                cols.append(extract[j])
                vals.append(extract[k])
                j+=2
                k+=2
        elif method == 2:
            j = start + 4
            k = j + 1
            l = k + 1
            for i in range(row):
                cols.append(extract[j]+'_FUND')
                cols.append(extract[j]+'_CAT')
                vals.append(extract[k])
                vals.append(extract[l])
                j+=3
                k+=3
                l+=3
        else:
            print('\n---- Scraper did not recognize table\n---- table',table,'\n----   url',url,'\n')
            continue
    return cols, vals

def performance_data(ticker):
    cols = []
    vals = []
    url = "https://finance.yahoo.com/quote/"+ticker+"/performance?p="+ticker

    path = '//span/text()'
    sel = create_selector(url)
    extract = sel.xpath(path).extract()

    # [table_name,#rows,#extract_method(if-else)]
    profile_page = [['Performance Overview',9,1],['Trailing Returns (%) Vs. Benchmarks',9,2],['Annual Total Return (%) History',4,2],['Past Quarterly Returns (%)',4,4]]

    for table in profile_page:
        start = extract.index(table[0])
        row = table[1]
        method = table[2]
        # 1 column
        if method == 1:
            j = start + 1
            k = j + 1
            for i in range(row):
                cols.append(extract[j])
                vals.append(extract[k])
                j+=2
                k+=2
        # 2 column
        elif method == 2:
            j = start + 4
            k = j + 1
            l = k + 1
            for i in range(row):
                cols.append(extract[j]+'_FUND')
                cols.append(extract[j]+'_CAT')
                vals.append(extract[k])
                vals.append(extract[l])
                j+=3
                k+=3
                l+=3
        # 4 column
        elif method == 4:
            j = start + 6
            k = j + 1
            l = k + 1
            m = l + 1
            n = m + 1
            for i in range(row):
                cols.append(extract[j]+'_Q1')
                cols.append(extract[j]+'_Q2')
                cols.append(extract[j]+'_Q3')
                cols.append(extract[j]+'_Q4')
                vals.append(extract[k])
                vals.append(extract[l])
                vals.append(extract[m])
                vals.append(extract[n])
        else:
            print('\n---- Scraper did not recognize table\n---- table',table,'\n----   url',url,'\n')
            continue
    return cols, vals

# variables for dataframe, error file and progression monitoring
columns=['Previous Close', 'YTD Return', 'Expense Ratio (net)', 'Category', 'Last Cap Gain', 'Morningstar Rating', 'Morningstar Risk Rating', 'Net Assets', 'Beta (5Y Monthly)', 'Yield', '5y Average Return', 'Holdings Turnover', 'Last Dividend', 'Average for Category', 'Inception Date', 'Category', 'Fund Family', 'Net Assets', 'YTD Return', 'Yield', 'Morningstar Rating', 'Inception Date', 'Last Dividend', 'Last Cap Gain', 'Holdings Turnover', 'Average for Category', 'Annual Report Expense Ratio (net)_FUND', 'Annual Report Expense Ratio (net)_CAT', 'Prospectus Net Expense Ratio_FUND', 'Prospectus Net Expense Ratio_CAT', 'Prospectus Gross Expense Ratio_FUND', 'Prospectus Gross Expense Ratio_CAT', 'Max 12b1 Fee_FUND', 'Max 12b1 Fee_CAT', 'Max Front End Sales Load_FUND', 'Max Front End Sales Load_CAT', 'Max Deferred Sales Load_FUND', 'Max Deferred Sales Load_CAT', '3 Yr Expense Projection_FUND', '3 Yr Expense Projection_CAT', '5 Yr Expense Projection_FUND', '5 Yr Expense Projection_CAT', '10 Yr Expense Projection_FUND', '10 Yr Expense Projection_CAT', 'Morningstar Return Rating', 'Year-to-Date Return', '5-Year Average Return', 'Number of Years Up', 'Number of Years Down', 'Best 1 Yr Total Return (Feb 3, 2019)', 'Worst 1 Yr Total Return (Feb 3, 2019)', 'Best 3-Yr Total Return', 'Worst 3-Yr Total Return', 'YTD_FUND', 'YTD_CAT', '1-Month_FUND', '1-Month_CAT', '3-Month_FUND', '3-Month_CAT', '1-Year_FUND', '1-Year_CAT', '3-Year_FUND', '3-Year_CAT', '5-Year_FUND', '5-Year_CAT', '10-Year_FUND', '10-Year_CAT', 'Last Bull Market_FUND', 'Last Bull Market_CAT', 'Last Bear Market_FUND', 'Last Bear Market_CAT', '2020_FUND', '2020_CAT', '2019_FUND', '2019_CAT', '2018_FUND', '2018_CAT', '2017_FUND', '2017_CAT', '2020_Q1', '2020_Q2', '2020_Q3', '2020_Q4', '2020_Q1', '2020_Q2', '2020_Q3', '2020_Q4', '2020_Q1', '2020_Q2', '2020_Q3', '2020_Q4', '2020_Q1', '2020_Q2', '2020_Q3', '2020_Q4']
row_dict = {}
bad_rows = {}
cnt = 0
tot = len(ticker_list)

print('\n\n '+chr(128376)+' beginning crawl\t\t',str(datetime.now()))

try:
    # Remember which range is scanned, for a retry
    first_ticker = 1
    last_ticker = cnt

    for ticker in ticker_list:
        # progress
        cnt+=1
        pet = chr(128375)
        petCrawl = pet+' ' if cnt%2==0 else ' '+pet
        print(petCrawl+'  Scraping '+ticker+' '+str(cnt)+' of '+str(tot)+'\t'+str(round((cnt/tot)*100,3))+'%')
        # full row of data
        f_row = []
        f_col = []

        # get rows, cols
        summary_col, summary_row = summary_data(ticker)
        profile_col, profile_row = profile_data(ticker)
        performance_col, performance_row = performance_data(ticker)


        f_row.extend(summary_row)
        f_row.extend(profile_row)
        f_row.extend(performance_row)

        f_col.extend(summary_col)
        f_col.extend(profile_col)
        f_col.extend(performance_col)

        if len(f_row) == len(columns):
            row_dict[ticker] = f_row
        else:
            time = str(datetime.now())
            error(ticker+' row rejected. Iteration '+str(cnt)+'. Row length '+str(len(f_row)))
            bad_rows[ticker] = f_row
except:
    print('\nERROR: Crawl Ended Unexpectedly ----------------------- \n')
    time = str(datetime.now())
    errors.append('Crawl Ended at '+time)
    pass

# Create DataFrames
mf = pd.DataFrame.from_dict(row_dict, orient='index', columns=columns)
br = pd.DataFrame.from_dict(bad_rows, orient='index')

# ch
print('>>> rows collected = '+str(len(row_dict)))
print('>>> tickers check  = '+str(cnt))
print('--- Range of Funds Scanned - From Original Mutual Fund Full List')
print('>>> Start = '+str(first_ticker))
print('>>> Stop  = '+str(last_ticker))

# timestamp for filenames
time = str(datetime.now())
timestamp = time[0:10]+':'+time[12:19]
timestamp = timestamp.replace(':','_')

# save and print df.head()
print('\n>>> saving Mutual_Funds.csv...\n>>> preview...\n')
print(mf.head())
mf_title = r'C:\Users\nuajd15\Documents\scrapers\mutualFunds\csvOut\Mutual_Funds_{}.csv'.format(timestamp)
mf.to_csv(mf_title, index=False)

# print and write errors
print('\n>>> saving error log...\n')
for i in (errors):
    print(i)

f = open(r'C:\Users\nuajd15\Documents\scrapers\mutualFunds\csvOut\test_errors.txt', "a")
for i in errors:
  f.write(i+'\n')
f.close()

# saving bad rows collected
bad_rows_title = r'C:\Users\nuajd15\Documents\scrapers\mutualFunds\csvOut\Bad_Rows_{}.csv'.format(timestamp)
br.to_csv(bad_rows_title, index=False)

