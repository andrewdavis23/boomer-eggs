# boomer-eggs
Yahoo Finance scrapper for mutual funds and etfs

## Steps:
1. Create list of mutual funds.  Each URL will be created from the mutual funds.  Each mutual funds has several webpages.  On each webpage are several data tables.
2. Define one function per webpage
- Define each data table per webpage
- Define the for loop that works with each data table
- Return data row and col names collected
3. Loop each mutual fund through each function, extend all data rows to dictionary of the form { mf_ticker : [data, data , ...]}
4. If data row is not the expected length, then add to error log and do not add row to dataframe
5. If crawl stops, print dataframe and error log, otherwise print the same at the end.

## Files
- [USD_MF.txt](https://github.com/andrewdavis23/boomer-eggs/blob/main/USD_MF.txt):  All of the tickers for every mutual fund traded in the US dollar.
- [method_scrape_all_text_first.py](https://github.com/andrewdavis23/boomer-eggs/blob/main/method_scrape_all_text_first.py):  Another version of the main program.
- [single_data_point.py](https://github.com/andrewdavis23/boomer-eggs/blob/main/single_data_point.py):  Simple example that uses hard coded input for a single mutual fund.
- [yahoo-mf](https://github.com/andrewdavis23/boomer-eggs/blob/main/single_data_point.py):  The main program.

