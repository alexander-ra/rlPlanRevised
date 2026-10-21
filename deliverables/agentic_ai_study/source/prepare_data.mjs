import fs from 'node:fs';
import crypto from 'node:crypto';
const base = 'C:/Users/UserNIK/projects/rlPlanRevised';
const out = base + '/deliverables/agentic_ai_study/data';
const raw = fs.readFileSync(base + '/outputs/agentic_ai_build/erdos_wiki_snapshot.md','utf8');
const part = raw.split('### 1(a). AI standalone')[1].split('### 1(b).')[0];
const rows = [];
const months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
for (const line of part.split(/\r?\n/)) {
  if (!/^\| \[\[\d+\]\]/.test(line)) continue;
  const cells = line.split('|').slice(1).map(x=>x.trim());
  const id = cells[0].match(/\[\[(\d+)\]\]/)[1];
  const d = cells[2].match(/(\d+)(?:-(\d+))? ([A-Z][a-z]{2}), (\d{4})/);
  if (!d) throw new Error('Unparsed date: '+cells[2]);
  const date = `${d[4]}-${String(months.indexOf(d[3])+1).padStart(2,'0')}-${String(d[2]||d[1]).padStart(2,'0')}`;
  rows.push({problem:id,systems:cells[1],date,dateOriginal:cells[2],outcome:cells[3],full:cells[3].startsWith('🟢')});
}
const csv = (a, keys)=> keys.join(',')+'\n'+a.map(r=>keys.map(k=>'"'+String(r[k]).replaceAll('"','""')+'"').join(',')).join('\n')+'\n';
fs.writeFileSync(out+'/erdos_standalone_rows.csv',csv(rows,['problem','systems','date','dateOriginal','outcome','full']));
const ends=['2025-11-30','2025-12-31','2026-01-31','2026-02-28','2026-03-31','2026-04-30','2026-05-31','2026-06-30'];
const growth=ends.map(end=>({month:end.slice(0,7),recordedProblems:new Set(rows.filter(r=>r.date<=end).map(r=>r.problem)).size,fullResolutionProblems:new Set(rows.filter(r=>r.date<=end&&r.full).map(r=>r.problem)).size}));
const reliability=[10,100,500,1000].map(n=>({steps:n,p99:100*.99**n,p999:100*.999**n,p9999:100*.9999**n}));
fs.writeFileSync(out+'/erdos_growth.csv',csv(growth,['month','recordedProblems','fullResolutionProblems']));
fs.writeFileSync(out+'/reliability.csv',csv(reliability,['steps','p99','p999','p9999']));
const meta={source:'https://github.com/teorth/erdosproblems/wiki/AI-contributions-to-Erd%C5%91s-problems',retrieved:'2026-10-05',sourceCutoff:'2026-06-30',scope:'Section 1(a), AI standalone only. Unique problem IDs, independently deduplicated per series. Full resolutions use green outcome marker. Dates are contribution dates, NOT verification dates. Outcomes are retrospective at source cutoff. Ranges use end date. Includes incorrect, partial and unverified work in total. Selected observational record, not a benchmark, all submissions, journal approvals, or an exponential-growth estimate.',sourceSha256:crypto.createHash('sha256').update(raw).digest('hex'),rows:rows.length,growth,reliability};
fs.writeFileSync(out+'/chart_data.json',JSON.stringify(meta,null,2));
console.log(JSON.stringify({rows:rows.length,growth},null,2));
