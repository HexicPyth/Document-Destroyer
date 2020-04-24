# -*- mode: python -*-

block_cipher = None


a = Analysis(['TranslateGUI.py'],
             pathex=['C:\\Users\\user\\PycharmProjects\\GTrans\\Portable'],
             binaries=[],
             datas=[],
             hiddenimports=['mtranslate'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=True,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='Text Screwer-upper',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False , icon='icon.ico')
