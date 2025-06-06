# bilive

## Mode
1. `append` 模式: 分段视频录制完毕即上传。
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
- `reserve_for_fixing = false` 表示如果视频出现错误，重试失败后不保留视频用于修复，推荐硬盘空间有限的用户设置 false。
- `upload_line = "auto"` 表示自动探测上传线路并上传，如果需要指定固定的线路，可以设置为 `bldsa`、`ws`、`tx`、`qn`、`bda2`。

#### 4.2. 配置录制参数

> [!IMPORTANT]
> 请不要修改任何有关路径的任何配置，否则会导致上传模块不可用

> 录制模块使用第三方包 `blrec`，参数配置在 `settings.toml` 文件中，建议录制启动后在对应端口可视化页面配置。支持热修改。

- 录制模块默认不登录录制超清画质，如需登录，请将 `cookie.json` 文件（见步骤 4）中的 `SESSDATA` 参数值填写到 `[header]` 的 `cookie` 部分，格式为 `cookie = "SESSDATA=XXXXXXXXXXX"`，登录后可以录制更高画质的视频。（推荐不登录）

### 5. bilitool 登录（持久化登录，此步骤仅需执行一次）

```
pip install bilitool
bilitool login --export
# 然后使用 app 扫码登录，会自动导出 cookie.json 文件
```

将登录的 cookie.json 文件放在本项目根目录下。

### 6. 启动自动录制

> [!IMPORTANT]
> - 如需使用 https，可以考虑使用 openssl 自签名证书，并在 `record.sh` 中添加参数 `--key-file path/to/key-file --cert-file path/to/cert-file`。

启动前请设置录制前端页面的密码，并保存在 `RECORD_KEY` 环境变量中，`your_password` 由字母和数字组成，最少 8 位，最多 80 位。
- 设置密码 `echo "export RECORD_KEY=your_password" >> ~/.bashrc && source ~/.bashrc`，其中 `~/.bashrc` 可以根据你使用的 shell 自行修改。

```bash
./record.sh
```
### 7. 启动自动上传

```bash
./upload.sh
```
#### 日志信息

对应的执行日志可以在 `logs` 文件夹中查看

```
logs # 日志文件夹
├── record # blrec 录制日志
└── runtime # 运行时日志 [info] 级别
```
