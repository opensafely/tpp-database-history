import datetime


# The value of RUN_DATE should be the date analysis/query.sql was run. However, this
# date is not knowable, so instead we use today's date, which is the same as @to_date in
# analysis/query.sql. For more information, see:
# https://github.com/opensafely/tpp-database-history/issues/45
RUN_DATE = datetime.date.today()
