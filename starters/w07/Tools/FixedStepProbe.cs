// ============================================================
// 7주차 · 측정 도구 — 화면 프레임마다 물리 스텝이 몇 번 돌았나
// 컴퓨터그래픽스 VF3500076 · 조성호
//
// 출력 예 : "프레임당 물리 스텝 : 010101011010..."
//   - 0 과 1 이 섞여 나오면 → 화면 주기와 물리 주기가 엇갈림 → 움직이는 물체가 덜컥거림(judder)
//   - 해결 ① Rigidbody Interpolate = Interpolate   ② Fixed Timestep 을 화면 주기에 맞춤 (90Hz → 0.0111)
//   - 2 이상이 자주 보이면 → 프레임이 무거워 물리가 몰아서 돌고 있음
//
// 사용법 : 아무 GameObject 에 붙이고 Play → Console 확인
// ============================================================
using System.Text;
using UnityEngine;

public class FixedStepProbe : MonoBehaviour
{
    public int framesPerLog = 60;

    int stepsThisFrame;
    readonly StringBuilder pattern = new StringBuilder();

    void FixedUpdate()
    {
        stepsThisFrame++;           // FixedUpdate 는 같은 프레임의 Update 보다 먼저 실행
    }

    void Update()
    {
        pattern.Append(Mathf.Min(stepsThisFrame, 9));
        stepsThisFrame = 0;

        if (pattern.Length >= framesPerLog)
        {
            Debug.Log($"[FixedStepProbe] 화면 약 {1f / Time.unscaledDeltaTime:F0} fps · " +
                      $"물리 {1f / Time.fixedDeltaTime:F0} Hz · 프레임당 물리 스텝 : {pattern}");
            pattern.Clear();
        }
    }
}
