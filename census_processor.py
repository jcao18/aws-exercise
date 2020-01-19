import requests
import xlrd
import csv
import boto3

census_file_xlsx = 'county-to-county-2013-2017-current-residence-sort.xlsx'
census_file_url = 'https://www2.census.gov/programs-surveys/demo/tables/geographic-mobility/2017/county-to-county-migration-2013-2017/county-to-county-migration-flows/county-to-county-2013-2017-current-residence-sort.xlsx'
census_file_csv = 'county-to-county-2013-2017-current-residence-sort.csv'
s3_bucket_name = 'aws-exercise-census'

us_states = ["Alabama","Alaska","Arizona","Arkansas","California","Colorado",
  "Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho","Illinois",
  "Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland",
  "Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana",
  "Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York",
  "North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania",
  "Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah",
  "Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"]

# download census migration dataset
print("Download census migration dataset")
r = requests.get(census_file_url, allow_redirects=True)
open(census_file_xlsx, 'wb').write(r.content)

# the dataset is in excel format, need to convert to csv for use in aws
print("Convert excel to csv")
wb = xlrd.open_workbook(census_file_xlsx)
csv_file = open(census_file_csv, 'w')
wr = csv.writer(csv_file, quoting=csv.QUOTE_NONNUMERIC)
for state in us_states:
    sh = wb.sheet_by_name(state)
    for rownum in range(sh.nrows):
        wr.writerow(sh.row_values(rownum))
csv_file.close()

# upload the csv file to the deployed s3 bucket for use by athena
print("Upload the csv file to the s3 bucket")
s3_client = boto3.client('s3')
s3_client.upload_file(census_file_csv, s3_bucket_name, census_file_csv)
