# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['../scan2folder.py'],
             pathex=['../'],
             binaries=[],
             datas=[('../*.ui', '.'),('../images/*.svg','.')],
             hiddenimports=['packaging.requirements'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
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
          name='scan2folder',
          exclude_binaries=False,
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir="/tmp",
          console=False )
