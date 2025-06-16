# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

datas = [
    ('Authentification', 'Authentification'),
    ('Asset', 'Asset'),
    ('data', 'data'),
    ('src', 'src'),
    ('database.py', '.'),
    ('AccessDatabaseEngine_X64.exe', '.'),
    ('politique.txt', '.'), 
]

a = Analysis(
    ['main.py'],  # ou facture.py selon ton point d'entrée
    pathex=[r'D:\Beny_TFC\Log_Facturation'],  # adapte ce chemin à ton projet
    binaries=[],
    datas=datas,
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='facture',
    debug=False,
    strip=False,
    upx=True,
    console=False,
    icon='Asset/icon.ico'

)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name='facture',
)
