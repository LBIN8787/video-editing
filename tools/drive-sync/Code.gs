/**
 * ytflow → Google Drive 자동 복사 (키·토큰 없이, 내 구글 계정 안에서 실행되는 Apps Script)
 *
 * 하는 일: 15분마다 GitHub 저장소(공개)의 릴리스 'video-<프로젝트>' 를 확인해서
 *          새 영상·자막·업로드 문구를 Drive 의 채널 폴더 / <프로젝트> 폴더로 복사한다.
 * 설치(한 번): docs/12-drive-sync.md
 *   1) script.google.com → 새 프로젝트 → 이 파일 내용을 Code.gs 에 붙여넣기
 *   2) 프로젝트 설정 → 'appsscript.json 매니페스트 파일 표시' → tools/drive-sync/appsscript.json 내용 붙여넣기
 *   3) 함수 'setup' 선택 → 실행 → 권한 허용 (내 Drive 에 파일 만들기, 외부 주소 읽기)
 *   이후 자동. 바로 돌리려면 'syncReleases' 실행.
 * 큰 파일: Apps Script 는 한 번에 50MB 까지만 받으므로 16MB 씩 나눠 받아(Range) Drive 이어 올리기로 붙인다.
 */
const REPO = 'LBIN8787/video-editing';
const ROOT_FOLDER_ID = '16Y2oMXY7Ze_4yQP3Omlqll9rUwWPJvnu';       // 'ytflow 영상'
const CHANNEL_FOLDERS = {                                           // config/storage.yaml 과 같게
  'ch-paper-column': '10W0Ws3bDEwJLL7x7hOd0_-TymUejpLjZ',
  'ch-source-brief': '1S-A_IcVh1SHFqhoLwDAN3cJrgTUfbxhK',
  'ch-data-motion': '1sJrI9mYFemlw2-niEKtyhxTmHk2vTp69',
  'ch-ai-shorts': '1f0SYDO5VMUdpfll-FgnbjSbxevGSMP2i',
  'ch-money-shorts': '18xCQtSz0SqYdej60pp-GN-TwotnVxnLh',
};
const NEW_CHANNEL_PARENT = ROOT_FOLDER_ID;                          // 목록에 없는 채널(예: ch-knowledge)은 root 아래 새 폴더
const CHUNK = 16 * 1024 * 1024;                                     // 256KB 의 배수
const EXTS = ['.mp4', '.srt', '.ass', '.txt', '.md', '.zip'];

function setup() {
  ScriptApp.getProjectTriggers().forEach(t => ScriptApp.deleteTrigger(t));
  ScriptApp.newTrigger('syncReleases').timeBased().everyMinutes(15).create();
  syncReleases();
}

function syncReleases() {
  const lock = LockService.getScriptLock();
  if (!lock.tryLock(1000)) return;
  try {
    const props = PropertiesService.getScriptProperties();
    const res = UrlFetchApp.fetch('https://api.github.com/repos/' + REPO + '/releases?per_page=30',
      { headers: { Accept: 'application/vnd.github+json' }, muteHttpExceptions: true });
    if (res.getResponseCode() !== 200) { console.log('GitHub ' + res.getResponseCode()); return; }
    const started = Date.now();
    for (const rel of JSON.parse(res.getContentText())) {
      if (!rel.tag_name.startsWith('video-')) continue;
      const project = rel.tag_name.slice(6);
      const m = (rel.body || '').match(/채널: `([^`]*)`/);
      const folder = projectFolder_(m ? m[1] : '', project);
      for (const a of rel.assets) {
        if (!EXTS.some(e => a.name.endsWith(e))) continue;
        const key = 'a' + a.id + '@' + a.updated_at;
        if (props.getProperty(key)) continue;
        if (Date.now() - started > 4 * 60 * 1000) return;           // 실행 시간 6분 제한 → 나머지는 다음 회차
        const name = project.slice(0, 8) + ' ' + (a.name === 'final.mp4' ? project.slice(9) + '.mp4' : a.name);
        const old = folder.getFilesByName(name);                    // 같은 이름(이전 판)은 휴지통으로
        while (old.hasNext()) old.next().setTrashed(true);
        copyAsset_(a, folder.getId(), name);
        props.setProperty(key, new Date().toISOString());
        console.log('복사: ' + project + ' / ' + name + ' (' + Math.round(a.size / 1e6) + 'MB)');
      }
    }
  } finally {
    lock.releaseLock();
  }
}

function projectFolder_(channel, project) {
  let parent;
  if (CHANNEL_FOLDERS[channel]) parent = DriveApp.getFolderById(CHANNEL_FOLDERS[channel]);
  else {
    const root = DriveApp.getFolderById(NEW_CHANNEL_PARENT);
    const name = channel || '기타';
    const it = root.getFoldersByName(name);
    parent = it.hasNext() ? it.next() : root.createFolder(name);
  }
  const it2 = parent.getFoldersByName(project);
  return it2.hasNext() ? it2.next() : parent.createFolder(project);
}

function copyAsset_(a, folderId, name) {
  if (a.size <= 45 * 1024 * 1024) {
    const blob = UrlFetchApp.fetch(a.browser_download_url).getBlob().setName(name);
    DriveApp.getFolderById(folderId).createFile(blob);
    return;
  }
  // 큰 파일: Drive 이어 올리기(resumable) 세션 + GitHub 에서 16MB 씩 Range 로 받기
  const token = ScriptApp.getOAuthToken();
  const init = UrlFetchApp.fetch('https://www.googleapis.com/upload/drive/v3/files?uploadType=resumable', {
    method: 'post', contentType: 'application/json; charset=UTF-8',
    headers: { Authorization: 'Bearer ' + token, 'X-Upload-Content-Type': a.content_type || 'video/mp4',
               'X-Upload-Content-Length': String(a.size) },
    payload: JSON.stringify({ name: name, parents: [folderId] }),
  });
  const session = init.getHeaders()['Location'] || init.getHeaders()['location'];
  const src = UrlFetchApp.fetch(a.browser_download_url, { followRedirects: false }).getHeaders()['Location'];
  for (let start = 0; start < a.size; start += CHUNK) {
    const end = Math.min(start + CHUNK, a.size) - 1;
    const part = UrlFetchApp.fetch(src, { headers: { Range: 'bytes=' + start + '-' + end } }).getBlob().getBytes();
    const r = UrlFetchApp.fetch(session, {
      method: 'put', contentType: a.content_type || 'video/mp4', payload: part, muteHttpExceptions: true,
      headers: { 'Content-Range': 'bytes ' + start + '-' + end + '/' + a.size },
    });
    const code = r.getResponseCode();
    if (code !== 308 && code !== 200 && code !== 201) throw new Error('Drive 업로드 실패 ' + code + ' ' + r.getContentText());
  }
}
