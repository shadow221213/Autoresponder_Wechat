import glob
import os
import threading

import markdown
import pyautogui
import pyperclip
import keyboard
import time

import win32gui
import win32con
from bs4 import BeautifulSoup
from ollama import chat
from ollama import ChatResponse

# 时延，减少CPU使用
delay = 0.05
# 置信度
confidence = 0.8
# 缓存图像识别结果
emoji_location = None
# 图片位置
friend_directory = "./image/friend"
# 设置pyautogui的默认延迟为最小值
pyautogui.PAUSE = 0.1
pyautogui.MINIMUM_DURATION = 0.1
# 结束标志
exit_program = False

def Ollama_response( content ):
    response: ChatResponse = chat(
        model='deepseek-r1:7b',  # 在此可换其他模型
        messages=[{
            'role':    'user',
            'content': content,
            }]
        )
    res = response['message']['content']
    begin = res.find('<think>', 0, len(res)) + 9
    end = res.find('</think>', 0, len(res)) + 10

    print(res[begin:end - 10])

    return res[end:len(res)]

def find_friend_images( directory ):
    pattern = os.path.join(directory, "*.png")
    matching_files = glob.glob(pattern)

    return matching_files

def extract_filename( file_path ):
    filename = os.path.basename(file_path)
    filename_without_extension = os.path.splitext(filename)[0]

    return filename_without_extension

def markdownToText( md_text ):
    html = markdown.markdown(md_text)
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text( )

    lines = text.splitlines( )
    non_empty_lines = [line for line in lines if line.strip( ) != '']
    return '\n'.join(non_empty_lines)

def findFriends( ):
    try:
        friend_locations = find_friend_images(friend_directory)
        if friend_locations:
            for friend_location in friend_locations:
                friend = pyautogui.locateOnScreen(friend_location, confidence=confidence)
                if friend and findNews(friend):
                    return friend_location

            return None
    except Exception as e:
        # print(f"未找到朋友或查找朋友时出错: {str(e)}")
        return None

def findNews( news_location ):
    try:
        if news_location:
            if pyautogui.locateOnScreen("./image/news.png", region=news_location, confidence=confidence):
                x, y, width, height = news_location
                pyautogui.click(x + 20, y + 20)
                print("发现了新消息")
                return True

        return False
    except Exception as e:
        # print(f"未找到新信息或查找新消息时出错: {str(e)}")
        return False

def findReset( ):
    try:
        reset_location = pyautogui.locateOnScreen('./image/reset.png', confidence=confidence)

        if reset_location:
            x, y, width, height = reset_location
            pyautogui.click(x + 20, y + 20)
            print("恢复原始状态")
    except Exception as e:
        print(f"查找文件传输助手时出错: {str(e)}")

def sendMsg( name ):
    global emoji_location
    try:
        # 使用缓存的图标位置
        if not emoji_location:
            emoji_location = pyautogui.locateOnScreen('./image/emoji.png', confidence=confidence)

        x, y, width, height = emoji_location
        X = x + width
        Y = y - 40

        # 快速执行点击操作
        pyautogui.rightClick(X, Y)
        pyautogui.click(X + 10, Y + 10)

        friendMsg = pyperclip.paste( )
        msg = name + ": " + friendMsg
        print(msg)

        print("正在思考如何回复...")
        reply = Ollama_response(friendMsg)
        text = markdownToText(reply)
        print("即将发送的消息：" + text)

        pyperclip.copy(text)
        pyautogui.click(X, y + 50)
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.press('enter')
        print("发送成功!")

        findReset( )
    except Exception as e:
        print(f"发送消息时出错: {str(e)}")

def bringWechatToTop( ):
    global exit_program

    try:
        hwnd = win32gui.FindWindow('WeChatMainWndForPC', "微信")

        if hwnd:
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            win32gui.SetForegroundWindow(hwnd)
            print("微信已经置顶")
        else:
            print("没有找到微信")
    except Exception as e:
        print(f"查找微信时出错，请打开微信: {str(e)}")
        exit_program = True

def exitKey( ):
    global delay, exit_program
    while True:
        if keyboard.is_pressed('end'):
            print("按下了end键，程序即将结束")
            exit_program = True
            break
        time.sleep(delay)

if __name__ == '__main__':
    cnt = 0
    max_cnt = 10 / delay

    key_thread = threading.Thread(target=exitKey)
    key_thread.daemon = True
    key_thread.start( )

    bringWechatToTop( )
    reply = Ollama_response(
        "你是一个精通聊天的人，接下来请扮演我与我的朋友们进行对话，注意要有人情味，回答要简洁明了，不要罗列多条"
        )
    print("即将发送的消息：" + reply)
    findReset( )

    while not exit_program:
        try:
            if cnt > max_cnt:
                bringWechatToTop( )
                findReset( )
                cnt = 0
            time.sleep(delay)

            friend_location = findFriends( )
            if friend_location is not None:
                time.sleep(delay)
                name = extract_filename(friend_location)
                sendMsg(name)
            else:
                time.sleep(delay)

            cnt += 1
        except Exception as e:
            print(f"运行时出错: {str(e)}")
            break

    key_thread.join( )
    pyautogui.alert(text='程序已结束!', title='提示', button='好的')
