# Windows 定时任务设置（推荐方案）

**问题**：GitHub Actions 无法访问 TWSE API 和 yfinance（网络环境限制），台股数据无法获取。

**解决方案**：在 Windows 本地使用定时任务，每天运行报告（已验证 100% 成功）。

## 步骤 1：测试本地运行

```powershell
cd "c:\Users\Liu\Desktop\Projects\Proj001_DcMorningReport"
.\.venv\Scripts\python.exe main.py --schedule
```

✅ 预期结果：每天 06:30 和 07:00 输出报告

## 步骤 2：创建 Windows 定时任务

### 方法 A：使用 GUI（简单）

1. **打开任务计划程序**
   - Win 键 → 搜索 `taskschd.msc` → 回车

2. **创建基本任务**
   - 右边栏 → "创建基本任务..."
   - 名称：`DC Daily Morning Report`
   - 描述：`每天 06:30 和 07:00 运行财务报告`

3. **触发器设置**
   - 选项 1（06:30）：
     ```
     每天
     时间: 06:30
     ```
   - 点 "新建" 添加选项 2（07:00）

4. **操作设置**
   - 程序/脚本：
     ```
     powershell.exe
     ```
   - 添加参数：
     ```
     -NoProfile -ExecutionPolicy Bypass -Command "cd 'c:\Users\Liu\Desktop\Projects\Proj001_DcMorningReport'; .\.venv\Scripts\python.exe main.py"
     ```
   - 起始位置：
     ```
     c:\Users\Liu\Desktop\Projects\Proj001_DcMorningReport
     ```

5. **完成并启用**
   - ✅ 启用定时任务
   - ✅ 完成

### 方法 B：使用 PowerShell（脚本化）

在 PowerShell 中运行以下命令（以管理员身份）：

```powershell
# 创建两个定时任务
$taskPath = "c:\Users\Liu\Desktop\Projects\Proj001_DcMorningReport"
$pythonPath = "$taskPath\.venv\Scripts\python.exe"

# 定时任务 1：06:30
$trigger1 = New-ScheduledTaskTrigger -Daily -At 06:30
$action1 = New-ScheduledTaskAction `
  -Execute "powershell.exe" `
  -Argument "-NoProfile -ExecutionPolicy Bypass -Command `"cd '$taskPath'; & '$pythonPath' main.py`"" `
  -WorkingDirectory $taskPath

Register-ScheduledTask `
  -TaskName "DC Daily Morning Report 06:30" `
  -Trigger $trigger1 `
  -Action $action1 `
  -RunLevel Highest `
  -Force

# 定时任务 2：07:00
$trigger2 = New-ScheduledTaskTrigger -Daily -At 07:00
$action2 = New-ScheduledTaskAction `
  -Execute "powershell.exe" `
  -Argument "-NoProfile -ExecutionPolicy Bypass -Command `"cd '$taskPath'; & '$pythonPath' main.py`"" `
  -WorkingDirectory $taskPath

Register-ScheduledTask `
  -TaskName "DC Daily Morning Report 07:00" `
  -Trigger $trigger2 `
  -Action $action2 `
  -RunLevel Highest `
  -Force

Write-Host "✅ 定时任务已创建" -ForegroundColor Green
```

## 步骤 3：验证

1. **检查定时任务状态**

   ```powershell
   Get-ScheduledTask | Where-Object {$_.TaskName -like "*DC Daily*"}
   ```

2. **查看最后运行结果**

   ```powershell
   Get-ScheduledTaskInfo | Where-Object {$_.TaskName -like "*DC Daily*"}
   ```

3. **手动测试运行**
   - 任务计划程序 → 右键任务 → "运行"
   - 检查 Discord 是否收到消息

## 步骤 4：监视和日志

### 查看历史记录

```powershell
# 查看最近 10 条日志
Get-EventLog -LogName System -Source USER32 |
  Where-Object {$_.Message -like "*DC Daily*"} |
  Select-Object -First 10 | Format-Table EventID, TimeGenerated, Message
```

### 查看应用日志

```powershell
# 检查 logs/debug.log 文件
Get-Content "c:\Users\Liu\Desktop\Projects\Proj001_DcMorningReport\logs\debug.log" -Tail 50 -Encoding UTF8
```

## 步骤 5：关闭 GitHub Actions（可选）

如果只用本地定时任务，可以在 GitHub 中禁用 GitHub Actions 工作流：

1. 项目主页 → Settings → Actions → General
2. "Actions permissions" → Select "Disable all"

或保留 GitHub Actions 作为备选（当电脑关闭时可自动运行）。

## 优势对比

| 特性          | Windows 定时任务    | GitHub Actions   |
| ------------- | ------------------- | ---------------- |
| 台股数据获取  | ✅ 100% 成功        | ❌ 0% (网络限制) |
| 美股/加密数据 | ✅ 成功             | ✅ 成功          |
| 系统要求      | Windows PC 持续运行 | 无要求 (云端)    |
| 网络限制      | 无                  | TWSE/Yahoo 限制  |
| 成本          | 免费                | 免费 (无超额)    |
| 可靠性        | 高 (本地)           | 中 (云端)        |

## 故障排查

### 定时任务未运行

- ✅ 检查电脑是否是时间后开机（可配置屏幕唤醒）
- ✅ 任务计划程序 → 任务属性 → 勾选 "不管用户是否登录都要运行"
- ✅ 权限问题：以管理员身份创建任务

### Python 脚本找不到

- ✅ 在 PowerShell 中测试完整路径：
  ```powershell
  & "c:\Users\Liu\Desktop\Projects\Proj001_DcMorningReport\.venv\Scripts\python.exe" --version
  ```

### Discord 消息未收到

- ✅ 检查网络连接
- ✅ 验证 `DISCORD_WEBHOOK_URL` 环境变量
- ✅ 查看 `logs/debug.log` 获取错误详情

## 推荐配置

```powershell
# 建议：每天 06:30 运行一次（足以获取完整报告）
# 原因：
# 1. 台股美股都已开盘
# 2. 避免重复发送消息
# 3. 节省资源

$trigger = New-ScheduledTaskTrigger -Daily -At 06:30
# ... 参考上面的步骤 B
```

## 备注

- ✅ 所有敏感信息（API KEY）从 `reminders.txt` 读取，自动注入环境变量
- ✅ 日志文件会自动轮转（5MB/file，保留 3 个备份）
- ✅ 每次运行自动检测更新并发送 Discord 消息
