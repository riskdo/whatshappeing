[Setup]
AppName=what'shappeing
AppVersion=1.0.0
DefaultDirName={pf}\whatshappeing
DefaultGroupName=what'shappeing
OutputDir=.
OutputBaseFilename=whatshappeingSetup-1.0.0
Compression=lzma
SolidCompression=yes

[Files]
Source: "..\dist\whatshappeing.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\what'shappeing"; Filename: "{app}\whatshappeing.exe"
Name: "{commondesktop}\what'shappeing"; Filename: "{app}\whatshappeing.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a desktop icon"; GroupDescription: "Additional icons:"