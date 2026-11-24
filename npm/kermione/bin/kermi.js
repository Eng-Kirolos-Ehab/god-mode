#!/usr/bin/env node
// God Mode installer for Claude Code.   npx kermione@godmode
// Adds the God Mode marketplace, installs the core plugin, lets you pick categories
// (multi-select, with a description and size for each), installs them, and sets up OpenWolf
// in the current git project. No dependencies. It only runs `claude plugin ...` and `npx openwolf`.
//
// Options: --all | --categories gm-career,gm-video | --no-openwolf | --help
'use strict';

const { spawnSync } = require('child_process');
const fs = require('fs');
const os = require('os');
const path = require('path');
const readline = require('readline');

const REPO = 'Eng-Kirolos-Ehab/god-mode';
const SOURCE = process.env.GM_SOURCE || REPO;                                    // override for testing
const RAW = process.env.GM_RAW || `https://raw.githubusercontent.com/${REPO}/main`; // override for testing
const MARKET = 'god-mode';
const isWin = process.platform === 'win32';

const c = (code) => (s) => (process.stdout.isTTY ? `\x1b[${code}m${s}\x1b[0m` : s);
const bold = c('1'), dim = c('2'), cyan = c('36'), yellow = c('33'), green = c('32'), red = c('31');

function parseArgs(argv) {
  const o = { all: false, categories: null, openwolf: true, help: false };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--all') o.all = true;
    else if (a === '--no-openwolf') o.openwolf = false;
    else if (a === '--help' || a === '-h') o.help = true;
    else if (a === '--categories') o.categories = (argv[++i] || '').split(',').map((s) => s.trim()).filter(Boolean);
    else if (a.startsWith('--categories=')) o.categories = a.slice(13).split(',').map((s) => s.trim()).filter(Boolean);
    else { console.error(red(`unknown option: ${a}`)); process.exit(2); }
  }
  return o;
}

// Child commands get a clean environment: when this runs under `npx`, npm exports npm_config_* vars
// (e.g. npm_config_package) that would make a nested `npx openwolf` run the wrong package.
const cleanEnv = Object.fromEntries(Object.entries(process.env).filter(([k]) => !/^npm_(config|package|lifecycle)_/i.test(k)));

function run(cmd, args, { quiet = false } = {}) {
  const r = spawnSync(cmd, args, { stdio: quiet ? 'pipe' : 'inherit', shell: isWin, encoding: 'utf8', env: cleanEnv });
  return r.status === 0;
}

function has(cmd) {
  const r = spawnSync(cmd, ['--version'], { stdio: 'pipe', shell: isWin, env: cleanEnv });
  return r.status === 0;
}

async function loadCatalog() {
  if (/^https?:\/\//.test(RAW)) {
    const res = await fetch(`${RAW}/catalog.generated.json`);
    if (!res.ok) throw new Error(`could not download the catalog (${res.status})`);
    return res.json();
  }
  return JSON.parse(fs.readFileSync(path.join(RAW, 'catalog.generated.json'), 'utf8'));
}

// Interactive multi-select: ↑/↓ move, space toggles, a = all, enter confirms.
function pickInteractive(cats, already) {
  return new Promise((resolve) => {
    const sel = cats.map((x) => already.has(x.id));
    let cur = 0, lines = 0;
    const out = process.stdout;
    const draw = () => {
      if (lines) out.write(`\x1b[${lines}A\x1b[0J`);
      const rows = [bold('Pick the categories you want') + dim('  (↑/↓ move · space select · a all · enter done)'), ''];
      cats.forEach((x, i) => {
        const box = sel[i] ? green('[x]') : '[ ]';
        const ptr = i === cur ? cyan('›') : ' ';
        const tag = already.has(x.id) ? dim(' (installed)') : '';
        rows.push(`${ptr} ${box} ${bold(x.name)} ${yellow(x.size)}${tag}`);
        if (i === cur) {
          rows.push(`      ${x.description}`);
          if (x.extras) rows.push(dim(`      + ${x.extras}`));
        }
      });
      const total = cats.reduce((s, x, i) => s + (sel[i] ? x.bytes : 0), 0);
      rows.push('', dim(`Selected: ${sel.filter(Boolean).length} · ${(total / 1024).toFixed(0)} KB`));
      out.write(rows.join('\n') + '\n');
      lines = rows.length;
    };
    readline.emitKeypressEvents(process.stdin);
    process.stdin.setRawMode(true);
    process.stdin.resume();
    const onKey = (_s, key) => {
      if (!key) return;
      if (key.ctrl && key.name === 'c') { process.stdin.setRawMode(false); out.write('\n'); process.exit(130); }
      if (key.name === 'up') cur = (cur - 1 + cats.length) % cats.length;
      else if (key.name === 'down') cur = (cur + 1) % cats.length;
      else if (key.name === 'space') sel[cur] = !sel[cur];
      else if (key.name === 'a') { const all = sel.every(Boolean); sel.fill(!all); }
      else if (key.name === 'return' || key.name === 'enter') {
        process.stdin.removeListener('keypress', onKey);
        process.stdin.setRawMode(false);
        process.stdin.pause();
        return resolve(cats.filter((_, i) => sel[i]).map((x) => x.id));
      }
      draw();
    };
    process.stdin.on('keypress', onKey);
    draw();
  });
}

// Fallback when there is no interactive terminal: numbered list, read one line.
function pickByNumbers(cats) {
  cats.forEach((x, i) => {
    console.log(`  [${i + 1}] ${bold(x.name)}  ${yellow(x.size)}`);
    console.log(`      ${x.description}`);
    if (x.extras) console.log(dim(`      + ${x.extras}`));
  });
  return new Promise((resolve) => {
    const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
    rl.question("Numbers separated by spaces (e.g. 1 3 5), 'all', or Enter for none: ", (ans) => {
      rl.close();
      ans = (ans || '').trim();
      if (ans === 'all') return resolve(cats.map((x) => x.id));
      const ids = [];
      for (const n of ans.split(/[\s,]+/).filter(Boolean)) {
        const k = Number(n);
        if (!Number.isInteger(k) || k < 1 || k > cats.length) { console.error(red(`Out of range: ${n}`)); process.exit(2); }
        if (!ids.includes(cats[k - 1].id)) ids.push(cats[k - 1].id);
      }
      resolve(ids);
    });
  });
}

function configDir() {
  return process.env.CLAUDE_CONFIG_DIR || path.join(os.homedir(), '.claude');
}

function readMark() {
  try { return JSON.parse(fs.readFileSync(path.join(configDir(), 'god-mode', 'setup.json'), 'utf8')); } catch { return null; }
}

async function main() {
  const opt = parseArgs(process.argv.slice(2));
  if (opt.help) {
    console.log('npx kermione@godmode [--all | --categories gm-career,gm-video] [--no-openwolf]');
    console.log('Installs God Mode for Claude Code: core + the categories you pick + OpenWolf.');
    return;
  }
  console.log(bold(cyan('\n  God Mode for Claude Code')) + dim('  · by Kermi\n'));

  if (!has('claude')) {
    console.error(red('Claude Code CLI not found. Install it first: https://claude.com/claude-code'));
    process.exit(1);
  }

  console.log(cyan('==> Adding the God Mode marketplace'));
  if (!run('claude', ['plugin', 'marketplace', 'add', SOURCE], { quiet: true })) {
    run('claude', ['plugin', 'marketplace', 'update', MARKET], { quiet: true });
  }
  console.log(cyan('==> Installing the core (router, rules, setup)'));
  if (!run('claude', ['plugin', 'install', `god-mode@${MARKET}`])) { console.error(red('Installing the core failed.')); process.exit(1); }

  const cat = await loadCatalog();
  const cats = cat.categories;
  const prev = readMark();
  const already = new Set((prev && prev.categories) || []);

  let chosen;
  if (opt.all) chosen = cats.map((x) => x.id);
  else if (opt.categories) {
    const bad = opt.categories.filter((id) => !cats.some((x) => x.id === id));
    if (bad.length) { console.error(red(`Unknown category: ${bad.join(', ')}. Valid: ${cats.map((x) => x.id).join(', ')}`)); process.exit(2); }
    chosen = opt.categories;
  } else {
    console.log('');
    console.log(dim(`God Mode ${cat.version} · core ${cat.core.size} is always installed`));
    chosen = process.stdin.isTTY && process.stdout.isTTY ? await pickInteractive(cats, already) : await pickByNumbers(cats);
  }

  for (const id of chosen) {
    if (already.has(id)) continue;
    console.log(cyan(`==> Installing ${id}`));
    run('claude', ['plugin', 'install', `${id}@${MARKET}`]);
  }

  const all = [...new Set([...(prev && prev.categories) || [], ...chosen])];
  fs.mkdirSync(path.join(configDir(), 'god-mode'), { recursive: true });
  fs.writeFileSync(path.join(configDir(), 'god-mode', 'setup.json'), JSON.stringify({
    version: cat.version, categories: all, openwolf: opt.openwolf ? 'auto' : 'off', updated: new Date().toISOString(), install: 'npx kermione@godmode',
  }, null, 2) + '\n');

  if (opt.openwolf) {
    const proj = process.cwd();
    const ow = `openwolf@${cat.openwolf.version}`;
    if (!fs.existsSync(path.join(proj, '.git')) || proj === os.homedir()) {
      console.log(dim('OpenWolf: will be set up automatically the next time you open Claude Code in a git project.'));
    } else if (fs.existsSync(path.join(proj, '.wolf'))) {
      console.log(dim('OpenWolf: already set up in this project.'));
    } else {
      console.log(cyan(`==> Setting up OpenWolf ${cat.openwolf.version} in ${proj}`));
      const ok = run('npx', ['-y', ow, 'init', '--agent', 'claude']) && fs.existsSync(path.join(proj, '.wolf'));
      if (!ok) console.log(red(`OpenWolf setup did not finish. Run it yourself in this folder: npx -y ${ow} init --agent claude`));
    }
  }

  console.log(green(`\nDone. ${chosen.length ? `Installed: ${chosen.join(', ')}. ` : ''}Restart Claude Code, then type /god-mode <task>.`));
  console.log(dim('Change categories any time: /god-mode:setup inside Claude Code, or run npx kermione@godmode again.'));
}

main().catch((e) => { console.error(red(`Error: ${e.message}`)); process.exit(1); });
