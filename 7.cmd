cd D:\Documents\Programs\blog\
pelican content
xcopy D:\Documents\Programs\blog\output D:\Documents\Programs\gaomengkai.github.io /y
cd D:\Documents\Programs\gaomengkai.github.io
git add .
git commit -m "Updating"
git push origin master
cd D:\Documents\Programs\netClassVideoDownloader
git add 3.csv
git commit -m "Update 3.csv"
git push origin master