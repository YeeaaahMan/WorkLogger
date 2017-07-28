pyinstaller --workpath=%TEMP%/pyinst ^
            --distpath=%CD%/exe ^
            --onefile --noconsole ^
            --icon=selftimer128.ico  ^
            --name=WorkLogger ^
            --version-file=version-file.txt main3.py