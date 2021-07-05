import subprocess


def main():
    subprocess.Popen('python3 server.py', creationflags=subprocess.CREATE_NEW_CONSOLE)
    subprocess.Popen('python3 client.py', creationflags=subprocess.CREATE_NEW_CONSOLE)


if __name__ == '__main__':
    main()
