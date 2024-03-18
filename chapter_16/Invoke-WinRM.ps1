# Import the Active Directory module
    Import-Module ActiveDirectory
    # Static credentials
    $username = "DOMAIN\Administrator"
    $password = ConvertTo-SecureString "Testim123!" -AsPlainText -Force
    # Create credential object
    $credential = New-Object System.Management.Automation.PSCredential ($username,
    $password)
    # Get all AD computers
    $computers = Get-ADComputer -Filter *
    # Iterate through each computer
foreach ($computer in $computers) { # Get the computer name $computerName = $computer.Name
    # Attempt to connect using Invoke-Command
try {
Invoke-Command -ComputerName $computerName -Credential $credential -
    ScriptBlock { Write-Output "Connection Successful" } -ErrorAction Stop
            Write-Output "Success: Able to connect to WinRM on $computerName"
} catch {
Write-Output "Failed: Unable to connect to WinRM on $computerName"
} }
