# Telegram Auto Check-in

A simple python function to check you in for anything in telegram, when deployed using **Azure Functions**
![CI](https://github.com/Maxwell-Lyu/AutoCheckin/workflows/CI/badge.svg)

## Usage: 

### 1. Create a function in Azure that is triggered by a timer

[Microsoft Docs](https://docs.microsoft.com/en-us/azure/azure-functions/functions-create-scheduled-function)  
When created, click `Functions > Functions > Develop Locally` in your Function App's control panel  
Follow the instructions to create a default function app  
You may test run, but do not deploy the default function

### 2. Clone this Repo

### 3. Copy files in this repo into your project

+ delete your default function
+ rename TelegramCheckin at your convenience

### 4. Generate configuration files

```bash
cd utility
python get_session.py
# follow instruction prompted by get_session.py
```
`gen_session.py` will give your configuration a test drive. If you cannot get desired result(a check-in message sent to your desired account using your identity), check the configurations and try again.  
**ATTENTION NEEDED**: the files `utility/local.settings.json`, `utility/remote.settings.json` contains sensitive data, must be kept as top-secret

### 5. Debug or deploy

#### Debug
`utility/local.settings.json` contains environment variables needed for local dev, copy the lines under `Values` and add the lines under `Values` in file `local.settings.json`

#### Depoly
`utility/remote.settings.json` contains configurations for azure function app, copy the lines and add into the editor `Configuration > Application settings > Advanced edit`. Pay attention to commas if you cannot submit the settings

### 6. Have fun

<TODO> rewrite this readme
