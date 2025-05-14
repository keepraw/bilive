
# Introduction

> **Warning: This project is only for learning and exchange, please record after obtaining the consent of the other party, please do not use the content without authorization for commercial purposes, please do not use it for large-scale recording, otherwise it will be banned by the official, legal consequences will be self-borne.**

Automatically monitors and records Bilibili live broadcasts and danmaku (including paid comments, gifts, etc.), converts danmaku according to resolution, recognizes speech and renders subtitles into videos, splits exciting fragments according to danmaku density, and generates interesting titles through video understanding models, automatically generates video covers using image generation models, and automatically posts videos and slices to Bilibili, compatible with the version without GPU, compatible with low-configuration servers and hosts.


## Major features

- **Fast**：Use the `pipeline` pipeline to process videos, in ideal conditions, the recording and live broadcast differ by half an hour, and the recording can be上线录播，**Currently the fastest version of Bilibili recording**!
- **( 🎉 NEW)Multi-architecture**：Compatible with amd64 and arm64 architectures!
- **Multiple rooms**：Simultaneously record the content of multiple live broadcast rooms and danmaku files (including normal danmaku, paid danmaku, and gift-up-ship information).
- **Small memory usage**：Automatically delete locally uploaded videos, saving space.
- **Template**：No complex configuration, ready to use, automatically fetch related popular tags through the Bilibili search suggestion interface.
- **Detect and merge segments**：For video stream segments caused by network issues or live broadcast connection issues, it can automatically detect and merge them into complete videos.
- **Automatically render danmaku**：Automatically convert xml to ass danmaku file, the danmaku conversion tool library has been open source [DanmakuConvert](https://github.com/timerring/DanmakuConvert) and rendered to the video to form **danmaku version video** and automatically upload.
- **Low hardware requirements**：No GPU required, only the most basic single-core CPU and the lowest memory can complete the recording, danmaku rendering, upload, etc. All processes, no minimum configuration requirements, 10-year-old computers or servers can still be used!
- **( :tada: NEW)Persistent login/download/upload video (supports multi-part posting)**：[bilitool](https://github.com/timerring/bilitool) has been open source, implements persistent login, download video and danmaku (including multi-part)/upload video (can post multi-part), query posting status, query detailed information, etc., one-click pip installation, can be operated using the command line cli, and can also be used as an api call.
- **( :tada: NEW)Auto-loop multi-platform live streaming**：The tool has been open source [looplive](https://github.com/timerring/looplive) is a 7 x 24 hours fully automatic **loop multi-platform live streaming** tool.