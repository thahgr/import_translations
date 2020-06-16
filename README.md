# import_translations
Python script to get translations from an xls file and import on Android studio
Each language should be in a separate tab with its Android code name eg "de,es"

To install the packages on mac run:
sudo easy_install pip
pip install pandas XlsxWriter xlrd django

The program can run on mac as:
./import_translations.py yourfile.xls pathtoyourres/Android/app/src/main/res
