from django.shortcuts import render
from dwebsocket.decorators import accept_websocket, require_websocket
from django.http import HttpResponse
import paramiko


# def exec_command(comm):
#     hostname = '192.168.0.162'
#     username = 'root'
#     password = 'root'
#
#     ssh = paramiko.SSHClient()
#     ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#     ssh.connect(hostname=hostname, username=username, password=password)
#     stdin, stdout, stderr = ssh.exec_command(comm,get_pty=True)
#     result = stdout.read()
#     ssh.close()
#     return result


@accept_websocket
def echo_once(request):
    if not request.is_websocket():  # 判断是不是websocket连接
        try:  # 如果是普通的http方法
            message = request.GET['message']
            return HttpResponse(message)
        except:
            return render(request, 'index.html')
    else:
        for message in request.websocket:
            message = message.decode('utf-8')
            if message == 'backup_all':#这里根据web页面获取的值进行对应的操作
                command = 'bash /opt/test.sh'#这里是要执行的命令或者脚本

                hostname = '192.168.91.128'
                username = 'root'
                password = 'root'

                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(hostname=hostname, username=username, password=password)
                # 务必要加上get_pty=True,否则执行命令会没有权限
                stdin, stdout, stderr = ssh.exec_command(command, get_pty=True)
                while True:
                    nextline = stdout.readline()
                    request.websocket.send((nextline.strip()).encode('utf-8')) # 发送消息到客户端
                    # 判断消息为空时,退出循环
                    if nextline == "" and nextline != None:
                        break

                ssh.close()  # 关闭ssh连接
            else:
                request.websocket.send('小样儿，没权限!!!'.encode('utf-8'))