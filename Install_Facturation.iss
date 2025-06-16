; Script Inno Setup pour créer l'installateur de Facturation

[Setup]
AppName=Facturation
AppVersion=1.1
DefaultDirName={autopf}\Facturation
DefaultGroupName=Facturation
OutputDir=.\installateur
OutputBaseFilename=Install_Facturation
Compression=lzma
SolidCompression=yes
DisableProgramGroupPage=yes
WizardStyle=modern
SetupIconFile=dist\_internal\Asset\icon.ico

; Ajout pour afficher la politique avec bouton d’acceptation
LicenseFile=dist\_internal\politique.txt

[Files]
; Copie l’exécutable principal
Source: "dist\facture.exe"; DestDir: "{app}"; Flags: ignoreversion

; Copie complète du dossier _internal
Source: "dist\_internal\*"; DestDir: "{app}\_internal"; Flags: ignoreversion recursesubdirs createallsubdirs

; Copie spécifique du pilote Access
Source: "dist\_internal\AccessDatabaseEngine_X64.exe"; DestDir: "{tmp}"; Flags: ignoreversion

[Run]
; Installation silencieuse du pilote Access avec élévation
Filename: "{tmp}\AccessDatabaseEngine_X64.exe"; \
    Parameters: "/quiet"; \
    StatusMsg: "Installation du moteur de base de données Microsoft Access..."; \
    Flags: postinstall runhidden shellexec

[Icons]
; Raccourci dans le menu démarrer
Name: "{group}\Facturation"; Filename: "{app}\facture.exe"; IconFilename: "{app}\_internal\Asset\icon.ico"

; Raccourci pour désinstallation
Name: "{group}\Désinstaller Facturation"; Filename: "{uninstallexe}"

; Raccourci sur le bureau
Name: "{commondesktop}\Facturation"; Filename: "{app}\facture.exe"; IconFilename: "{app}\_internal\Asset\icon.ico"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Créer un raccourci sur le bureau"; GroupDescription: "Icônes supplémentaires:"
