# tweaks.py - DFSTweaks: All optimization tweaks organized by category

TWEAKS = {
    "Debloat": {
        "icon": "🗑",
        "items": [
            {
                "id": "remove_copilot",
                "name": "Remover Copilot",
                "desc": "Remove o Microsoft Copilot e bloqueia via políticas do sistema.",
                "cmds": [
                    '$pkgs = @("Microsoft.Windows.Ai.Copilot.Provider","Microsoft.Copilot","Microsoft.WindowsAiFoundation","Microsoft.Windows.Recall"); foreach ($p in $pkgs) { Get-AppxPackage -Name $p -AllUsers -ErrorAction SilentlyContinue | Remove-AppxPackage -AllUsers -ErrorAction SilentlyContinue; Get-AppxProvisionedPackage -Online -ErrorAction SilentlyContinue | Where-Object DisplayName -like $p | Remove-AppxProvisionedPackage -Online -ErrorAction SilentlyContinue }',
                    'Get-AppxPackage "Microsoft.CoPilot" | Remove-AppxPackage -ErrorAction SilentlyContinue',
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\WindowsCopilot" /v "TurnOffWindowsCopilot" /t "REG_DWORD" /d "1" /f',
                    'reg add "HKCU\\Software\\Policies\\Microsoft\\Windows\\WindowsCopilot" /v "TurnOffWindowsCopilot" /t "REG_DWORD" /d "1" /f',
                    'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced" /v "ShowCopilotButton" /t "REG_DWORD" /d "0" /f',
                    'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\Shell\\Copilot" /v "IsCopilotAvailable" /t "REG_DWORD" /d "0" /f',
                    'reg add "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\WindowsCopilot" /v "AllowCopilotRuntime" /t "REG_DWORD" /d "0" /f',
                ],
            },
            {
                "id": "remove_recall",
                "name": "Desativar Recall",
                "desc": "Remove o recurso Recall (captura de tela contínua da Microsoft).",
                "cmds": [
                    'DISM /Online /Disable-Feature /NoRestart /FeatureName:Recall | Out-Null',
                    '$t = @("\\Microsoft\\Windows\\WindowsAI\\*","\\Microsoft\\Windows\\Recall\\*"); foreach ($p in $t) { Get-ScheduledTask -TaskPath $p -ErrorAction SilentlyContinue | Unregister-ScheduledTask -Confirm:$false -ErrorAction SilentlyContinue }',
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\WindowsAI" /v "DisableAIDataAnalysis" /t REG_DWORD /d 1 /f',
                    'reg add "HKLM\\Software\\Policies\\WindowsNotepad" /v "DisableAIFeatures" /t REG_DWORD /d 1 /f',
                ],
            },
            {
                "id": "remove_onedrive",
                "name": "Remover OneDrive",
                "desc": "Desinstala o OneDrive e move os arquivos para a pasta local do usuário.",
                "cmds": [
                    'Stop-Process -Name "OneDrive" -Force -ErrorAction SilentlyContinue',
                    '$i = "$env:SystemRoot\\System32\\OneDriveSetup.exe"; if (Test-Path $i) { Start-Process -FilePath $i -ArgumentList "/uninstall" -Wait }',
                    'robocopy "$env:USERPROFILE\\OneDrive" "$env:USERPROFILE" /mov /e /xj /ndl /nfl /njh /njs /nc /ns /np | Out-Null',
                    'Remove-Item -Path "$env:USERPROFILE\\OneDrive" -Recurse -Force -ErrorAction SilentlyContinue',
                    'Remove-Item -Path "$env:LOCALAPPDATA\\OneDrive" -Recurse -Force -ErrorAction SilentlyContinue',
                    'Remove-Item -Path "$env:LOCALAPPDATA\\Microsoft\\OneDrive" -Recurse -Force -ErrorAction SilentlyContinue',
                    'Remove-Item -Path "$env:ProgramData\\Microsoft OneDrive" -Recurse -Force -ErrorAction SilentlyContinue',
                    'Remove-Item -Path "C:\\OneDriveTemp" -Recurse -Force -ErrorAction SilentlyContinue',
                    'Remove-Item -Path "HKCU:\\Software\\Microsoft\\OneDrive" -Recurse -Force -ErrorAction SilentlyContinue',
                    'Get-ScheduledTask -TaskPath "\\" -TaskName "OneDrive*" -ErrorAction SilentlyContinue | Unregister-ScheduledTask -Confirm:$false -ErrorAction SilentlyContinue',
                ],
            },
            {
                "id": "remove_edge",
                "name": "Remover Microsoft Edge",
                "desc": "Desinstala o Microsoft Edge do sistema.",
                "cmds": [
                    '$p = (Get-ChildItem "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\*\\Installer\\setup.exe" -ErrorAction SilentlyContinue)[0].FullName; if ($p) { New-Item "C:\\Windows\\SystemApps\\Microsoft.MicrosoftEdge_8wekyb3d8bbwe\\MicrosoftEdge.exe" -Force | Out-Null; Start-Process $p -ArgumentList "--uninstall --system-level --force-uninstall --delete-profile" }',
                ],
            },
            {
                "id": "remove_widgets",
                "name": "Remover Widgets",
                "desc": "Remove o painel de Widgets/News do Windows 11.",
                "cmds": [
                    'Get-AppxPackage *WebExperience* | Remove-AppxPackage -ErrorAction SilentlyContinue',
                    'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Appx\\AppxAllUserStore\\Deprovisioned\\MicrosoftWindows.Client.WebExperience_cw5n1h2txyewy" /f',
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\Windows Feeds" /v "EnableFeeds" /t REG_DWORD /d 0 /f',
                ],
            },
            {
                "id": "disable_ie",
                "name": "Desativar Internet Explorer",
                "desc": "Remove o Internet Explorer via DISM.",
                "cmds": [
                    'dism /online /Disable-Feature /FeatureName:Internet-Explorer-Optional-amd64 | Out-Null; if ($LASTEXITCODE -eq 0) { Write-Host "IE removido com sucesso" } else { Write-Host "IE nao encontrado" }',
                ],
            },
            {
                "id": "disable_fax",
                "name": "Desativar Fax e Digitalização",
                "desc": "Remove o serviço de Fax e Digitalização do Windows.",
                "cmds": [
                    'dism /Online /Disable-Feature /FeatureName:FaxServicesClientPackage | Out-Null; if ($LASTEXITCODE -eq 0) { Write-Host "Fax removido com sucesso" } else { Write-Host "Fax nao encontrado" }',
                ],
            },
            {
                "id": "disable_consumer",
                "name": "Desativar Consumer Features",
                "desc": "Bloqueia instalação automática de apps sugeridos e recursos de consumidor.",
                "cmds": [
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\CloudContent" /v "DisableWindowsConsumerFeatures" /t "REG_DWORD" /d "1" /f',
                    'reg add "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\ContentDeliveryManager" /v "ContentDeliveryAllowed" /d "0" /t REG_DWORD /f',
                    'reg add "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\ContentDeliveryManager" /v "OemPreInstalledAppsEnabled" /d "0" /t REG_DWORD /f',
                    'reg add "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\ContentDeliveryManager" /v "PreInstalledAppsEnabled" /d "0" /t REG_DWORD /f',
                    'reg add "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\ContentDeliveryManager" /v "SilentInstalledAppsEnabled" /d "0" /t REG_DWORD /f',
                ],
            },
        ],
    },

    "Privacidade": {
        "icon": "🔒",
        "items": [
            {
                "id": "priv_account_info",
                "name": "Bloquear acesso à Conta",
                "desc": "Impede que apps acessem informações da conta do usuário.",
                "cmds": ['reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\CapabilityAccessManager\\ConsentStore\\userAccountInformation" /v "Value" /d "Deny" /f'],
            },
            {
                "id": "priv_contacts",
                "name": "Bloquear acesso a Contatos",
                "desc": "Impede que apps acessem sua lista de contatos.",
                "cmds": ['reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\CapabilityAccessManager\\ConsentStore\\contacts" /v "Value" /d "Deny" /t REG_SZ /f'],
            },
            {
                "id": "priv_call_history",
                "name": "Bloquear Histórico de Chamadas",
                "desc": "Impede que apps acessem o histórico de chamadas.",
                "cmds": ['reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\CapabilityAccessManager\\ConsentStore\\phoneCallHistory" /v "Value" /d "Deny" /t REG_SZ /f'],
            },
            {
                "id": "priv_messaging",
                "name": "Bloquear acesso a Mensagens",
                "desc": "Impede que apps leiam ou enviem mensagens.",
                "cmds": ['reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\CapabilityAccessManager\\ConsentStore\\chat" /v "Value" /d "Deny" /t REG_SZ /f'],
            },
            {
                "id": "priv_notifications",
                "name": "Bloquear acesso a Notificações",
                "desc": "Impede que apps acessem suas notificações.",
                "cmds": ['reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\CapabilityAccessManager\\ConsentStore\\userNotificationListener" /v "Value" /d "Deny" /f'],
            },
            {
                "id": "priv_email",
                "name": "Bloquear acesso a E-mail",
                "desc": "Impede que apps acessem seu e-mail.",
                "cmds": ['reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\CapabilityAccessManager\\ConsentStore\\email" /v "Value" /d "Deny" /t REG_SZ /f'],
            },
            {
                "id": "priv_tasks",
                "name": "Bloquear acesso a Tarefas",
                "desc": "Impede que apps acessem dados de tarefas do usuário.",
                "cmds": ['reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\CapabilityAccessManager\\ConsentStore\\userDataTasks" /v "Value" /d "Deny" /t REG_SZ /f'],
            },
            {
                "id": "priv_diagnostics",
                "name": "Bloquear Diagnósticos de Apps",
                "desc": "Impede que apps coletem dados de diagnóstico de outros apps.",
                "cmds": ['reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\CapabilityAccessManager\\ConsentStore\\appDiagnostics" /v "Value" /d "Deny" /t REG_SZ /f'],
            },
            {
                "id": "priv_voice",
                "name": "Desativar Ativação por Voz",
                "desc": "Desativa a ativação por voz (Cortana, Alexa, etc.) para todos os apps.",
                "cmds": ['reg add "HKCU\\Software\\Microsoft\\Speech_OneCore\\Settings\\VoiceActivation\\UserPreferenceForAllApps" /v "AgentActivationEnabled" /t REG_DWORD /d 0 /f'],
            },
            {
                "id": "priv_phone",
                "name": "Bloquear acesso ao Telefone",
                "desc": "Impede que apps façam ou acessem chamadas telefônicas.",
                "cmds": ['reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\AppPrivacy" /v "LetAppsAccessPhone" /t REG_DWORD /d 2 /f'],
            },
            {
                "id": "priv_calendar",
                "name": "Bloquear acesso ao Calendário",
                "desc": "Impede que apps acessem seu calendário.",
                "cmds": ['reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\CapabilityAccessManager\\ConsentStore\\appointments" /v "Value" /d "Deny" /t REG_SZ /f'],
            },
            {
                "id": "priv_motion",
                "name": "Bloquear Sensores de Movimento",
                "desc": "Impede que apps acessem sensores de atividade/movimento.",
                "cmds": ['reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\CapabilityAccessManager\\ConsentStore\\activity" /v "Value" /d "Deny" /f'],
            },
            {
                "id": "priv_radio",
                "name": "Bloquear acesso ao Rádio",
                "desc": "Impede que apps controlem rádios (Bluetooth, Wi-Fi).",
                "cmds": ['reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\CapabilityAccessManager\\ConsentStore\\radios" /v "Value" /d "Deny" /t REG_SZ /f'],
            },
            {
                "id": "priv_recordings",
                "name": "Bloquear Captura de Tela Programática",
                "desc": "Impede que apps capturem a tela de outros programas.",
                "cmds": [
                    'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\CapabilityAccessManager\\ConsentStore\\graphicsCaptureProgrammatic" /v "Value" /d "Deny" /t REG_SZ /f',
                    'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\CapabilityAccessManager\\ConsentStore\\graphicsCaptureWithoutBorder" /v "Value" /d "Deny" /t REG_SZ /f',
                ],
            },
            {
                "id": "priv_ai_models",
                "name": "Bloquear Modelos de IA do Sistema",
                "desc": "Impede que apps usem modelos de IA integrados ao Windows.",
                "cmds": ['reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\CapabilityAccessManager\\ConsentStore\\systemAIModels" /v "Value" /d "Deny" /t REG_SZ /f'],
            },
            {
                "id": "priv_lock_camera",
                "name": "Desativar Câmera na Tela de Bloqueio",
                "desc": "Impede o acesso à câmera sem desbloqueio do sistema.",
                "cmds": ['reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\Personalization" /v "NoLockScreenCamera" /t REG_DWORD /d 1 /f'],
            },
            {
                "id": "priv_biometrics",
                "name": "Desativar Biometria",
                "desc": "Desativa reconhecimento biométrico (Windows Hello deixará de funcionar).",
                "cmds": [
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Biometrics" /v "Enabled" /t REG_DWORD /d "0" /f',
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Biometrics\\Credential Provider" /v "Enabled" /t "REG_DWORD" /d "0" /f',
                ],
            },
            {
                "id": "priv_cloud_speech",
                "name": "Desativar Reconhecimento de Voz Online",
                "desc": "Bloqueia envio de dados de voz para servidores da Microsoft.",
                "cmds": [
                    'reg add "HKCU\\Software\\Microsoft\\Speech_OneCore\\Settings\\OnlineSpeechPrivacy" /v "HasAccepted" /t REG_DWORD /d 0 /f',
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\InputPersonalization" /v "AllowInputPersonalization" /t REG_DWORD /d 0 /f',
                ],
            },
        ],
    },

    "Telemetria": {
        "icon": "📡",
        "items": [
            {
                "id": "tele_windows",
                "name": "Desativar Telemetria do Windows",
                "desc": "Desativa coleta de diagnóstico, CEIP, relatórios de erro e DiagTrack.",
                "cmds": [
                    'Disable-ScheduledTask -TaskName "\\Microsoft\\Windows\\Customer Experience Improvement Program\\Consolidator" -ErrorAction SilentlyContinue',
                    'Disable-ScheduledTask -TaskName "\\Microsoft\\Windows\\Customer Experience Improvement Program\\KernelCeipTask" -ErrorAction SilentlyContinue',
                    'Disable-ScheduledTask -TaskName "\\Microsoft\\Windows\\Customer Experience Improvement Program\\UsbCeip" -ErrorAction SilentlyContinue',
                    'Disable-ScheduledTask -TaskName "\\Microsoft\\Windows\\Autochk\\Proxy" -ErrorAction SilentlyContinue',
                    'Disable-ScheduledTask -TaskName "\\Microsoft\\Windows\\Windows Error Reporting\\QueueReporting" -ErrorAction SilentlyContinue',
                    'Set-Service -Name "DiagTrack" -StartupType Manual -ErrorAction SilentlyContinue',
                    'Set-Service -Name "WerSvc" -StartupType Manual -ErrorAction SilentlyContinue',
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\DataCollection" /v "AllowTelemetry" /t REG_DWORD /d 0 /f',
                    'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\DataCollection" /v "AllowTelemetry" /t REG_DWORD /d 0 /f',
                    'reg add "HKLM\\Software\\Policies\\Microsoft\\Windows\\Windows Error Reporting" /v "Disabled" /t REG_DWORD /d "1" /f',
                    'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\Windows Error Reporting" /v "Disabled" /t "REG_DWORD" /d "1" /f',
                ],
            },
            {
                "id": "tele_ads",
                "name": "Desativar Anúncios e Dados Personalizados",
                "desc": "Remove anúncios direcionados, Windows Spotlight e conteúdo personalizado.",
                "cmds": [
                    'reg add "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\AdvertisingInfo" /v "Enabled" /t REG_DWORD /d "0" /f',
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\AdvertisingInfo" /v "DisabledByGroupPolicy" /t REG_DWORD /d "1" /f',
                    'reg add "HKLM\\Software\\Policies\\Microsoft\\Windows\\CloudContent" /v "DisableWindowsSpotlightFeatures" /t "REG_DWORD" /d "1" /f',
                    'reg add "HKLM\\Software\\Policies\\Microsoft\\Windows\\CloudContent" /v "DisableTailoredExperiencesWithDiagnosticData" /t "REG_DWORD" /d "1" /f',
                    'reg add "HKLM\\Software\\Microsoft\\Windows\\CurrentVersion\\SystemSettings\\AccountNotifications" /v "EnableAccountNotifications" /t REG_DWORD /d "0" /f',
                ],
            },
            {
                "id": "tele_search",
                "name": "Desativar Telemetria do Windows Search",
                "desc": "Remove pesquisa online, Bing, Cortana e histórico de buscas.",
                "cmds": [
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\Windows Search" /v "AllowCortana" /t "REG_DWORD" /d "0" /f',
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\Windows Search" /v "ConnectedSearchUseWeb" /t "REG_DWORD" /d "0" /f',
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\Windows Search" /v "DisableWebSearch" /t "REG_DWORD" /d "1" /f',
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\Windows Search" /v "AllowCloudSearch" /t "REG_DWORD" /d "0" /f',
                    'reg add "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Search" /v "BingSearchEnabled" /t "REG_DWORD" /d "0" /f',
                    'reg add "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\SearchSettings" /v "IsMSACloudSearchEnabled" /t REG_DWORD /d "0" /f',
                    'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\SearchSettings" /v "IsDeviceSearchHistoryEnabled" /t REG_DWORD /d "0" /f',
                ],
            },
            {
                "id": "tele_office",
                "name": "Desativar Telemetria do Office",
                "desc": "Para logging, upload de dados e agentes de telemetria do Microsoft Office.",
                "cmds": [
                    'reg add "HKCU\\SOFTWARE\\Microsoft\\Office\\Common\\ClientTelemetry" /v "DisableTelemetry" /t REG_DWORD /d 1 /f',
                    'reg add "HKCU\\SOFTWARE\\Microsoft\\Office\\16.0\\Common\\ClientTelemetry" /v "DisableTelemetry" /t REG_DWORD /d 1 /f',
                    'reg add "HKCU\\SOFTWARE\\Policies\\Microsoft\\Office\\16.0\\OSM" /v "EnableLogging" /t REG_DWORD /d 0 /f',
                    'reg add "HKCU\\SOFTWARE\\Policies\\Microsoft\\Office\\16.0\\OSM" /v "EnableUpload" /t REG_DWORD /d 0 /f',
                    'reg add "HKCU\\SOFTWARE\\Microsoft\\Office\\16.0\\Common" /v "QMEnable" /t REG_DWORD /d 0 /f',
                    'reg add "HKCU\\SOFTWARE\\Microsoft\\Office\\16.0\\Common\\Feedback" /v "Enabled" /t REG_DWORD /d 0 /f',
                    'Disable-ScheduledTask -TaskName "\\Microsoft\\Office\\OfficeTelemetryAgentFallBack2016" -ErrorAction SilentlyContinue',
                    'Disable-ScheduledTask -TaskName "\\Microsoft\\Office\\OfficeTelemetryAgentLogOn2016" -ErrorAction SilentlyContinue',
                ],
            },
            {
                "id": "tele_nvidia",
                "name": "Desativar Telemetria NVIDIA",
                "desc": "Desativa coleta de dados e tarefas agendadas de telemetria da NVIDIA.",
                "cmds": [
                    'reg add "HKLM\\SOFTWARE\\NVIDIA Corporation\\NvControlPanel2\\Client" /v "OptInOrOutPreference" /t REG_DWORD /d 0 /f',
                    'reg add "HKLM\\SOFTWARE\\NVIDIA Corporation\\Global\\FTS" /v "EnableRID44231" /t REG_DWORD /d 0 /f',
                    'reg add "HKLM\\SOFTWARE\\NVIDIA Corporation\\Global\\FTS" /v "EnableRID64640" /t REG_DWORD /d 0 /f',
                    'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\nvlddmkm\\Global\\Startup" /v "SendTelemetryData" /t REG_DWORD /d 0 /f',
                    'Disable-ScheduledTask -TaskName "NvTmMon_{B2FE1952-0186-46C3-BAEC-A80AA35AC5B8}" -ErrorAction SilentlyContinue',
                    'Disable-ScheduledTask -TaskName "NvTmRep_{B2FE1952-0186-46C3-BAEC-A80AA35AC5B8}" -ErrorAction SilentlyContinue',
                    'Disable-ScheduledTask -TaskName "NvTmRepOnLogon_{B2FE1952-0186-46C3-BAEC-A80AA35AC5B8}" -ErrorAction SilentlyContinue',
                ],
            },
            {
                "id": "tele_adobe",
                "name": "Desativar Telemetria Adobe",
                "desc": "Bloqueia servidores de telemetria da Adobe via hosts file.",
                "cmds": [
                    '$hosts = "$env:windir\\System32\\drivers\\etc\\hosts"; try { $list = (Invoke-WebRequest -Uri "https://a.dove.isdumb.one/list.txt" -ErrorAction Stop).Content; Add-Content -Path $hosts -Value $list; Write-Host "Bloqueio Adobe aplicado." } catch { Write-Host "Falha ao baixar lista Adobe." }',
                ],
            },
            {
                "id": "tele_activity_feed",
                "name": "Desativar Feed de Atividades",
                "desc": "Desativa publicação e upload de atividades do usuário.",
                "cmds": [
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\System" /v "EnableActivityFeed" /d "0" /t REG_DWORD /f',
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\System" /v "PublishUserActivities" /t REG_DWORD /d "0" /f',
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\System" /v "UploadUserActivities" /t REG_DWORD /d "0" /f',
                ],
            },
            {
                "id": "tele_cloud_sync",
                "name": "Desativar Sincronização na Nuvem",
                "desc": "Desativa sincronização de configurações, temas e credenciais com a nuvem.",
                "cmds": [
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\SettingSync" /v "DisableSettingSync" /t REG_DWORD /d 2 /f',
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\SettingSync" /v "DisableSettingSyncUserOverride" /t REG_DWORD /d 1 /f',
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\SettingSync" /v "DisableCredentialsSettingSync" /t REG_DWORD /d 2 /f',
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\SettingSync" /v "DisableApplicationSettingSync" /t REG_DWORD /d 2 /f',
                    'reg add "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\SettingSync" /v "SyncPolicy" /t REG_DWORD /d 5 /f',
                ],
            },
            {
                "id": "tele_vs",
                "name": "Desativar Telemetria do Visual Studio",
                "desc": "Para SQM, IntelliCode remoto e feedback do Visual Studio.",
                "cmds": [
                    'reg add "HKLM\\SOFTWARE\\Wow6432Node\\Microsoft\\VSCommon\\17.0\\SQM" /v "OptIn" /t REG_DWORD /d 0 /f',
                    'reg add "HKCU\\Software\\Microsoft\\VisualStudio\\Telemetry" /v "TurnOffSwitch" /t REG_DWORD /d 1 /f',
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\VisualStudio\\IntelliCode" /v "DisableRemoteAnalysis" /t "REG_DWORD" /d "1" /f',
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\VisualStudio\\Feedback" /v "DisableFeedbackDialog" /t REG_DWORD /d 1 /f',
                ],
            },
            {
                "id": "tele_powershell",
                "name": "Desativar Telemetria do PowerShell",
                "desc": "Define variável de ambiente para optar por não participar da telemetria do PowerShell.",
                "cmds": ['[System.Environment]::SetEnvironmentVariable("POWERSHELL_TELEMETRY_OPTOUT", "1", "Machine")'],
            },
            {
                "id": "tele_ccleaner",
                "name": "Desativar Telemetria CCleaner",
                "desc": "Para monitoramento, atualização automática e telemetria do CCleaner.",
                "cmds": [
                    'reg add "HKCU\\Software\\Piriform\\CCleaner" /v "Monitoring" /t REG_DWORD /d 0 /f',
                    'reg add "HKCU\\Software\\Piriform\\CCleaner" /v "HelpImproveCCleaner" /t REG_DWORD /d 0 /f',
                    'reg add "HKCU\\Software\\Piriform\\CCleaner" /v "UpdateAuto" /t REG_DWORD /d 0 /f',
                    'reg add "HKCU\\Software\\Piriform\\CCleaner" /v "UpdateCheck" /t REG_DWORD /d 0 /f',
                ],
            },
            {
                "id": "tele_appexp",
                "name": "Desativar Telemetria de Compatibilidade",
                "desc": "Para tarefas de experiência de aplicativos e compatibilidade do Windows.",
                "cmds": [
                    'Disable-ScheduledTask -TaskName "\\Microsoft\\Windows\\Application Experience\\Microsoft Compatibility Appraiser" -ErrorAction SilentlyContinue',
                    'Disable-ScheduledTask -TaskName "\\Microsoft\\Windows\\Application Experience\\StartupAppTask" -ErrorAction SilentlyContinue',
                    'Disable-ScheduledTask -TaskName "\\Microsoft\\Windows\\Application Experience\\PcaPatchDbTask" -ErrorAction SilentlyContinue',
                ],
            },
        ],
    },

    "Gaming": {
        "icon": "🎮",
        "items": [
            {
                "id": "game_perf_plan",
                "name": "Plano Ultimate Performance",
                "desc": "Ativa o plano de energia de máximo desempenho do Windows.",
                "cmds": [
                    '$plan = powercfg -list | Select-String "Ultimate Performance"; if (-not $plan) { powercfg -duplicatescheme e9a42b02-d5df-448d-aa00-03f14749eb61 2>&1 | Out-Null }; $guid = (powercfg -list | Select-String "Ultimate Performance").Line.Split()[3]; if ($guid) { powercfg -setactive $guid; Write-Host "Plano Ultimate Performance ativado: $guid" } else { Write-Host "Falha ao obter GUID do plano." }',
                ],
            },
            {
                "id": "game_mouse_accel",
                "name": "Desativar Aceleração do Mouse",
                "desc": "Remove a aceleração do ponteiro para movimentos 1:1 mais precisos.",
                "cmds": [
                    'reg add "HKCU\\Control Panel\\Mouse" /v "MouseSpeed" /t REG_SZ /d "0" /f',
                    'reg add "HKCU\\Control Panel\\Mouse" /v "MouseThreshold1" /t REG_SZ /d "0" /f',
                    'reg add "HKCU\\Control Panel\\Mouse" /v "MouseThreshold2" /t REG_SZ /d "0" /f',
                ],
            },
            {
                "id": "game_bar",
                "name": "Desativar Game Bar / Xbox DVR",
                "desc": "Remove a Game Bar e gravação de tela do Xbox.",
                "cmds": [
                    'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\GameDVR" /v "AppCaptureEnabled" /t REG_DWORD /d 0 /f',
                    'reg add "HKCU\\SOFTWARE\\Microsoft\\GameBar" /v "UseNexusForGameBarEnabled" /t REG_DWORD /d 0 /f',
                    'reg add "HKCU\\SOFTWARE\\Microsoft\\GameBar" /v "ShowStartupPanel" /t REG_DWORD /d 0 /f',
                    'reg add "HKCU\\System\\GameConfigStore" /v "GameDVR_Enabled" /t REG_DWORD /d 0 /f',
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\GameDVR" /v "AllowGameDVR" /t REG_DWORD /d 0 /f',
                ],
            },
            {
                "id": "game_fullscreen_opt",
                "name": "Desativar Fullscreen Optimizations",
                "desc": "Desativa otimizações de tela cheia do DX que podem causar latência.",
                "cmds": ['reg add "HKCU\\System\\GameConfigStore" /v "GameDVR_DXGIHonorFSEWindowsCompatible" /t REG_DWORD /d 1 /f'],
            },
            {
                "id": "game_hags",
                "name": "Desativar HAGS",
                "desc": "Desativa Hardware-Accelerated GPU Scheduling para reduzir latência.",
                "cmds": ['reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\GraphicsDrivers" /v "HwSchMode" /t REG_DWORD /d 1 /f'],
            },
            {
                "id": "game_mpo",
                "name": "Desativar MPO (Multiplane Overlay)",
                "desc": "Corrige stuttering e artefatos visuais causados pelo MPO.",
                "cmds": ['reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\Dwm" /v "OverlayTestMode" /t REG_DWORD /d "5" /f'],
            },
            {
                "id": "game_core_isolation",
                "name": "Desativar Core Isolation (HVCI)",
                "desc": "Desativa isolamento de núcleo para reduzir overhead de CPU em jogos.",
                "cmds": ['reg add "HKLM\\System\\CurrentControlSet\\Control\\DeviceGuard\\Scenarios\\HypervisorEnforcedCodeIntegrity" /v "Enabled" /t REG_DWORD /d 0 /f'],
            },
        ],
    },

    "Performance": {
        "icon": "⚡",
        "items": [
            {
                "id": "perf_prefetch",
                "name": "Desativar Prefetch / SysMain",
                "desc": "Para o serviço SysMain (Superfetch) que pré-carrega dados na RAM.",
                "cmds": [
                    'Stop-Service -Name "sysmain" -ErrorAction SilentlyContinue',
                    'Set-Service -Name "sysmain" -StartupType Disabled -ErrorAction SilentlyContinue',
                ],
            },
            {
                "id": "perf_search_svc",
                "name": "Desativar Windows Search",
                "desc": "Desativa a indexação de arquivos do Windows Search.",
                "cmds": [
                    'Stop-Service -Name "wsearch" -ErrorAction SilentlyContinue',
                    'Set-Service -Name "wsearch" -StartupType Disabled -ErrorAction SilentlyContinue',
                ],
            },
            {
                "id": "perf_hibernate",
                "name": "Desativar Hibernação",
                "desc": "Desativa hibernação e remove o arquivo hiberfil.sys (libera espaço).",
                "cmds": ['powercfg /h off'],
            },
            {
                "id": "perf_storage_sense",
                "name": "Desativar Storage Sense",
                "desc": "Desativa limpeza automática de armazenamento do Windows.",
                "cmds": ['reg add "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\StorageSense\\Parameters\\StoragePolicy" /v "01" /t REG_DWORD /d 0 /f'],
            },
            {
                "id": "perf_mouse_delay",
                "name": "Remover Delay do Mouse / Menu",
                "desc": "Define atrasos de menus e hover do mouse para zero.",
                "cmds": [
                    'reg add "HKCU\\Control Panel\\Desktop" /v "MenuShowDelay" /t REG_SZ /d 0 /f',
                    'reg add "HKCU\\Control Panel\\Mouse" /v "MouseHoverTime" /t REG_SZ /d 0 /f',
                ],
            },
            {
                "id": "perf_transparency",
                "name": "Desativar Transparência",
                "desc": "Desativa efeitos de transparência da interface para reduzir carga na GPU.",
                "cmds": ['reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize" /v "EnableTransparency" /t REG_DWORD /d 0 /f'],
            },
        ],
    },

    "Interface": {
        "icon": "🖥",
        "items": [
            {
                "id": "ui_dark_mode",
                "name": "Ativar Dark Mode",
                "desc": "Define o tema escuro para apps e sistema.",
                "cmds": [
                    'reg add "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize" /v "AppsUseLightTheme" /t REG_DWORD /d 0 /f',
                    'reg add "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize" /v "SystemUsesLightTheme" /t REG_DWORD /d 0 /f',
                ],
            },
            {
                "id": "ui_classic_menu",
                "name": "Menu de Contexto Clássico",
                "desc": 'Restaura o menu de clique direito antigo sem "Mostrar mais opções".',
                "cmds": ['reg add "HKCU\\Software\\Classes\\CLSID\\{86ca1aa0-34aa-4e8b-a509-50c905bae2a2}\\InprocServer32" /f /ve'],
            },
            {
                "id": "ui_end_task",
                "name": "Encerrar Tarefa no Clique Direito",
                "desc": "Adiciona opção de encerrar processo pela barra de tarefas.",
                "cmds": ['reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced\\TaskbarDeveloperSettings" /v "TaskbarEndTask" /t REG_DWORD /d "1" /f'],
            },
            {
                "id": "ui_file_ext",
                "name": "Mostrar Extensões de Arquivo",
                "desc": "Exibe as extensões de arquivo no Explorer (.exe, .txt, etc.).",
                "cmds": ['reg add "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced" /v "HideFileExt" /t REG_DWORD /d 0 /f'],
            },
            {
                "id": "ui_sticky_keys",
                "name": "Desativar Sticky Keys",
                "desc": "Remove o popup irritante de teclas de aderência.",
                "cmds": ['reg add "HKCU\\Control Panel\\Accessibility\\StickyKeys" /v "Flags" /t REG_SZ /d "58" /f'],
            },
            {
                "id": "ui_snap_assist",
                "name": "Desativar Snap Assist Flyout",
                "desc": "Remove o popup de layout de snap ao passar o mouse no botão maximizar.",
                "cmds": ['reg add "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced" /v "EnableSnapAssistFlyout" /t REG_DWORD /d 0 /f'],
            },
            {
                "id": "ui_numlock",
                "name": "Desativar Num Lock no Boot",
                "desc": "Define o Num Lock como desativado ao inicializar o Windows.",
                "cmds": ['reg add "HKCU\\Control Panel\\Keyboard" /v "InitialKeyboardIndicators" /t REG_SZ /d "0" /f'],
            },
            {
                "id": "ui_notification_center",
                "name": "Desativar Central de Notificações",
                "desc": "Desativa a central de ações e notificações da bandeja do sistema.",
                "cmds": ['reg add "HKCU\\Software\\Policies\\Microsoft\\Windows\\Explorer" /v "DisableNotificationCenter" /d "1" /t REG_DWORD /f'],
            },
            {
                "id": "ui_taskbar_widgets",
                "name": "Desativar Botão de Widgets",
                "desc": "Remove o botão de widgets e feeds de notícias da barra de tarefas.",
                "cmds": [
                    'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced" /v "ShowTaskViewButton" /t REG_DWORD /d 0 /f',
                    'reg add "HKLM\\SOFTWARE\\Microsoft\\PolicyManager\\default\\NewsAndInterests\\AllowNewsAndInterests" /v "value" /t REG_DWORD /d 0 /f',
                ],
            },
        ],
    },

    "Atualizações": {
        "icon": "🔄",
        "items": [
            {
                "id": "upd_windows",
                "name": "Desativar Windows Update",
                "desc": "Para serviços, tarefas agendadas e entrega do Windows Update.",
                "cmds": [
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\WindowsUpdate\\AU" /v "NoAutoUpdate" /t REG_DWORD /d "1" /f',
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\WindowsUpdate\\AU" /v "AUOptions" /t REG_DWORD /d "1" /f',
                    '$s = @("BITS","wuauserv","UsoSvc"); foreach ($svc in $s) { Stop-Service -Name $svc -ErrorAction SilentlyContinue; Set-Service -Name $svc -StartupType Disabled -ErrorAction SilentlyContinue }',
                    'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\DeliveryOptimization\\Config" /v "DODownloadMode" /t REG_DWORD /d "0" /f',
                    '$paths = @("\\Microsoft\\Windows\\InstallService\\","\\Microsoft\\Windows\\UpdateOrchestrator\\","\\Microsoft\\Windows\\WindowsUpdate\\"); foreach ($p in $paths) { Get-ScheduledTask -TaskPath "$p*" -ErrorAction SilentlyContinue | Disable-ScheduledTask -ErrorAction SilentlyContinue }',
                ],
            },
            {
                "id": "upd_pause_limit",
                "name": "Estender Pausa do Windows Update (20 anos)",
                "desc": "Permite pausar atualizações por até 20 anos pelas configurações do Windows.",
                "cmds": ['reg add "HKLM\\SOFTWARE\\Microsoft\\WindowsUpdate\\UX\\Settings" /v "FlightSettingsMaxPauseDays" /t REG_DWORD /d 7300 /f'],
            },
            {
                "id": "upd_store",
                "name": "Desativar Atualizações Automáticas da Store",
                "desc": "Bloqueia download automático de apps pela Microsoft Store.",
                "cmds": ['reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\WindowsStore" /v "AutoDownload" /t REG_DWORD /d 2 /f'],
            },
            {
                "id": "upd_google",
                "name": "Desativar Atualizações do Google",
                "desc": "Desativa serviços de atualização automática do Google (Chrome, etc.).",
                "cmds": [
                    'Set-Service -Name "gupdate" -StartupType Disabled -ErrorAction SilentlyContinue',
                    'Set-Service -Name "gupdatem" -StartupType Disabled -ErrorAction SilentlyContinue',
                ],
            },
            {
                "id": "upd_adobe",
                "name": "Desativar Atualizações da Adobe",
                "desc": "Para atualização automática dos produtos Adobe.",
                "cmds": [
                    'Disable-ScheduledTask -TaskName "\\Adobe Acrobat Update Task" -ErrorAction SilentlyContinue',
                    'Set-Service -Name "AdobeARMservice" -StartupType Disabled -ErrorAction SilentlyContinue',
                    'Set-Service -Name "adobeupdateservice" -StartupType Disabled -ErrorAction SilentlyContinue',
                ],
            },
            {
                "id": "upd_maps",
                "name": "Desativar Download Automático de Mapas",
                "desc": "Bloqueia download e atualização automática de mapas offline.",
                "cmds": [
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\Maps" /v "AutoDownloadAndUpdateMapData" /t REG_DWORD /d 0 /f',
                    'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\Maps" /v "AllowUntriggeredNetworkTrafficOnSettingsPage" /t REG_DWORD /d 0 /f',
                ],
            },
        ],
    },

    "Instalar Apps": {
        "icon": "📦",
        "items": [
            {
                "id": "app_cpuz",
                "name": "CPU-Z",
                "desc": "Monitora informações detalhadas do processador, memória e placa-mãe.",
                "cmds": ['winget install CPUID.CPU-Z --accept-source-agreements --accept-package-agreements --force'],
            },
            {
                "id": "app_gpuz",
                "name": "GPU-Z",
                "desc": "Exibe informações detalhadas sobre a placa de vídeo e VRAM.",
                "cmds": ['winget install TechPowerUp.GPU-Z --accept-source-agreements --accept-package-agreements --force'],
            },
            {
                "id": "app_afterburner",
                "name": "MSI Afterburner",
                "desc": "Overclock, monitoramento de GPU e overlay de FPS em tempo real.",
                "cmds": ['winget install Guru3D.Afterburner --accept-source-agreements --accept-package-agreements --force'],
            },
            {
                "id": "app_winget_update",
                "name": "Atualizar Winget",
                "desc": "Atualiza o Winget para a versão mais recente (necessário para as instalações acima).",
                "cmds": [
                    '$v = winget -v 2>$null; try { if ([version]($v.TrimStart("v")) -lt [version]"1.7.0") { Set-Location $env:USERPROFILE; Invoke-WebRequest -Uri "https://aka.ms/getwinget" -OutFile "winget.msixbundle"; Add-AppPackage -ForceApplicationShutdown .\\winget.msixbundle; Remove-Item .\\winget.msixbundle } else { Write-Host "Winget ja esta atualizado." } } catch { Write-Host "Falha ao verificar/atualizar winget." }',
                ],
            },
        ],
    },
}
