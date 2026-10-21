import fs from 'node:fs/promises';
import crypto from 'node:crypto';
import {FileBlob,PresentationFile} from '@oai/artifact-tool';
const root='C:/Users/UserNIK/projects/rlPlanRevised';
const build=root+'/outputs/agentic_ai_build';
const out=root+'/deliverables/agentic_ai_study';
const p=await PresentationFile.importPptx(await FileBlob.load(out+'/presentation_v1.pptx'));
await fs.mkdir(build+'/final-preview',{recursive:true});
const differences=[];
for(let i=0;i<p.slides.items.length;i++){
 const slide=p.slides.items[i];
 const blob=await p.export({slide,format:'png',scale:1});
 const bytes=new Uint8Array(await blob.arrayBuffer());
 const name='slide-'+String(i+1).padStart(2,'0')+'.png';
 await fs.writeFile(build+'/final-preview/'+name,bytes);
 const before=await fs.readFile(build+'/preview/'+name);
 if(crypto.createHash('sha256').update(before).digest('hex')!==crypto.createHash('sha256').update(bytes).digest('hex'))differences.push(i+1);
}
const abstract=(await fs.readFile(out+'/abstract_en.txt','utf8')).trim();
if(abstract.length>1000)throw Error('Abstract limit');
const notes=JSON.parse(await fs.readFile(build+'/notes.json','utf8'));
const total=notes.reduce((a,b)=>a+b.seconds,0);
if(total>900)throw Error('Timing');
console.log(JSON.stringify({slides:p.slides.items.length,abstractCharacters:abstract.length,timingSeconds:total,renderDifferences:differences}));
