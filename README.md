# Markdown Live Editor

Windows 환경에서 실행되는 Python 데스크톱 Markdown 편집기입니다. 왼쪽에서 Markdown 원문을 작성하고, 오른쪽에서 HTML 렌더링 결과를 실시간으로 확인할 수 있습니다.

## 주요 기능

- Markdown 문서 작성, 편집, 새 문서 생성
- `.md`, `.markdown`, `.txt` 파일 열기
- 저장, 다른 이름으로 저장
- GitHub README 스타일 실시간 HTML 미리보기
- 제목, 굵게, 기울임, 취소선, 목록, 체크박스, 인용문, 코드블록, 표, 링크, 이미지, 수평선 지원
- CSS가 포함된 완성형 HTML 파일 내보내기
- `Ctrl + F` 검색 패널
- 전체 검색 결과 하이라이트 및 현재 검색 결과 강조
- 대소문자 구분 검색
- 라이트모드와 다크모드 전환
- 종료 전 저장되지 않은 변경사항 확인

## 파일 구성

| 파일 | 설명 |
|---|---|
| `main.py` | Markdown Editor GUI 프로그램 코드 |
| `requirements.txt` | 필요한 Python 패키지 목록 |
| `install_venv.bat` | 가상환경 생성 및 패키지 설치 |
| `run.bat` | Windows 탐색기 더블클릭 실행 |
| `build_exe.bat` | PyInstaller exe 빌드 |
| `README.md` | 설치, 실행, 기능 설명 |

## 설치

Python 3.11 이상을 설치한 뒤, Windows 탐색기에서 `install_venv.bat`을 더블클릭합니다. 이 배치 파일은 `.venv` 가상환경을 생성하고 필요한 패키지를 설치합니다.

수동으로 설치하려면 이 폴더에서 다음 명령을 실행합니다.

```bat
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## 실행

Windows 탐색기에서 `run.bat`을 더블클릭합니다.

```bat
run.bat
```

`run.bat`은 `.venv\Scripts\pythonw.exe`가 있으면 이를 우선 사용합니다. 그래서 QtWebEngine 내부 Chromium의 GPU 관련 진단 로그가 콘솔 창에 표시되지 않습니다.

터미널에서 직접 실행하려면 다음 명령을 사용할 수 있습니다.

```bat
.venv\Scripts\python.exe main.py
```

단, 터미널에서 직접 실행하면 QtWebEngine/Chromium의 GPU 관련 로그가 표시될 수 있습니다. 앱이 정상 실행된다면 일반적으로 무시해도 됩니다.

## 단축키

| 기능 | 단축키 |
|---|---|
| 새 문서 | Ctrl + N |
| 열기 | Ctrl + O |
| 저장 | Ctrl + S |
| 다른 이름으로 저장 | Ctrl + Shift + S |
| 찾기 | Ctrl + F |
| 모두 선택 | Ctrl + A |
| 종료 | Ctrl + Q |

검색 패널에서는 `Enter`로 다음 결과, `Shift + Enter`로 이전 결과, `Esc`로 닫기를 수행합니다.

## HTML 내보내기

메뉴에서 `파일 > HTML 내보내기`를 선택하면 현재 Markdown 문서를 CSS가 포함된 HTML 파일로 저장합니다. 저장된 HTML은 브라우저에서 바로 열어도 스타일이 적용됩니다.

## exe 빌드

`build_exe.bat`을 실행하면 PyInstaller로 실행 파일을 생성합니다.

```bat
build_exe.bat
```

빌드가 완료되면 다음 경로에 exe 파일이 생성됩니다.

```text
dist\Markdown Live Editor\Markdown Live Editor.exe
```

현재 빌드는 PyInstaller의 기본 `onedir` 방식입니다. 따라서 배포할 때는 `Markdown Live Editor.exe`만 복사하지 말고, 아래 폴더 전체를 함께 배포해야 합니다.

```text
dist\Markdown Live Editor\
```

이 폴더 안에는 실행 파일과 `_internal` 폴더가 함께 들어 있습니다. `_internal` 폴더에는 PySide6, QtWebEngine, Markdown 확장 모듈 등 실행에 필요한 파일이 포함됩니다.

## 빌드 참고

Markdown 체크박스와 취소선을 지원하기 위해 `pymdown-extensions`를 사용합니다. `build_exe.bat`에는 PyInstaller가 동적 import 모듈을 빠뜨리지 않도록 다음 옵션이 포함되어 있습니다.

```bat
--hidden-import pymdownx.tasklist
--hidden-import pymdownx.tilde
--collect-submodules pymdownx
```

하나의 exe 파일만 만드는 `--onefile` 방식도 가능하지만, PySide6와 QtWebEngine 앱은 실행 시작이 느려지고 리소스 처리 문제가 생길 수 있습니다. 안정성을 우선해 현재 프로젝트는 `onedir` 방식을 사용합니다.

## 사용 기술

- Python 3.11 이상
- PySide6
- PySide6.QtWebEngineWidgets의 `QWebEngineView`
- markdown
- pymdown-extensions
- PyInstaller
