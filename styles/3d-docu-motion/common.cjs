'use strict';
const fs = require('node:fs');
const path = require('node:path');
const {spawnSync} = require('node:child_process');
const {pipeline} = require('node:stream/promises');
const {createHash} = require('node:crypto');

function args(values, allowed, required) {
  if (values.length % 2) throw Error('Expected --key value pairs; see README.ko.md');
  const out = Object.create(null);
  for (let i = 0; i < values.length; i += 2) {
    const key = values[i].slice(2), value = values[i + 1];
    if (!values[i].startsWith('--') || !allowed.includes(key) || key in out || !value || value.startsWith('--')) {
      throw Error('Invalid or duplicate option: ' + values[i]);
    }
    out[key] = value;
  }
  for (const key of required) if (!out[key]) throw Error('Required option: --' + key);
  return out;
}
function file(value) {
  const resolved = path.resolve(value);
  if (!fs.statSync(resolved).isFile()) throw Error('Not a regular file: ' + resolved);
  return resolved;
}
function tool(value, fallback) { return value ? file(value) : fallback; }
function outDir(value) {
  const resolved = path.resolve(value);
  fs.mkdirSync(resolved); // Deliberately reject existing directories. Create the parent separately.
  return resolved;
}
function run(bin, argv, capture = false) {
  const result = spawnSync(bin, argv, {encoding: 'utf8', windowsHide: true, stdio: capture ? ['ignore', 'pipe', 'inherit'] : 'inherit'});
  if (result.error) throw result.error;
  if (result.status !== 0) throw Error(bin + ' failed: ' + (result.status ?? result.signal));
  return result.stdout;
}
function probe(bin, name) {
  return JSON.parse(run(bin, ['-v','error','-show_format','-show_streams','-of','json',name], true));
}
async function sha(name) {
  const digest = createHash('sha256');
  await pipeline(fs.createReadStream(name), digest);
  return digest.digest('hex');
}
function load(value) {
  const cfg = JSON.parse(fs.readFileSync(value ? file(value) : path.join(__dirname,'optics-recipe.v0.1.json'), 'utf8'));
  if (cfg.schemaVersion !== '1.0.0' || cfg.id !== '20261128-market-deep-optics-v2-v4-v5') {
    throw Error('Unsupported optics recipe or schema');
  }
  return cfg;
}
const fmt = n => {
  if (typeof n !== 'number' || !Number.isFinite(n)) throw Error('Invalid numeric recipe value');
  return n.toFixed(6).replace(/0+$/,'').replace(/\.$/,'');
};
const ffStart = ['-hide_banner','-nostdin','-loglevel','error','-xerror','-n'];
function failed(e) { console.error(e.stack || e); process.exitCode = 1; }
module.exports = {fs,path,args,file,tool,outDir,run,probe,sha,load,fmt,ffStart,failed};
