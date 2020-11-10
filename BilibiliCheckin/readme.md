# AutoCheckin - Telegram

The `AutoCheckin` for `Telegram`. 

## How it checks you in

Using your cookie `SESSDATA`, this function sends a request to check you in

## Environ to set

|name|value|
|-|-|
|BL_SESSDATA|cookie achieved using devtool in your browser |

You should first log yourself in at [Bilibili](https://www.bilibili.com/).  
Then, open the devtool in your browser, turn to `Application` > `Storage` > `Cookies` > `https://www.bilibili.com`.  
The cookie named `SESSDATA` is the environ you need.
