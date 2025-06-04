# record common issues

> If you don't find the problem you encountered, please submit it in [issues](https://github.com/timerring/bilive/issues/new/choose).

## What is the purpose of recording cookies?

This is used to verify the account when recording, and the default maximum quality parameter for Bilibili when not logged in is 250 (super-clear), if you want to record a higher quality video, you need to log in to the account, please specify the account's cookies in the configuration file. 

You can specify cookies in the `settings.toml` file in the project directory, or fill in cookies in the settings of the recording panel `http://localhost:2233/settings` (the default port is 2233, you can modify it yourself).
```
[header]
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
cookie = "xxxx"
```

After restarting record, select a higher quality recording.

> [!TIP]
> It is not recommended to use cookies to login to blrec recording, because Bilibili's official sometimes blocks the recording, causing the recording to fail. In addition, after logging in with cookies, the recording effect is not stable, and there may be a situation where the corresponding stream is not captured.
> 
> Therefore, I personally recommend **not using cookies for default recording of 250 super-clear quality**, currently there is no problem with getting the stream.

## If the port is already occupied
If the port is conflicted, please reset the port `port` in the `record.sh` startup script and restart (the default port is 2233).

## How to adjust the directory
The recording part uses `blrec`, set the video storage directory and log directory in `settings.toml`, or set it in the blrec frontend interface即`http://localhost:port` after starting. For details, see [blrec](https://github.com/acgnhiki/blrec).

> [!TIP]
> Don't recommend adjust the directory, which will cause the upload module to be unavailable.

## The stream information cannot be obtained

```
[2023-06-15 13:07:09,375] [DEBUG] [parse] [xxxxxxxx] Error occurred while parsing stream: ValueError('12 is not a valid CodecID')
Traceback (most recent call last):
```

This usually happens when the recording host is overseas, because the overseas live stream encoding is HEVC, but it only supports processing AVC encoding, so it cannot obtain the live stream information.
Reference issue: https://github.com/BililiveRecorder/BililiveRecorder/issues/470

Solution: Switch the recording encoding, select hls encoding, and then re-record.

## Failed to add room

```
[2024-11-22 14:29:04,304] [ERROR] [task_manager] Failed to add task xxxxxxxxx due to: KeyError('sex')
[2024-11-22 14:29:04,305] [CRITICAL] [exception_handler] KeyError
```

This usually happens when the recording host is overseas, because the overseas live stream encoding is HEVC, but it only supports processing AVC encoding, so it cannot obtain the live stream information.
Reference issue: https://github.com/BililiveRecorder/BililiveRecorder/issues/470

Solution: Switch the recording encoding, select hls encoding, and then re-record.

## The project is already in the recording state, but it cannot work after restarting

Restarting requires waiting for about half a minute.

## Failed to add room `aiohttp.client_exceptions.ClientResponseError: 412 `

From [issue 148](https://github.com/timerring/bilive/issues/148)

```
aiohttp.client_exceptions.ClientResponseError: 412, message='Precondition Failed',
```

The recording part I use [blrec](https://github.com/acgnhiki/blrec), according to the [corresponding issue](https://github.com/acgnhiki/blrec/pull/264) it seems to be blocked by risk control. This is the [Bilibili API error 412 situation](https://github.com/SocialSisterYi/bilibili-API-collect/issues/872).

Solution: I recommend adding or replacing UA, you can also consider adding cookies, wait a few minutes to execute `./record.sh` to retry.

## `http://localhost:2233/settings` webpage cannot be accessed

The record process is not working, please check the log.