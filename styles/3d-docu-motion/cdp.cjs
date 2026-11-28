'use strict';
const fs = require('node:fs');
const path = require('node:path');
const {spawn} = require('node:child_process');
const wait = ms => new Promise(r => setTimeout(r, ms));

async function launch(browser, profile, width, height) {
  fs.mkdirSync(profile);
  const stamp = path.join(profile, 'DevToolsActivePort');
  const chrome = spawn(browser, [
    '--headless=new','--remote-debugging-port=0','--remote-debugging-address=127.0.0.1',
    '--user-data-dir=' + profile,'--no-first-run','--no-default-browser-check',
    '--disable-background-networking','--disable-component-update','--disable-sync',
    '--disable-features=MediaRouter,OptimizationHints','--disable-domain-reliability',
    '--host-resolver-rules=MAP * ~NOTFOUND, EXCLUDE 127.0.0.1','--no-proxy-server',
    '--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader',
    '--hide-scrollbars','about:blank'
  ], {windowsHide:true, stdio:['ignore','ignore','ignore']});
  let launchError, ws;
  chrome.on('error', e => { launchError = e; });
  try {
    let target;
    for (let i=0; i<160; i++) {
      if (launchError) throw launchError;
      if (chrome.exitCode !== null) throw Error('Chromium exited: ' + chrome.exitCode);
      try {
        const port = fs.readFileSync(stamp,'utf8').split(/\r?\n/)[0];
        if (!/^\d+$/.test(port)) throw Error('Waiting for local CDP port');
        const resp = await fetch('http://127.0.0.1:' + port + '/json/list', {signal:AbortSignal.timeout(750)});
        target = (await resp.json()).find(x => x.type === 'page');
        if (target) break;
      } catch {}
      await wait(125);
    }
    if (!target) throw Error('Chromium loopback CDP unavailable');
    const url = new URL(target.webSocketDebuggerUrl);
    if (url.protocol !== 'ws:' || url.hostname !== '127.0.0.1') throw Error('Expected loopback-only CDP');
    ws = new WebSocket(url);
    await new Promise((resolve,reject) => {
      const timer = setTimeout(() => reject(Error('CDP handshake timeout')), 5000);
      ws.addEventListener('open', () => {clearTimeout(timer); resolve();}, {once:true});
      ws.addEventListener('error', () => {clearTimeout(timer); reject(Error('CDP handshake failed'));}, {once:true});
    });
    let id = 0;
    const waiting = new Map();
    ws.addEventListener('message', e => {
      const m = JSON.parse(e.data);
      const p = waiting.get(m.id);
      if (!p) return;
      clearTimeout(p.timer);
      waiting.delete(m.id);
      if (m.error) p.reject(Error(JSON.stringify(m.error))); else p.resolve(m.result);
    });
    ws.addEventListener('close', () => {
      for (const p of waiting.values()) { clearTimeout(p.timer); p.reject(Error('CDP closed')); }
      waiting.clear();
    });
    function call(method, params={}) {
      return new Promise((resolve,reject) => {
        if (ws.readyState !== WebSocket.OPEN) return reject(Error('CDP is not open'));
        const request = ++id;
        const timer = setTimeout(() => { waiting.delete(request); reject(Error('CDP timeout: ' + method)); }, 15000);
        waiting.set(request,{resolve,reject,timer});
        ws.send(JSON.stringify({id:request,method,params}));
      });
    }
    await call('Emulation.setDeviceMetricsOverride',{width,height,deviceScaleFactor:1,mobile:false});
    await call('Network.enable');
    await call('Network.setBlockedURLs',{urls:['http://*','https://*','ws://*','wss://*']});
    return {call, async evaluate(expression) {
      const m = await call('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true,userGesture:true});
      if (m.exceptionDetails) throw Error(m.exceptionDetails.exception?.description || JSON.stringify(m.exceptionDetails));
      return m.result.value;
    }, close() { ws.close(); chrome.kill(); }};
  } catch (e) { if (ws) ws.close(); chrome.kill(); throw e; }
}
module.exports = {launch,wait};
