# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

datas = [
    ('Authentification', 'Authentification'),
    ('Asset', 'Asset'),
    ('data', 'data'),
    ('src', 'src'),
    ('database.py', '.'),
]

a = Analysis(
    ['main.py'],
    pathex=[r'D:\Beny_TFC\Log_Facturation'],  # adapte ce chemin
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
