import requests
from rich.console import Console
from rich.table import Table
import re  # 정규표현식 사용 모듈

# 서버 주소 설정
SERVER_URL = "http://[::1]:8000"

console = Console()

def get_model_list():
    """
    서버의 /v2/repository/index 엔드포인트에 POST 요청하여 모델 리스트를 가져온다.
    """
    try:
        response = requests.post(f"{SERVER_URL}/v2/repository/index")
        response.raise_for_status()
        models = response.json()
        return models
    except Exception as e:
        console.print(f"[red]모델 목록을 가져오는 중 오류 발생: {e}[/red]")
        return []
    
def natural_sort_key(s):
    """문자열을 자연스러운 순서로 정렬하기 위한 키 함수"""
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

def display_model_table(models: list, mode="full"):
    """
    전체 모델 리스트를 rich의 Table 형식으로 출력한다.
    
    mode:
      - "full": 전체 정보(No, Model Name, Version, State, Reason)를 출력.
      - "toggle": 상세 정보를 출력하며 마지막 행에 '돌아가기' 옵션을 추가.
    
    모델의 state가 READY가 아니면 'UNAVAILABLE'로 표시.
    """
    models = sorted(models, key=lambda item: natural_sort_key(item['name']))

    table_title = "전체 모델 리스트" if mode == "full" else "모델 로드/언로드 (토글) - 모델 리스트"
    table = Table(title=table_title)
    table.add_column("No", style="cyan", no_wrap=True)
    table.add_column("Model Name", style="magenta")
    table.add_column("Version", style="cyan")
    table.add_column("State", style="green")
    table.add_column("Reason", style="magenta")
    
    for idx, model in enumerate(models, start=1):
        name = model.get("name", "-")
        version = model.get("version", "-")
        state = model.get("state", "-")
        reason = model.get("reason", "-")
        if state != "READY":
            state = "UNAVAILABLE"
        table.add_row(str(idx), name, version, state, reason)
        
    if mode == "toggle":
        # 토글 모드에서는 마지막 행에 '돌아가기' 옵션 추가
        table.add_row("0", "[bold]돌아가기[/bold]", "", "", "")
        
    console.print(table)

def toggle_model(model):
    """
    선택한 모델의 상태에 따라 load 또는 unload 명령을 실행한다.
    - 상태가 READY이면 unload, 아닌 경우에는 load를 수행.
    """
    name = model.get("name")
    state = model.get("state", "UNAVAILABLE")
    
    if state == "READY":
        action = "unload"
        message = f"모델 {name}을(를) unload 합니다..."
    else:
        action = "load"
        message = f"모델 {name}을(를) load 합니다..."
        
    console.print(f"[yellow]{message}[/yellow]")
    try:
        response = requests.post(f"{SERVER_URL}/v2/repository/models/{name}/{action}")
        response.raise_for_status()
        console.print(f"[green]모델 {name}에 대해 {action} 명령이 성공적으로 실행되었습니다.[/green]")
    except Exception as e:
        console.print(f"[red]모델 {name}에 {action} 명령 실행 중 오류 발생: {e}[/red]")

def main():
    while True:
        console.print("[blue]--------------------------------------[/blue]")
        console.print("[blue]메인 메뉴를 선택하세요:[/blue]")
        console.print("[blue]1. 전체 모델 리스트 출력[/blue]")
        console.print("[blue]2. 모델 로드/언로드 (단일 토글)[/blue]")
        console.print("[blue]3. 멀티 모델 로드/언로드[/blue]")
        console.print("[blue]q. 종료[/blue]")
        main_choice = input("입력: ").strip()

        if main_choice == "1":
            models = get_model_list()
            display_model_table(models, mode="full")
            
        elif main_choice == "2":
            # 단일 토글 메뉴: 0번 입력 시 메인 메뉴 복귀
            while True:
                models = get_model_list()
                display_model_table(models, mode="toggle")
                
                choice = input("모델 선택 (번호): ").strip()
                if choice == "0":
                    break
                try:
                    idx = int(choice)
                    if 1 <= idx <= len(models):
                        # 정렬된 리스트 순서를 따름
                        # display_model_table 내부에서 정렬되지만, 여기서도 동일한 순서를 유지하기 위해 다시 정렬
                        models = sorted(models, key=lambda item: natural_sort_key(item['name']))
                        selected_model = models[idx - 1]
                        toggle_model(selected_model)
                    else:
                        console.print("[red]잘못된 모델 번호입니다.[/red]")
                except ValueError:
                    console.print("[red]숫자 값을 입력해 주세요.[/red]")

        elif main_choice == "3":
            # 멀티 모델 로드/언로드 기능
            while True:
                models = get_model_list()
                # 정렬된 리스트 확보
                models = sorted(models, key=lambda item: natural_sort_key(item['name']))
                display_model_table(models, mode="toggle")
                
                multi_choice = input("모델 선택 (번호 또는 범위; 예: 1-10): ").strip()
                if multi_choice == "0":
                    break
                # 정규표현식을 사용하여 입력값에서 두 개의 숫자 추출
                numbers = re.findall(r'\d+', multi_choice)
                if len(numbers) == 2:
                    start = int(numbers[0])
                    end = int(numbers[1])
                    if start < 1 or end > len(models) or start > end:
                        console.print("[red]올바른 범위를 입력해주세요.[/red]")
                        continue
                    for idx in range(start, end + 1):
                        selected_model = models[idx - 1]
                        toggle_model(selected_model)
                else:
                    console.print("[red]2개의 숫자(시작 인덱스, 종료 인덱스)를 입력해주세요.[/red]")
                    
        elif main_choice.lower() == "q":
            console.print("[yellow]스크립트를 종료합니다.[/yellow]")
            break
        else:
            console.print("[red]잘못된 옵션입니다. 다시 선택하세요.[/red]")

if __name__ == "__main__":
    main()