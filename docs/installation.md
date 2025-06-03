# Quick start

> [!NOTE]
> If you are a windows user, please use WSL to run this project.

### Mode

First, introduce the three different processing modes of this project:
1. `pipeline` mode (default): The fastest mode, it is recommended to set the segment in `blrec` to half an hour or less, and the video segments are uploaded in parallel.
2. `append` mode: Basically the same as above, but the rendering process is executed serially, which is expected to be 25% slower than the pipeline.
3. `merge` mode: Wait for all recordings to complete, then perform the rendering merging process, the uploads are all complete versions of the recordings (non-P submissions), the waiting time is longer, the efficiency is slower, and it is suitable for scenarios that need to upload complete recordings.

### Installation

> [!TIP]
> If you are a windows user, please use WSL to run this project.

#### 0. clone project

Since the project introduces my submodule [DanmakuConvert](https://github.com/timerring/DanmakuConvert) and [bilitool](https://github.com/timerring/bilitool), it is recommended to clone the project and update the submodules.

```bash
git clone --recurse-submodules https://github.com/timerring/bilive.git
```

If you do not clone the project using the above method, please update the submodules:

```bash
git submodule update --init --recursive
```

#### 1. Install dependencies (recommended to create a virtual environment)

```
cd bilive
pip install -r requirements.txt
```

Please install the corresponding [`ffmpeg`](https://www.ffmpeg.org/download.html) according to your system type, for example, [install ffmpeg on ubuntu](https://gcore.com/learning/how-to-install-ffmpeg-on-ubuntu/).

[Common issues collection](https://timerring.github.io/bilive/install-questions.html)

#### 2. Configure parameters

##### 2.1 Configure upload parameters

Customize the relevant configuration in the `bilive.toml` file, map the keywords to `{artist}`、`{date}`、`{title}`、`{source_link}`, please combine and customize the template by yourself:

- `title` title template.
- `description` description template.
- `gift_price_filter = 1` means filtering gifts priced below 1 yuan.
- `reserve_for_fixing = false` means that if the video appears to be incorrect, the video will not be retained for repair after the retry fails, it is recommended to set false for users with limited hard disk space.
- `upload_line = "auto"` means automatically detecting the upload line and uploading, if you need to specify a fixed line, you can set it to `bldsa`、`ws`、`tx`、`qn`、`bda2`.

#### 3. Configure recording parameters

> [!IMPORTANT]
> Please do not modify any configuration related to paths, otherwise the upload module will be unavailable.

> The recording module uses the third-party package `blrec`, the parameter configuration is in the `settings.toml` file, and you can also configure it in the corresponding port visualization page after the recording starts. Quick start only introduces the key configuration, other configurations can be understood by referring to the configuration items in the page, and support hot modification.

- The addition of rooms follows the format corresponding to `[[tasks]]` in the file.
- The default recording quality of the recording module is super-high quality without login. If you need to login, please fill in the `SESSDATA` parameter value from the `cookie.json` file (see step 4) to the `cookie` part of `[header]`, the format is `cookie = "SESSDATA=XXXXXXXXXXX"`, after logging in, you can record higher quality video. (Recommended not to login)
- `duration_limit` means the recording duration.

#### 4. bilitool login (persistent login, this step only needs to be executed once)

> For docker deployment, this step can be ignored, because `docker logs` can print the QR code in the console, and you can scan the QR code to login directly, the following content is for source code deployment.

##### 4.1 Method 1: Login via cookie

Generally, the log file does not print the QR code effect, so this step needs to be installed in advance on the machine:

```
pip install bilitool
bilitool login --export
# Then use the app to scan the QR code to login, the cookie.json file will be automatically exported
```
Leave the login cookie.json file in the root directory of this project, and it will be deleted after the `./upload.sh` starts.

##### 4.2 Method 2: Login via submodule

Or you can login in the submodule, the way is as follows:

```
cd src/upload/bilitool
python -m bilitool.cli login
# Then use the app to scan the QR code to login
```

[Common issues collection](https://timerring.github.io/bilive/biliup.html)

#### 5. Start automatic recording

> [!IMPORTANT]
> Using the default password and exposing the port on a server with a public IP has a potential risk of exposing the cookie, so **not recommended** to map the port on a server with a public IP.
> - If you need to use https, you can consider using an openssl self-signed certificate and adding the parameters `--key-file path/to/key-file --cert-file path/to/cert-file` in `record.sh`.
> - You can limit the inbound IP rules of the server port or use nginx etc. to restrict access.

Before starting, please set the password for the recording front-end page, and save it in the `RECORD_KEY` environment variable, `your_password` consists of letters and numbers, and is at least 8 digits, at most 80 digits.
- Temporary setting password `export RECORD_KEY=your_password`。(Recommended)
- Persistent setting password `echo "export RECORD_KEY=your_password" >> ~/.bashrc && source ~/.bashrc`，where `~/.bashrc` can be modified according to the shell you are using.

```bash
./record.sh
```

[Common issues collection](https://timerring.github.io/bilive/record.html)

#### 6. Start automatic upload

```bash
./upload.sh
```

[Common issues collection](https://timerring.github.io/bilive/upload.html)

#### Log information

The corresponding execution logs can be viewed in the `logs` folder, if there are any issues, please submit them in [`issue`](https://github.com/timerring/bilive/issues/new/choose), and provide [debug] level logs if there are any exceptions.

```
logs # Log folder
├── record # blrec recording log
│   └── ...
├── scan # scan processing log [debug] level
│   └── ...
├── upload # upload log [debug] level
│   └── ...
└── runtime # runtime log [info] level
    └── ...
```