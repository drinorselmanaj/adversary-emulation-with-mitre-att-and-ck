Private Sub Workbook_Open() 
	Dim psCommand As String
	Dim shellApp As Object
	psCommand = "powershell.exe -Command ""& {Start-Process calc.exe}""" , Set shellApp = CreateObject("Shell.Application")
	shellApp.ShellExecute "cmd.exe", "/c " & psCommand, "", "runas", 0 ,
End Sub

