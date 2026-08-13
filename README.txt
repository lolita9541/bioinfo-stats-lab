Bioinfo & Stats Lab — Netlify 靜態網站

【最快上線方式】
1. 解壓縮 bioinfo-stats-netlify.zip
2. 先雙擊 index.html 預覽
3. 登入 Netlify
4. 找到 Add new project / Deploy manually
5. 將整個 bioinfo-stats-netlify 資料夾拖進 Netlify
6. 等待幾秒後會得到 *.netlify.app 網址

【最常需要修改的地方】
請用文字編輯器打開 index.html：

1. Email
搜尋：
your.email@example.com
改成你的 Email。

2. Google Scholar / ORCID / GitHub
搜尋：
href="#"
將 # 換成自己的完整網址。

3. 網站名稱
搜尋：
Bioinfo & Stats Lab
可改成你的正式品牌名稱或姓名。

4. 文字
中文與英文都放在同一個 HTML 裡：
data-zh="中文"
data-en="English"
直接改對應文字即可。

【檔案說明】
index.html   網站內容
style.css    顏色、版面、手機版
script.js    中英文切換與手機選單
assets/      研究方向彩圖

這是純靜態網站，不含 CMS、登入、資料庫或研究檔案上傳。
