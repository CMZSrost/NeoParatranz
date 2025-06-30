# 项目介绍
本项目是NEO的Paratranz翻译文件自动化脚本，欢迎大家参与翻译以及修改

# 安装方法
1. 安装uv

参考教程：https://docs.astral.sh/uv/getting-started/installation/#installation-methods
```powershell
# 首先用管理员模式打开PowerShell
# 然后执行以下命令即可安装uv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

2. 配置环境变量（windows环境）

将安装uv过程中提示的安装路径配置到环境变量PATH中
   1. win+R, 输入sysdm.cpl
   2. 选择 高级 > 环境变量 > 用户/系统变量（两个都可以） > Path > 编辑 > 新建 > 粘贴uv安装路径 > 确定 > 确定 > 确定 > 重启电脑

3. 克隆项目

方法1：下载zip文件，解压到任意目录

方法2：使用git克隆项目
```powershell
git clone https://github.com/CMZSrost/NeoParatranz.git
```

4. 配置token（可选，用于上传与下载翻译文件）

将.env_example文件重命名为.env，并在其中配置paratranz的token (token可以在paratranz的个人设置中获取) 以及 paratranz的项目id

5. 运行脚本（第一次运行会联网下载依赖环境）

查看帮助
```powershell
uv run main.py --help
```
导出翻译文件
```powershell
uv run main.py convert "mod文件夹路径" "翻译文件导出路径，默认在运行目录"
```
复原翻译文件
```powershell
uv run main.py convert "mod文件夹路径" "解压后的翻译文件夹路径"
```

罗列项目文件
```powershell
uv run main.py list
```

上传翻译文件到paratranz
```powershell
uv run main.py upload "翻译文件路径" -c(创建文件) -o(更新原文) -t(更新译文) -f(更新译文时更新所有词条)
```

下载翻译文件到本地
```powershell
uv run main.py download "保存路径，默认在运行目录" -z(解压并删除zip文件)
```

# 运行示例

假设有以下mod文件夹

"D:\Neo Scavenger\Mods\NeoScavExtended"

导出翻译文件
```powershell
uv run main.py convert "D:\Neo Scavenger\Mods\NeoScavExtended"
```
翻译文件会导出到本项目根目录的"NeoScavExtended"文件夹中（不存在就会创建）
> 注意，如果有已翻译好的文件，会进行覆盖更新操作，即同键值的字段会被覆盖，通常搭配-t参数来将译文更新到翻译文件中

从paratranz导出翻译文件后，需要复原翻译文件，将文件解压后，通常目录结构如下：

"D:\Download\utf-8\NeoScavExtended"

复原翻译文件
```powershell
uv run main.py deconvert "D:\Neo Scavenger\Mods\NeoScavExtended" "D:\Download\utf-8\NeoScavExtended"
```
> 注意，这里会对文件进行覆盖更新操作，运行前建议做好备份工作，或者将"D:\Neo Scavenger\Mods\NeoScavExtended"改为复制后的文件夹路径，这样可以避免覆盖原文件

# 更新方法

1. git 克隆得到
```powershell
git pull
```

2. 直接下载zip

如果不介意重新安装依赖，直接运行即可，会直接安装依赖

如果想复用依赖，可以将旧文件夹里的.venv文件夹挪到新文件夹里