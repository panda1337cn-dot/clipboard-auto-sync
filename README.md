# clipboard-auto-sync
automatic clipboard sync between computer and ios

自动同步ios与电脑（windows/linux端）的剪切板
需要自行准备服务器或者内网使用

Sample shortcut
https://www.icloud.com/shortcuts/536ab3ffb8d7496889196b9f19e78f4f

在服务器上运行web.py
在电脑上运行client_send.py
在ios上点击运行shortcut
(仅需要点击一次，会自动循环执行脚本)
在每个脚本中都应该设置api_url 和 独立的 machine_id
