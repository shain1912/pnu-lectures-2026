// 10주차 스타터 — 게임 흐름 상태 기계 + 액션 맵 전환
// Unity 6 · Input System 패키지
//
// 준비
//  1) Project Settings → Player → Active Input Handling = Input System Package (New)
//  2) 프로젝트의 InputSystem_Actions 에셋 열기
//     - Player 맵에 Button 타입 액션 "Pause" 추가 → 바인딩 : Keyboard Escape · Gamepad Start
//       (Quest 컨트롤러 메뉴 버튼 바인딩은 11주차에 추가)
//     - UI 맵의 "Cancel" 액션은 템플릿에 이미 존재 (Escape 포함)
//  3) 빈 오브젝트 "GameState" 에 이 스크립트 부착 → actions · pause · resume · menuPanel 지정
//
// 왜 Pause 와 Resume 을 다른 맵에 두는가
//  일시정지 중에는 Player 맵이 꺼짐 → Player/Pause 로는 되돌아올 수 없음
//  → 되돌아오는 입력은 켜져 있는 UI 맵(Cancel) 이 담당

using System;
using UnityEngine;
using UnityEngine.InputSystem;

public enum GameState { Menu, Playing, Paused }

public class GameStateMachine : MonoBehaviour
{
    [Header("입력")]
    [SerializeField] InputActionAsset actions;           // InputSystem_Actions
    [SerializeField] InputActionReference pause;         // Player/Pause
    [SerializeField] InputActionReference resume;        // UI/Cancel

    [Header("UI")]
    [SerializeField] GameObject menuPanel;               // 메뉴 캔버스(또는 패널)

    [SerializeField] GameState initialState = GameState.Playing;

    public GameState State { get; private set; }
    public event Action<GameState> StateChanged;         // UI · 소리 · 진동이 구독

    InputActionMap playerMap, uiMap;

    void Awake()
    {
        playerMap = actions.FindActionMap("Player", throwIfNotFound: true);
        uiMap     = actions.FindActionMap("UI",     throwIfNotFound: true);
    }

    // 구독은 OnEnable · 해제는 OnDisable — 항상 한 쌍
    void OnEnable()
    {
        pause.action.performed  += OnPause;
        resume.action.performed += OnResume;
    }
    void OnDisable()
    {
        pause.action.performed  -= OnPause;
        resume.action.performed -= OnResume;
    }

    void Start() => Apply(initialState);

    void OnPause(InputAction.CallbackContext _)  { if (State == GameState.Playing) SetState(GameState.Paused); }
    void OnResume(InputAction.CallbackContext _) { if (State == GameState.Paused)  SetState(GameState.Playing); }

    // 버튼 onClick 에서도 호출 (예 : 메뉴의 «계속» 버튼 → SetPlaying)
    public void SetPlaying() => SetState(GameState.Playing);
    public void SetPaused()  => SetState(GameState.Paused);
    public void SetMenu()    => SetState(GameState.Menu);

    public void SetState(GameState next)
    {
        if (next == State) return;
        Apply(next);
    }

    // 상태 전환 = 이 함수 한 곳 — 맵 전환 · 패널 표시 · 시간 정지
    void Apply(GameState next)
    {
        State = next;
        bool ui = next != GameState.Playing;

        playerMap.Disable();
        uiMap.Disable();
        (ui ? uiMap : playerMap).Enable();

        if (menuPanel) menuPanel.SetActive(ui);
        Time.timeScale = next == GameState.Paused ? 0f : 1f;   // VR : 머리 트래킹은 timeScale 과 무관하게 계속됨

        Debug.Log($"[GameState] → {next} · 켜진 맵 = {(ui ? "UI" : "Player")}");
        StateChanged?.Invoke(next);
    }
}
