# bilive

## Mode

首先介绍本项目三种不同的处理模式：
1. `append` 模式: 基本同上，但渲染过程串行执行，比 pipeline 慢预计 25% 左右。
2. `merge` 模式: 等待所有录制完成，再进行渲染合并过程，上传均为完整版录播（非分 P 投稿），等待时间较长，效率较慢，适合需要上传完整录播的场景。

## Installation

### 1.安装 ffmpeg
```
apt install ffmpeg python3-pip -y
```

### 2. clone 项目

```bash
git clone --recurse-submodules https://github.com/keepraw/bilive.git
```
### 3. 安装依赖(推荐创建虚拟环境)

```
cd bilive
pip install -r requirements.txt
```

### 4. 配置参数

#### 4.1 配置上传参数

在 `bilive.toml` 中自定义相关配置，映射关键词为 `{artist}`、`{date}`、`{title}`、`{source_link}`，请自行组合删减定制模板：

- `title` 标题模板。
- `description` 简介模板。
- `tid` 视频分区，请参考 [bilitool tid](https://bilitool.timerring.com/tid.html) 文档。
- `gift_price_filter = 1` 表示过滤价格低于 1 元的礼物。
- `reserve_for_fixing = false` 表示如果视频出现错误，重试失败后不保留视频用于修复，推荐硬盘空间有限的用户设置 false。
- `upload_line = "auto"` 表示自动探测上传线路并上传，如果需要指定固定的线路，可以设置为 `bldsa`、`ws`、`tx`、`qn`、`bda2`。

### 4.2. 配置录制参数

> [!IMPORTANT]
> 请不要修改任何有关路径的任何配置，否则会导致上传模块不可用

> 录制模块使用第三方包 `blrec`，参数配置在 `settings.toml` 文件中，也可以在录制启动后在对应端口可视化页面配置。快速开始仅介绍关键配置，其他配置可以参照页面中的配置项自行理解，支持热修改。

- 添加房间按照文件中 `[[tasks]]` 对应的格式添加。
- 录制模块默认不登录录制超清画质，如需登录，请将 `cookie.json` 文件（见步骤 4）中的 `SESSDATA` 参数值填写到 `[header]` 的 `cookie` 部分，格式为 `cookie = "SESSDATA=XXXXXXXXXXX"`，登录后可以录制更高画质的视频。（推荐不登录）
- `duration_limit` 表示录制时长。

### 5. bilitool 登录（持久化登录，此步骤仅需执行一次）

```
pip install bilitool
bilitool login --export
# 然后使用 app 扫码登录，会自动导出 cookie.json 文件
```

将登录的 cookie.json 文件放在本项目根目录下，`./upload.sh` 启动后会自动删除。

### 6. 启动自动录制

> [!IMPORTANT]
> 使用默认密码并在具有公网 IP 的服务器上暴露端口存在暴露 cookie 的潜在风险，因此**不推荐**在具有公网 IP 的服务器上映射端口。
> - 如需使用 https，可以考虑使用 openssl 自签名证书，并在 `record.sh` 中添加参数 `--key-file path/to/key-file --cert-file path/to/cert-file`。
> - 你可以限制服务器端口的入站 IP 规则或使用 nginx 等限制访问。

启动前请设置录制前端页面的密码，并保存在 `RECORD_KEY` 环境变量中，`your_password` 由字母和数字组成，最少 8 位，最多 80 位。
- 持久设置密码 `echo "export RECORD_KEY=your_password" >> ~/.bashrc && source ~/.bashrc`，其中 `~/.bashrc` 可以根据你使用的 shell 自行修改。

```bash
./record.sh
```

### 7. 启动自动上传

```bash
./upload.sh
```

#### 日志信息

对应的执行日志可以在 `logs` 文件夹中查看，如有问题请在 [`issue`](https://github.com/timerring/bilive/issues/new/choose) 中提交，如有异常请提供 [debug] 级别日志。

```
logs # 日志文件夹
├── record # blrec 录制日志
│   └── ...
├── scan # scan 处理日志 [debug] 级别
│   └── ...
├── upload # 上传日志 [debug] 级别
│   └── ...
└── runtime # 运行时日志 [info] 级别
    └── ...
```
