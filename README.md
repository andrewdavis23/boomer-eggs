# boomer-eggs
Yahoo Finance scrapper for mutual funds and etfs

Mutual Fund Algorithim:
1. Create list of mutual funds.  Each URL will be created from the mutual funds.  Each mutual funds has several webpages.  On each webpage are several data tables.
2. Define one function per webpage
- Define each data table per webpage
- Define the for loop that works with each data table
- Return data row and col names collected
3. Loop each mutual fund through each function, extend all data rows to dictionary of the form { mf_ticker : [data, data , ...]}
4. If data row is not the expected length, then add to error log and do not add row to dataframe
5. If crawl stops, print dataframe and error log, otherwise print the same at the end.

