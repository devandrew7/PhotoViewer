# 🖼️ PyQt6 Photo Viewer & Organizer (프로토타입)

> **대용량 폴더도 끊김 없이!** 
> 윈도우 환경에서 폴더별로 이미지를 깔끔하게 분할 조회하고 실시간 배율 조절 및 비동기 지연 로딩을 지원하는 프리미엄 데스크톱 이미지 뷰어입니다.

---

## ✨ 핵심 기능 (Key Features)

* **⚡ 비동기 지연 로딩 (Lazy Loading with Multi-Threading)**:
  * 대량의 이미지를 불러올 때 메인 UI가 얼어버리거나(Freeze) 버벅거리는 문제를 완벽 해결했습니다.
  * 백그라운드 스레드 풀(`QThreadPool` & `QRunnable`)에서 이미지 읽기 및 EXIF 회전, 리사이징 연산을 수행합니다.
  * 화면 영역(Viewport)과 그 위/아래 버퍼 영역에 노출되는 이미지 카드만 실시간으로 순차 로드합니다.
* **📂 하위 폴더 재귀 스캔 & 자동 그룹화 (Recursive Directory Scanning)**:
  * 단일 폴더 탐색뿐 아니라, **하위 디렉토리 내의 모든 이미지 파일**을 스캔하여 폴더별로 **가로 구분선 및 타이틀 헤더**를 생성해 일괄적으로 분리 및 정렬합니다.
  * **다중 선택 지원**: 좌측 폴더 트리 뷰에서 `Ctrl` 또는 `Shift` 키를 누른 채 **복수의 폴더를 동시에 선택**해 결합하여 한 번에 탐색할 수 있습니다.
* **📐 2의 제곱수 단계별 스냅 슬라이더 (Dynamic Snap Sizing)**:
  * 실시간으로 그리드 내 모든 썸네일 크기를 `16px`, `32px`, `64px`, `128px`, `256px`, `512px` 등 **2의 제곱수 배율 단계로 정밀하고 민첩하게 스냅 스케일링**합니다.
  * 원본 비율(Aspect Ratio)을 완벽히 보존하며, 크기 조절에 따라 반응형 바둑판 레이아웃(`FlowLayout`)이 매끄럽게 재배치(Wrap)됩니다.
* **⚠️ 대용량 안전 로딩 경고 (QMessageBox Safety Alert)**:
  * 스캔된 총 이미지 수가 **500개를 초과할 시**, 사용자에게 성능 경고 알림창을 띄워 로딩 속도 저하를 안전하게 방지할 수 있습니다.
* **🎨 프리미엄 플루언트 라이트 테마 (Fluent Light Theme)**:
  * 눈이 편안한 밝고 현대적인 Off-White 레이아웃과 고대비 다크-차콜 텍스트로 **극대화된 가독성**을 선사합니다.
  * 트리 뷰와 이미지 영역의 경계선(`QSplitter`)에 마우스를 대면 세련된 파란색으로 밝아지며, 드래그 핸들 그립 디자인이 적용되어 드래그 조작이 매우 직관적입니다.
* **🚀 드롭다운 탐색 및 더블 클릭 실행**:
  * Windows 탐색기 등에서 폴더를 드래그 앤 드롭하여 바로 스캔 경로로 입력할 수 있으며, 썸네일 더블 클릭 시 Windows 기본 사진 뷰어로 해당 파일이 안전하게 열립니다.

---

## 🛠️ 기술 스택 (Tech Stack)

* **언어**: Python 3.13+
* **GUI 라이브러리**: PyQt6 (v6.11.0+)
* **컴파일러**: PyInstaller (v6.20.0+)
* **아키텍처**: Multi-Threaded Task Queue with `QRunnable` & Custom `FlowLayout`

---

## 📂 파일 구조 (File Structure)

* [main.py](main.py): 애플리케이션의 메인 윈도우, 컨트롤 바, 폴더 트리 뷰 및 핵심 비동기 통합 흐름 제어.
* [thumbnail_widget.py](thumbnail_widget.py): 멀티스레드 기반 디코더(`ThumbnailLoaderRunnable`), 썸네일 카드, 폴더별 묶음 컨테이너.
* [flow_layout.py](flow_layout.py): 너비에 반응하여 자동 래핑 및 리플로우를 수행하는 반응형 Flow Layout 클래스.
* [styles.py](styles.py): 라이트 테마 정의, SVG 벡터 에셋 및 전역 CSS 스타일시트.
* [implementation_plan.md](implementation_plan.md): 초기 시스템 아키텍처 및 상세 개발 임플리멘테이션 기획 플랜.
* [walkthrough.md](walkthrough.md): 최종 기능 테스트 내역 및 가이드 문서.

---

## 🚀 빠른 시작 (Quick Start)

### 1. 로컬 가상 환경 구축 및 직접 실행 (Python 실행)
소스 코드가 있는 프로젝트 폴더로 이동한 뒤, 아래 명령어를 실행하여 즉시 빌드 및 실행할 수 있습니다.

```powershell
# 1. 프로젝트 폴더로 이동
cd D:\Antigravity\PhotoViewer

# 2. 가상 환경 활성화 (PowerShell)
.venv\Scripts\Activate.ps1

# 3. 애플리케이션 가동
python main.py
```

### 2. 컴파일 없이 즉시 사용할 수 있는 바이너리 구동 (EXE 실행)
미리 빌드해 둔 포터블 실행 파일을 이용해 파이썬 없이 바로 구동할 수 있습니다.
* **실행 경로**: `D:\Antigravity\PhotoViewer\dist\main.exe`를 더블 클릭하여 실행합니다.

---

## 📦 독립 실행형 EXE 파일 직접 빌드 방법
필요 시 직접 새로운 단독 `.exe` 파일을 재구성할 수 있습니다.

```powershell
# 가상 환경이 활성화된 상태에서 PyInstaller 컴파일 실행
pyinstaller --noconsole --onefile main.py
```
* 완료되면 `dist/` 폴더 내에 단일 `main.exe` 파일이 생성됩니다.

---

## 🤝 기여 안내
버그 리포트, 제안 사항 또는 풀 리퀘스트(PR)는 언제든 환영합니다!
더 나은 고성능 이미지 탐색 경험을 위해 아이디어가 있다면 편하게 컨트리뷰션에 참여해 주세요.
