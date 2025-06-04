# scan common issues

> If you don't find the problem you encountered, please submit it in [issues](https://github.com/timerring/bilive/issues/new/choose).

## About rendering speed

The rendering speed mainly depends on the hardware and the number of danmaku. The basic test hardware is 2 cores Xeon(R) Platinum 85 CPU, the rendering speed is between 3 ~ 6 times, and can also use Nvidia GPU acceleration. The test graphics card is GTX1650, its rendering speed is between 16 ~ 20 times.

## requests request error
```
requests.exceptions.ConnectionError: ('Connection aborted.', ConnectionResetError(104, 'Connection reset by peer'))
```

Reference: https://stackoverflow.com/questions/70379603/python-script-is-failing-with-connection-aborted-connectionreseterror104

Solution: Network problem, you should know what to do.

## Why did you change back to the queue rendering method?

Due to the usually 10 ~ 15x rendering speed of danmaku under nvidia acceleration, and the speed of whisper executing speech recognition is 5x, so the previous way of creating danmaku rendering by whisper is completely feasible, but for live broadcasts with a large number of danmaku (20 minutes fragment produces 15400+ danmaku), the rendering speed will drop to 2 ~ 4x, when the new whisper processed fragment is rendered, the rendering speed will further decrease, and the number of accumulated parallel danmaku rendering processes will exceed 3, which will cause failure due to the limit of the number of concurrent encoding of the graphics card, in addition, there is a risk of out of memory. Therefore, in order to ensure the quality of rendering and the stability of the program, I originally changed back to the queue rendering method to process danmaku rendering.

### 4. Upload to Bilibili

> [!TIP]
> - The configuration related to video upload is in the `[video]` section of the `bilive.toml` file.
> - `title` and `description` can use keywords: {artist}, {date}, {title}, {source_link}.
> - `tid` is the video category ID, see https://bilitool.timerring.com/tid.html.
> - `reserve_for_fixing` is whether to reserve the video for fixing if MOOV crash error occurs.
> - `upload_line` is the upload line to be used, default is "auto" (recommended), can be "bldsa", "ws", "tx", "qn", "bda2".