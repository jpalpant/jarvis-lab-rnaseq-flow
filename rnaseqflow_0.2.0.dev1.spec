# -*- mode: python -*-

block_cipher = None


a = Analysis(['rnaseqflow/__main__.py'],
             pathex=['./rnaseqflow', '/Users/new/Documents/Jarvis Lab/jarvis-lab-rnaseq-flow'],
             binaries=None,
             datas=None,
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None,
             excludes=None,
             win_no_prefer_redirects=None,
             win_private_assemblies=None,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='rnaseqflow_0.2.0.dev1',
          debug=False,
          strip=None,
          upx=True,
          console=True )
