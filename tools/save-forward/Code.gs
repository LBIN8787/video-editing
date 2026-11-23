/**
 * SAVE(오선) 알림 → GitHub inbox/save/<YYYYMMDD>.md 자동 기록 (메모 없이, 2026-11-14 사용자 요청)
 *
 * ⚠️ 지금은 켜지 않습니다 — 참고·백업용. 2026-11-14 부터는 MacroDroid → Gmail `[save알림]` →
 *    Pickle 30분 Gmail 감시가 같은 파일을 채웁니다 (docs/28 §1). 둘 다 켜면 같은 알림이 두 줄로 쌓입니다.
 *    이 스크립트를 쓰려면 30분 감시를 먼저 멈추세요.
 *
 * 흐름: 휴대폰의 SAVE 앱 푸시 알림 → 알림 전달 앱(Notifly·Message487·Tasker 등, SAVE 앱만 선택)이 Gmail 로 보냄
 *       → Gmail 필터가 라벨 'SAVE알림' 을 붙임 → 이 스크립트가 10분마다 새 메일을 읽어 저장소의 그날 파일에 한 줄씩 덧붙임
 *       → 아침 자동 제작(06:05)의 `python -m ytflow daily` 가 01_research/save_check.md 표로 옮김 (manual/09 §3-0)
 * SAVE 웹을 긁지 않습니다 (봇 확인·AI 수집 거부 — 우회 금지). 내 휴대폰에 온 내 알림만 씁니다.
 *
 * 설치(30분 감시를 멈출 때만, docs/28-save-and-imagegen.md §1):
 *   1) script.google.com → 새 프로젝트 → 이 내용을 Code.gs 에 붙여넣기
 *   2) 프로젝트 설정 → 스크립트 속성: GH_TOKEN = GitHub 세분화 토큰(저장소 LBIN8787/video-editing, Contents: Read and write 만)
 *      (토큰은 채팅에 쓰지 않기)
 *   3) 함수 'setup' 실행 → 권한 허용(Gmail 읽기·라벨, 외부 주소 호출)
 */
const REPO = 'LBIN8787/video-editing';
const LABEL = 'SAVE알림';          // Gmail 필터가 붙이는 라벨 (알림 전달 앱의 제목·보낸이로 필터)
const DONE = 'SAVE알림/기록됨';
const BRANCH = 'main';

function setup() {
  ScriptApp.getProjectTriggers().forEach(t => ScriptApp.deleteTrigger(t));
  ScriptApp.newTrigger('forwardSave').timeBased().everyMinutes(10).create();
  GmailApp.getUserLabelByName(LABEL) || GmailApp.createLabel(LABEL);
  GmailApp.getUserLabelByName(DONE) || GmailApp.createLabel(DONE);
  forwardSave();
}

function kstDay_(d) {   // 영상 날짜: 한국 시간 06:00 이후 알림은 다음 날 아침 영상 몫
  const k = new Date(d.getTime() + 9 * 3600 * 1000);
  if (k.getUTCHours() >= 6) k.setUTCDate(k.getUTCDate() + 1);
  return Utilities.formatDate(k, 'UTC', 'yyyyMMdd');
}

function forwardSave() {
  const token = PropertiesService.getScriptProperties().getProperty('GH_TOKEN');
  if (!token) throw new Error('스크립트 속성 GH_TOKEN 없음');
  const done = GmailApp.getUserLabelByName(DONE);
  const threads = GmailApp.search(`label:${LABEL} -label:${DONE.replace('/', '-')}`, 0, 50);
  const byDay = {};
  threads.forEach(th => th.getMessages().forEach(m => {
    const text = (m.getSubject() + ' ' + m.getPlainBody()).replace(/\s+/g, ' ').trim().slice(0, 300);
    if (!text) return;
    const day = kstDay_(m.getDate());
    const hm = Utilities.formatDate(m.getDate(), 'Asia/Seoul', 'MM-dd HH:mm');
    (byDay[day] = byDay[day] || []).push(`${text} (알림 ${hm})`);
  }));
  Object.keys(byDay).forEach(day => appendFile_(token, `inbox/save/${day}.md`, byDay[day]));
  threads.forEach(th => th.addLabel(done));
}

function appendFile_(token, path, lines) {
  const url = `https://api.github.com/repos/${REPO}/contents/${encodeURIComponent(path).replace(/%2F/g, '/')}`;
  const h = { Authorization: 'Bearer ' + token, Accept: 'application/vnd.github+json' };
  let sha = null, body = '';
  const r = UrlFetchApp.fetch(url + '?ref=' + BRANCH, { headers: h, muteHttpExceptions: true });
  if (r.getResponseCode() === 200) {
    const j = JSON.parse(r.getContentText());
    sha = j.sha;
    body = Utilities.newBlob(Utilities.base64Decode(j.content.replace(/\n/g, ''))).getDataAsString('UTF-8');
  }
  body += lines.map(l => '- ' + l).join('\n') + '\n';
  const payload = { message: `SAVE 알림 ${lines.length}건 → ${path}`, content: Utilities.base64Encode(body, Utilities.Charset.UTF_8), branch: BRANCH };
  if (sha) payload.sha = sha;
  UrlFetchApp.fetch(url, { method: 'put', headers: h, contentType: 'application/json', payload: JSON.stringify(payload) });
}
