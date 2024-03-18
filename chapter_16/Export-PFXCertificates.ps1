# Secure password creation for exporting certificates
    $exportPassword = ConvertTo-SecureString -String "YourPassword" -Force -
    AsPlainText
    # Retrieving certificate paths from the local machine
    $ListOfCertificates = Get-ChildItem -Path cert:\LocalMachine -Recurse
    # Looping through each certificate
foreach ($SingleCert in $ListOfCertificates) {
        # Checking if the certificate has a thumbprint
if ($SingleCert.Thumbprint) {
            # Generating a unique file name for the PFX file
            $GeneratedFileName = [System.IO.Path]::GetRandomFileName()
            $PfxFileDestination = "$env:USERPROFILE\Downloads\$GeneratedFile
    Name.pfx"
            # Attempting to export the certificate
try {
Export-PfxCertificate -Cert $SingleCert -FilePath $PfxFileDestina
    tion -Password $exportPassword -ErrorAction SilentlyContinue
            }
catch [System.ComponentModel.Win32Exception],[Microsoft.CertificateServi ces.Commands.ExportPfxCertificate] {
          # Handling exceptions silently
} }
}

