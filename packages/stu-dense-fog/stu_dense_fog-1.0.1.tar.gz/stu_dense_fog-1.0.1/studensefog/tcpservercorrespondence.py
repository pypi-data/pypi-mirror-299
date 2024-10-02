# 这是一个tcp服务器解决方案，里面包含文字传输，音视频传输基本方法，能基于此快速搭建一个TCP服务器
# 解堵塞除了收到客户端消息外，也有可能是客户端关闭套接字
# 注意文字信息一般不会丢失，音频信息传输更严格，所以我只在音频传输时用了重传机制
import socket
import time
import threading


def init_tcp_server(ip, port, num):  # 初始化tcp服务器套接字
    tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建套接字
    tcp_server_address = (ip, port)  # 服务器地址
    tcp_server.bind(tcp_server_address)  # 绑定服务器地址
    tcp_server.listen(num)  # 最大允许的客户端连接数量
    return tcp_server


def send_characters_message_server(tcp_client, tcp_client_address, out_time, deal_func):  # 返回文字信息，文字信息一般不会传错，不需要重传机制
    print(f"欢迎来自IP:{tcp_client_address[0]};Port:{tcp_client_address[1]}连接服务器")
    while True:
        start_time = time.time()  # 每次通信开始前都要进行超时管理
        while time.time() - start_time < out_time:
            data = tcp_client.recv(4096).decode('utf-8')  # 客户端的文字信息
            if not data:  # 检测到客户端断开连接，客户端关闭套接字
                print(f"来自IP:{tcp_client_address[0]};Port:{tcp_client_address[1]}的连接已断开")
                tcp_client.send('连接断开'.encode())
                tcp_client.close()
                return
            else:  # 处理文字信息，如大模型等等
                response = deal_func(data)  # 调用文字信息处理函数得到返回值
                tcp_client.send(response.encode())
                break  # 进入下一次通信
        if time.time() - start_time >= out_time:
            tcp_client.send('连接超时！'.encode())
            tcp_client.close()  # 一次通信超时就关闭套接字，顺便关闭整个函数
            return


# 每次通信是分批传输的
def send_audio_message_server(tcp_client, tcp_client_address, out_time, data_length, deal_func):  # data_length约定传输音频时每批大小
    print(f"欢迎来自IP:{tcp_client_address[0]};Port:{tcp_client_address[1]}连接服务器")
    while True:
        start_time = time.time()  # 每次通信开始前都要进行超时管理
        while time.time() - start_time < out_time:
            data_len = tcp_client.recv(data_length).decode()  # 音频数据长度
            if not data_len:
                print(f"来自IP:{tcp_client_address[0]};Port:{tcp_client_address[1]}的连接已断开")
                tcp_client.send('连接断开'.encode())
                tcp_client.close()
                return
            else:
                data_len = int(data_len)
                counts = data_len // data_length + 1  # 要传输的次数
                data = b''  # 存储传输的2进制/16进制数据
                for i in range(counts):
                    one_data = tcp_client.recv(data_length)
                    if not one_data:
                        print(f"来自IP为{tcp_client_address[0]};Port为{tcp_client_address[1]}的连接已断开")
                        tcp_client.send('连接断开'.encode())
                        tcp_client.close()
                        return
                    else:
                        data += one_data
                if len(data) == data_len:  # 检查数据有无遗漏，对音频数据进行操作
                    response = deal_func(data)  # 调用音频信息处理函数得到返回值
                    tcp_client.send(response.encode())
                    break  # 进入下一次通信
                else:
                    tcp_client.send('音频数据传输有误'.encode())
                    break  # 进入下一次通信,告诉客户端重传
        if time.time() - start_time >= out_time:
            tcp_client.send('连接超时！'.encode())
            tcp_client.close()  # 一次通信超时就关闭套接字，顺便关闭整个函数
            return


def tcp_server_audio_start(ip, port, num, out_time, data_length, deal_func):  # 启动tcp音频服务器
    tcp_server = init_tcp_server(ip, port, num)
    print(f"TCP服务器运行在IP:{ip};Port:{port}上，最大连接数量为:{num}个客户端")
    while True:
        tcp_client, tcp_client_address = tcp_server.accept()
        threading.Thread(
            target=send_audio_message_server(tcp_client, tcp_client_address, out_time, data_length, deal_func)).start()


def tcp_server_characters_start(ip, port, num, out_time, deal_func):  # 启动tcp文字服务器
    tcp_server = init_tcp_server(ip, port, num)
    print(f"TCP服务器运行在IP:{ip};Port:{port}上，最大连接数量为:{num}个客户端")
    while True:
        tcp_client, tcp_client_address = tcp_server.accept()
        threading.Thread(
            target=send_characters_message_server(tcp_client, tcp_client_address, out_time, deal_func)).start()
