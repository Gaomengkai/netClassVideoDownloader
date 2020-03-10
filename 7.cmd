cd D:\Documents\Programs\blog\
pelican content
xcopy D:\Documents\Programs\blog\output D:\Documents\Programs\gaomengkai.github.io /y /e
cd D:\Documents\Programs\gaomengkai.github.io
git add .
git commit -m "Updating"
git push origin master