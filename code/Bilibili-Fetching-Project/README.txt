1.启动前先更新B站的Cookie
2.先使用fetch_all_url_by_up.py生成所有指定UP主的urls，指定UP主的信息在UP_info.txt中填写，然后运行create_up_json.py转换为Up_info.json
3.再使用fetch_single_vedio_by_url.py获取指定urls的视频信息

git-hub上传代码的流程
1.git add .
2.git commit -m '本次上传的注释'
3.git config --global https.proxy http://127.0.0.1:此次端口号
4.git config --global http.proxy http://127.0.0.1:此次端口号
5.git push -u origin master

git-hub更新本地代码的流程
1.git reset --hard
2.git pull
