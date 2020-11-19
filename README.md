# AutoCheckin - 自动签到

<div align=center style='margin: 50px'><img width = '150' height ='150' src ="./img/autocheckin.svg"/></div>

一系列自动签到函数, 基于Azure Functions实现每日签到   
A group of python function to check you in, using Azure Functions

[![Python](https://img.shields.io/badge/Python%20-%2314354C.svg?&style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Make with love](https://img.shields.io/badge/made%20with-vscode-%23007ACC?&style=for-the-badge&logo=visual-studio-code)](https://code.visualstudio.com/)
[![Azure Functions](https://img.shields.io/badge/Azure%20Functions%20-%230072C6.svg?&style=for-the-badge&logo=azure-functions&logoColor=white)](https://azure.microsoft.com/services/functions/)
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/Maxwell-Lyu/AutoCheckin/CD?label=deployment&logo=github-actions&logoColor=white&style=for-the-badge)

## Now supporting - 支持的服务

|Function|Description|
|-|-|-|
|BilibiliCheckin|Bilibili弹幕网-直播每日签到|
|TelegramCheckin|Telegram-向bot发指定消息签到|
|TSDMCheckin|天使动漫论坛-每日签到|
|TSDMLabor|天使动漫论坛-打工|

## Usage - 使用说明

### 1. Create a function app in Azure - 创建函数应用

[Microsoft Docs](https://docs.microsoft.com/azure/azure-functions/functions-create-scheduled-function)   
Create an empty function app, with attention to these points:
+ choose `Consumption plan` for hosting plan
+ choose `Python` as your runtime

创建空的函数应用, 并请注意以下几点
+ 在`正在承载`选择`消耗计划`
+ 在运行时环境选择`Python`


### 2. Clone this repo - 克隆该项目

### 3. Open this repo using VSCode - 使用VSCode打开该项目

Install extension `Azure Functions` and connect to your function app  
安装拓展插件`Azure Functions`并连接到您的函数应用  

### 4. Disable functions you dont need - 禁用您不需要的函数

In the VSCode's azure panel, right click on the functions to disable it   
在VSCode的azure面板中, 右键您不需要的函数以禁用之

### 5. Debug or deploy - 测试或部署

Refer to readme in each function for detailed instructions on configuration  
参阅各个函数自己的readme, 获取详细配置指导

Why there are only instructions in English? Cuz I'm lazy.  
为什么只有英文指导? 因为我懒, 一开始用英文写, 懒得翻译了

### 6. Have fun - 爽歪歪
