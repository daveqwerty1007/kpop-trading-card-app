# SQL Query For R6-R11

This guide is created for S24 CS338 Report only with no production purpose use.

## 1. Setup MySQL db in MysqlWorkbench

   Set up a local host mysql database.

   run script 'Setup.sql', \
   'LoadSample.sql' for sample testing, and \
   'LoadProd.sql' for production testing.

## 3. Populate Database

#

## Using these tables with the app

`Setup.sql` creates the same table names the Flask app uses (`user`,
`cart_item`, `order_item`, ...), so the app can run against this database
via `DATABASE_URL`. The passwords in `LoadSample.sql` and `LoadProd.sql` are
plain text, though, so those users can't log in to the app. To get sample
data you can log in with, use `python backend/data/loaddata.py` instead.
