NAME=$1
URL=$2
echo Downloading data to data/$NAME.xlsx
curl $URL -o data/$NAME.xlsx
echo Converting data/$NAME.xlsx to data/$NAME.csv
xlsx2csv data/$NAME.xlsx data/$NAME.csv
echo Saving $NAME to database
python data/data_to_db.py data/$NAME.csv
