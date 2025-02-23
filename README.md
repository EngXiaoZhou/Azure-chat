# azure_chat
一个调用Azure Ai Foundry api，实现调取azure中创建的模型来进行聊天的项目


## 依赖
**python >= 3.8**

**azure.identity**

**azure-ai-inference**


## 环境搭建
### 1.请先前往[python官网](https://www.python.org/downloads/)下载所需的python版本，建议使用二进制安装并勾选自动配置环境变量

### 2.使用pip安装(ide或者cmd中)所需的azure依赖包，命令如下:

`pip install azure.identity`

`pip install azure-ai-inference`

#### 注：如您有网络访问问题，请自行更换pip源后再安装

`pip config set global.index-url URL`

### 3.下载安装所需ide（可选）
推荐使用[pycharm](https://www.jetbrains.com/pycharm/download)或[vscode](https://code.visualstudio.com/)
没有IDE在cmd/tty中运行也可，但是体验会较差。


## 用法
### 1.git clone或打包下载本项目并进入项目目录
项目中含有**chat.py**与**stream-chat.py**
#### chat.py为直出模式，输入会等到云端模型全部输出完毕再返回响应
#### stream-chat.py为流模式，模型实时回复，即类似目前各家的主流模型响应

### 2.根据你所需要使用的模式编辑对应的py源文件，填入自己云端对应的信息
包括**ENDPOINT**，**DEPLOYMENT_NAME**与**SDK_KEY**

### 3.在ide或tty/cmd中运行对应py文件
`python xyz.py`


## TODO
- [ ] **加入arguments与options，实现模型参数（温度，上下文窗口等）可调**
- [ ] **可使用参数或外部文件指定云端对应信息，不再需要修改源码方式填入**
- [ ] **将stream-chat.py与chat.py整合，使用arguments指定模式**
