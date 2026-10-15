// 10주차 스타터 — 메뉴 패널 UI (이벤트 구독 · 해제 짝 검증용)
// 메뉴 패널 오브젝트에 부착 · 같은 스크립트를 Overlay 버전과 World Space 버전에서 그대로 사용
//
// 검증 조건 (워크북 실습 5)
//  패널을 5회 껐다 켠 뒤 «계속» 버튼 1회 클릭 → 콘솔 «클릭 콜백 1회» 가 정확히 1번
//  OnDisable 의 RemoveListener 를 지우고 다시 하면 → 여러 번 찍힘 = 구독 해제 누락 재현

using UnityEngine;
using UnityEngine.UI;
using TMPro;

public class PauseMenuUI : MonoBehaviour
{
    [SerializeField] GameStateMachine game;
    [SerializeField] Button resumeButton;
    [SerializeField] Button quitButton;
    [SerializeField] TMP_Text stateLabel;
    [SerializeField] TMP_Text scoreLabel;

    int score = 1240;
    int clickCount;   // 이번 클릭에서 콜백이 몇 번 불렸는지 확인용

    void OnEnable()
    {
        resumeButton.onClick.AddListener(OnResumeClicked);
        quitButton.onClick.AddListener(OnQuitClicked);
        if (game) game.StateChanged += OnStateChanged;
        Refresh(game ? game.State : GameState.Paused);
    }

    void OnDisable()
    {
        resumeButton.onClick.RemoveListener(OnResumeClicked);
        quitButton.onClick.RemoveListener(OnQuitClicked);
        if (game) game.StateChanged -= OnStateChanged;
    }

    void OnResumeClicked()
    {
        clickCount++;
        Debug.Log($"[Menu] 클릭 콜백 {clickCount}회");
        game.SetPlaying();
    }

    void OnQuitClicked() => game.SetMenu();

    void OnStateChanged(GameState s) => Refresh(s);

    void LateUpdate() => clickCount = 0;   // 프레임마다 초기화 → 한 번 클릭에 몇 번 불렸는지만 남음

    void Refresh(GameState s)
    {
        if (stateLabel) stateLabel.text = s == GameState.Paused ? "일시정지 상태" : s.ToString();
        if (scoreLabel) scoreLabel.text = $"점수  {score:N0}";
    }
}
