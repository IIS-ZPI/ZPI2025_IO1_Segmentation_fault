from PyInstaller.utils.hooks import collect_all

datas = [
    ('init.py', '.'),
    ('src', 'src'),
    ('assets', 'assets'),
]
binaries = []
hiddenimports = []

streamlit_datas, streamlit_binaries, streamlit_hiddenimports = collect_all('streamlit')
datas += streamlit_datas
binaries += streamlit_binaries
hiddenimports += streamlit_hiddenimports

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='app',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
