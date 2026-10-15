// ============================================================
// 12주차 스타터 · 움직임·프레임 기록기
// 컴퓨터그래픽스 VF3500076 · 조성호
//
// 리그(XR Origin) 의 움직임을 매 프레임 기록 → 체감 대신 «숫자» 로 비교
//   speed   : 리그 속도 (m/s)
//   accel   : 가속도 크기 (m/s²) = |이번 속도 − 지난 속도| ÷ deltaTime
//   yawRate : 좌우 회전 속도 (°/s)
//   frameMs : 프레임타임 (ms) — 90 Hz 기준 11.1 ms
//
// 세션 요약 (Console · logcat · CSV 마지막 줄)
//   최대 가속도 · 0.7 m/s² 초과 프레임 수 (전방 가속 임계 평균, Terenzi & Zaal 2020)
//   연속 회전 시간 (1~400 °/s 구간 · 스냅 턴의 순간 회전은 별도 집계)
//   순간 이동 횟수 (한 프레임 속도 20 m/s 초과 = 텔레포트·스냅)
//   11.1 ms 초과 프레임 수
//
// CSV 위치 : Application.persistentDataPath
//   Quest → /sdcard/Android/data/<패키지 이름>/files/  (Developer Hub 파일 탐색 또는 adb pull)
// ============================================================
using System.IO;
using System.Text;
using UnityEngine;

public class MotionLogger : MonoBehaviour
{
    public Transform rig;
    [Tooltip("CSV 파일 저장")] public bool writeCsv = true;
    [Tooltip("가속 임계 (m/s²)")] public float accelThreshold = 0.7f;
    [Tooltip("프레임 예산 (ms)")] public float frameBudgetMs = 11.1f;

    string label = "session";
    StringBuilder sb;
    Vector3 lastPos, lastVel; float lastYaw;
    bool primed;
    float t, maxAcc, contTurnTime, maxContYaw;
    int frames, accFrames, overBudget, jumps, snaps;

    void Awake() { if (rig == null) rig = transform; }

    void Start() { if (sb == null) BeginSession(label); }

    /// <summary>새 세션 시작 — 이전 세션은 요약·저장</summary>
    public void BeginSession(string name)
    {
        if (sb != null && frames > 0) EndSession();
        label = name;
        sb = new StringBuilder("time,speed,accel,yawRate,frameMs\n");
        primed = false;
        t = maxAcc = contTurnTime = maxContYaw = 0f;
        frames = accFrames = overBudget = jumps = snaps = 0;
    }

    void LateUpdate()
    {
        if (sb == null) return;
        float dt = Time.deltaTime;
        if (dt <= 0f) return;
        Vector3 pos = rig.position; float yaw = rig.eulerAngles.y;
        if (!primed) { lastPos = pos; lastYaw = yaw; lastVel = Vector3.zero; primed = true; return; }

        Vector3 vel = (pos - lastPos) / dt;
        float speed = vel.magnitude;
        float acc = (vel - lastVel).magnitude / dt;
        float yawRate = Mathf.DeltaAngle(lastYaw, yaw) / dt;
        float frameMs = Time.unscaledDeltaTime * 1000f;

        t += dt; frames++;
        bool jump = speed > 20f;                       // 텔레포트 프레임
        float absYaw = Mathf.Abs(yawRate);
        bool snap = absYaw > 400f;                     // 스냅 턴 프레임
        if (jump) jumps++;
        if (snap) snaps++;
        // 순간 이동·스냅 직후 프레임의 거대한 가속도는 «한 프레임 충돌» 로 따로 셈
        if (!jump && !snap && speed <= 20f)
        {
            maxAcc = Mathf.Max(maxAcc, acc);
            if (acc > accelThreshold) accFrames++;
        }
        if (absYaw >= 1f && absYaw <= 400f) { contTurnTime += dt; maxContYaw = Mathf.Max(maxContYaw, absYaw); }
        if (frameMs > frameBudgetMs) overBudget++;

        if (writeCsv) sb.Append($"{t:F3},{speed:F3},{acc:F3},{yawRate:F2},{frameMs:F2}\n");
        lastPos = pos; lastVel = jump ? Vector3.zero : vel; lastYaw = yaw;
    }

    void OnDisable() { EndSession(); }
    void OnApplicationPause(bool paused) { if (paused) EndSession(); }

    void EndSession()
    {
        if (sb == null || frames == 0) return;
        string summary =
            $"[{label}] 시간 {t:F1}s · 최대 가속 {maxAcc:F2} m/s² · 가속 {accelThreshold} 초과 {accFrames}프레임 · " +
            $"연속 회전 {contTurnTime:F1}s (최대 {maxContYaw:F0}°/s) · 순간 이동 {jumps}회 · 스냅 {snaps}회 · " +
            $"{frameBudgetMs} ms 초과 {overBudget}/{frames}프레임";
        Debug.Log("[MotionLogger] " + summary);
        if (writeCsv)
        {
            sb.Append("# ").Append(summary).Append('\n');
            string path = Path.Combine(Application.persistentDataPath,
                $"motion_{label}_{System.DateTime.Now:MMdd_HHmmss}.csv");
            try { File.WriteAllText(path, sb.ToString(), Encoding.UTF8); Debug.Log("[MotionLogger] 저장 " + path); }
            catch (System.Exception e) { Debug.LogWarning("[MotionLogger] 저장 실패 " + e.Message); }
        }
        frames = 0;
    }
}
