; Script de Inno Setup para Papucho Foodtruck
; Instrucciones: Abre este archivo en Inno Setup Compiler y compila

#define MyAppName "Papucho Foodtruck"
#define MyAppVersion "1.0"
#define MyAppPublisher "Papucho Foodtruck"
#define MyAppURL "https://www.papuchofoodtruck.com"
#define MyAppExeName "PapuchoFoodtruck.exe"

[Setup]
; Información básica de la aplicación
AppId={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
LicenseFile=
InfoBeforeFile=
InfoAfterFile=
OutputDir=installer
OutputBaseFilename=PapuchoFoodtruck_Setup
SetupIconFile=
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1; Check: not IsAdminInstallMode

[Files]
; Archivo ejecutable principal
Source: "dist\PapuchoFoodtruck.exe"; DestDir: "{app}"; Flags: ignoreversion
; Carpeta data completa (productos, orden, tickets, imágenes)
Source: "dist\data\*"; DestDir: "{app}\data"; Flags: ignoreversion recursesubdirs createallsubdirs
; Incluir imágenes directamente desde la carpeta source (por si PyInstaller no las copió)
Source: "data\imagenes\*"; DestDir: "{app}\data\imagenes"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Code]
procedure InitializeWizard;
begin
  WizardForm.WelcomeLabel1.Caption := 'Bienvenido al instalador de Papucho Foodtruck';
  WizardForm.WelcomeLabel2.Caption := 'Este asistente le guiará a través del proceso de instalación.';
end;
