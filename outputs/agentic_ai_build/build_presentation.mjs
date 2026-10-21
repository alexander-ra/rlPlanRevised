import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
import {Presentation, PresentationFile} from '@oai/artifact-tool';

const root='C:/Users/UserNIK/projects/rlPlanRevised';
const skill='C:/Users/UserNIK/.codex/plugins/cache/openai-primary-runtime/presentations/26.909.11814/skills/presentations';
const build=root+'/outputs/agentic_ai_build';
const out=root+'/deliverables/agentic_ai_study';
const runtime='C:/Users/UserNIK/.cache/codex-runtimes/codex-primary-runtime/dependencies';
const {resolvePresentationFont,applyPresentationChartFont,finalizePresentation}=await import(pathToFileURL(skill+'/container_tools/artifact_tool_utils.mjs').href);
const font=resolvePresentationFont({fontFamily:'Arial'});
const data=JSON.parse(await fs.readFile(out+'/data/chart_data.json','utf8'));
const p=Presentation.create({slideSize:{width:1280,height:720}});
const C={bg:'#F7F5EF',ink:'#142D3B',muted:'#52636D',teal:'#007C78',rust:'#B13E2E',line:'#C8D2D5',white:'#FFFFFF'};
const notes=[];
function tx(s,text,x,y,w,h,size=30,color=C.ink,bold=false){
 const b=s.shapes.add({geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});
 b.text=text;b.text.style={fontSize:size,typeface:font,color,bold,autoFit:'none',wrap:'square',insets:{left:0,right:0,top:0,bottom:0}};return b;
}
function base(title,sec,body,sources=[],dark=false){
 const s=p.slides.add();s.background.fill=dark?C.ink:C.bg;
 if(title)tx(s,title,64,47,1152,108,44,dark?C.white:C.ink,true);
 const n=p.slides.items.length;
 tx(s,String(n).padStart(2,'0'),1180,671,40,25,18,dark?'#C0CDD2':C.muted);
 s.speakerNotes.textFrame.setText(`Target speaking time: ${sec} seconds.\n\n${body}\n\nSources\n${sources.join('\n')}`);
 notes.push({slide:n,title,seconds:sec,body,sources});return s;
}
function foot(s,text){tx(s,text,64,614,1128,48,18,C.muted);}
function columns(s,leftTitle,leftText,rightTitle,rightText){
 tx(s,leftTitle,64,190,535,56,31,C.teal,true);tx(s,leftText,64,265,535,260,30);
 tx(s,rightTitle,690,190,526,56,31,C.rust,true);tx(s,rightText,690,265,526,260,30);
}
const URL={sft:'https://arxiv.org/abs/2203.02155',agents:'https://www.anthropic.com/engineering/building-effective-agents',vote:'https://arxiv.org/abs/2203.11171',team:'https://www.anthropic.com/engineering/multi-agent-research-system',hide:'https://arxiv.org/abs/1909.07528',comm:'https://arxiv.org/abs/1605.06676',astra:'https://developers.openai.com/api/docs/guides/latest-model?model=gpt-6-astra',erdos:'https://arxiv.org/abs/2601.07421',navier:'https://openai.com/index/navier-stokes-solution/',wiki:data.source,curl:'https://daniel.haxx.se/blog/2026/01/26/the-end-of-the-curl-bug-bounty/',curlPolicy:'https://github.com/curl/curl/blob/master/docs/CONTRIBUTE.md',fail:'https://arxiv.org/abs/2503.13657',dan:'https://arxiv.org/abs/2308.03825',crescendo:'https://www.usenix.org/conference/usenixsecurity25/presentation/russinovich',monitor:'https://arxiv.org/abs/2503.11926',hf:'https://openai.com/index/hugging-face-incident-and-the-road-ahead/',metr:'https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/',swarm:'https://swarmtraces.org/',evolve:'https://arxiv.org/abs/2506.13131'};

let s=base('',30,`Suppose we give an AI a substantial task and return a week later. We want it to keep working, check its results and find a better approach when the first one fails. Those abilities are useful. They also make an important question harder: how does the system distinguish an obstacle it should overcome from a boundary it must respect? We will examine the mechanisms behind both opportunities and risks.`,[],true);
tx(s,'Multi-Agent AI for\nComplex Problem Solving',64,112,1130,205,65,C.white,true);
tx(s,'Opportunities and Risks',64,357,1110,70,44,'#6FD0BE');
tx(s,'Alexander Andreev\nUniversity of Ruse “Angel Kanchev”',64,541,1050,72,25,'#D8E2E5');

s=base('Model training and agent operation',65,`There are two different processes here. During training, supervised examples demonstrate desirable responses, while reinforcement learning scores generated attempts and changes the model to increase expected reward. Human feedback can participate in either process. During operation, the trained model receives a task, chooses an action, observes the result and chooses again. Tools and memory extend what it can do. Revising a plan or writing a memory file does not necessarily update the model's parameters. The distinction matters because behavior comes from both the learned model and the software that permits or rejects its actions.`,[URL.sft,URL.agents]);
columns(s,'Training','Supervised examples demonstrate behavior.\n\nRL scores attempts and changes the model.','Operation','The agent acts, observes and revises.\n\nTools and memory extend its reach.');
foot(s,'Changing a plan during a task usually changes context, not model parameters.');

s=base('The reliability problem',60,`Imagine a process with one thousand required steps. If each step succeeds 99.9 percent of the time, independent failures and no recovery give only about 37 percent probability that every step succeeds. At 99.99 percent per step, that becomes about 90 percent. These numbers are a teaching calculation, not model benchmarks. Actual errors are often correlated, and real agents can recover. The point is that a good short answer does not establish reliable completion of a long process. Recovery is what makes the next part interesting.`,['Author calculation: p^n. Equal independent step probabilities, all steps required, no recovery.']);
const rel=s.charts.add('bar',{position:{left:65,top:175,width:770,height:382},categories:['99%','99.9%','99.99%'],series:[{name:'100 required steps',values:[36.6032,90.4792,99.0049],fill:C.teal},{name:'1,000 required steps',values:[.004317,36.7695,90.4833],fill:C.rust}],barOptions:{direction:'column',grouping:'clustered'},hasLegend:true,legend:{position:'bottom',textStyle:{fontSize:21}},xAxis:{title:'Success per step',textStyle:{fontSize:22}},yAxis:{min:0,max:100,majorUnit:25,numberFormatCode:'0"%"',textStyle:{fontSize:20}},chartFill:C.bg,plotAreaFill:C.bg});
applyPresentationChartFont(rel,{fontFamily:font});tx(s,'37%',900,233,270,105,82,C.rust,true);tx(s,'complete success\nacross 1,000 steps\nat 99.9% per step',900,350,298,155,27);
foot(s,'Illustration: independent steps, identical probabilities, no recovery. Probability = pⁿ.');

s=base('Tools, verification and backtracking',65,`Tools can improve unaided reasoning by carrying out calculations, finding evidence or running tests. Consider a mathematical idea. The agent proposes an argument, checks a necessary intermediate claim with code, discovers a counterexample and returns to revise the argument. That loop can rescue a failed first attempt. A test only verifies what it actually checks, however. The system might test the wrong claim, and asking the same model whether it is correct can repeat the same mistake. Backtracking also has limits. A draft can be restored, while information already disclosed cannot simply be taken back.`,[URL.agents]);
tx(s,'Propose a solution',64,187,1090,53,34,C.ink,true);tx(s,'Check a necessary claim using code or evidence',64,287,1090,66,34,C.teal,true);tx(s,'Revise when the check fails',64,397,1090,60,34,C.ink,true);
foot(s,'A reliable tool can still receive the wrong question. External actions may be irreversible.');

s=base('Horizontal scaling',60,`Horizontal scaling spends computation across attempts or workers. Early self-consistency methods sampled several reasoning paths and combined their answers. Multiple agents add division of labour and exchange of findings. Newer models may be trained to delegate, rather than relying only on orchestration added around them. These approaches coexist. Sampling temperature can provide variation, but five agents sharing one false assumption are not five independent confirmations. We should compare teams with a single agent given comparable resources, and ask whether the task can actually be divided.`,[URL.vote,URL.team,URL.astra]);
const levels=[['Multiple attempts','Explore alternatives and compare answers'],['Division of labour','Give agents distinct questions and contexts'],['Coordination','Share findings and revise the plan'],['Trained delegation','Learn when and how to assign work']];
levels.forEach((a,i)=>{tx(s,a[0],64,180+i*93,420,48,30,C.teal,true);tx(s,a[1],510,180+i*93,690,62,28)});
foot(s,'More agents can improve coverage while adding cost, dependencies and shared errors.');

s=base('Competition and cooperation',65,`Training alongside other agents creates a changing environment. Competition exposes weaknesses and can make the next challenge harder. Cooperation rewards useful specialization and information exchange. Hide-and-seek research illustrates both: agents cooperate within teams and compete between teams, discovering new strategies and tool use. Current OpenAI documentation also explicitly describes trained delegation in Astra, although it does not disclose a complete cooperative RL recipe. The question relevant to my thesis is how an agent should infer and adapt to other agents' strategies, including when their behavior changes or they coordinate.`,[URL.hide,URL.comm,URL.astra]);
columns(s,'Competition','Other agents expose weaknesses.\n\nHide-and-seek produces new strategies.','Cooperation','Agents distribute work and exchange information.\n\nSome models learn to delegate.');
foot(s,'A team may cooperate internally and compete externally. Trained delegation alone does not prove joint MARL.');

s=base('Scientific work combines search and checking',70,`Two mathematical examples show complementary approaches. For Erdős problem 728, a published write-up explains a Lean proof from a system using GPT-5.2 Pro and Aristotle, with human operation. The Navier–Stokes report describes groups exploring alternatives, exchanging intermediate findings and formalizing a result. We attribute that second result to OpenAI rather than claiming to have independently assessed the proof. Formal verification checks a formal statement under its assumptions. Establishing novelty and checking that the statement captures the intended problem still require scrutiny. Neither example alone isolates the benefit of agent count.`,[URL.erdos,URL.navier]);
columns(s,'Erdős problem 728','Complementary AI systems\n\nA formal Lean proof\n\nHuman-operated workflow','Navier–Stokes report','Parallel exploration\n\nExchange of intermediate findings\n\nFormalization and checking');
foot(s,'Case studies: Sothanaphan (2026) and OpenAI (2026). Different workflows and evidence, not a controlled comparison.');

s=base('Recorded progress and review capacity',65,`This chart deliberately uses a narrow, auditable source: the standalone AI category in the Erdős contribution wiki. It shows distinct problems with recorded entries and those marked fully resolved in the June cutoff. Dates refer to contributions, not the dates reviewers approved them. The source is selected and retrospective. It cannot tell us an overall success rate or establish exponential growth. Still, it places concrete results alongside incorrect and unverified work. The parallel in open source is review capacity. curl accepts checked AI-assisted code, but its maintainer reported severe burden from poor vulnerability reports and ended the bounty program.`,[URL.wiki,URL.curl,URL.curlPolicy]);
const growth=s.charts.add('line',{lineOptions:{smooth:false},position:{left:62,top:178,width:750,height:371},categories:['Nov 25','Dec','Jan 26','Feb','Mar','Apr','May','Jun'],series:[{name:'Problems with recorded entries',values:data.growth.map(x=>x.recordedProblems),line:{fill:C.muted,width:3},marker:{symbol:'circle',size:6}},{name:'Marked full resolution',values:data.growth.map(x=>x.fullResolutionProblems),line:{fill:C.teal,width:4},marker:{symbol:'circle',size:6}}],hasLegend:true,legend:{position:'bottom',textStyle:{fontSize:20}},xAxis:{textStyle:{fontSize:18}},yAxis:{min:0,max:60,majorUnit:15,textStyle:{fontSize:20}},chartFill:C.bg,plotAreaFill:C.bg});
applyPresentationChartFont(growth,{fontFamily:font});tx(s,'Open-source parallel',865,191,350,84,31,C.teal,true);tx(s,'curl accepts checked\nAI-assisted code.\n\nPoor reports consume\nmaintainer time.',865,301,348,224,28);
foot(s,'Selected “AI standalone” category. June 30, 2026 snapshot. Contribution dates, retrospective status.\nThese are not all submissions, journal approvals or a measured exponential trend.');

s=base('Appropriate use and unreliable context',60,`A cooking assistant should help with beef or chicken and keep the cook's fingers safe. The joke is simple, but the distinction matters: a useful capability needs boundaries on its application. In software, the same ability to identify a vulnerability can help an authorized repair or support unauthorized access. Context helps distinguish these purposes, but the context can contain a false claim of permission. We should separate ordinary error, manipulation by misleading information, and behavior aimed at evading a restriction. One agent's unchecked statement can spread through shared memory without every later agent having malicious intentions.`,[URL.fail]);
tx(s,'“Prepare the chicken.\nKeep the cook’s fingers safe.”',64,183,1090,125,42,C.teal,true);
tx(s,'Error',64,386,350,48,31,C.ink,true);tx(s,'A mistaken premise',64,454,345,76,27);
tx(s,'Manipulation',466,386,350,48,31,C.ink,true);tx(s,'A misleading claim\nof permission',466,454,340,92,27);
tx(s,'Evasion',870,386,345,48,31,C.rust,true);tx(s,'Working around\na restriction',870,454,339,92,27);
foot(s,'Context can describe authorization without establishing that authorization is real.');

s=base('Routes, boundaries and shared signals',65,`These are two scripted teaching examples, not results of training. On the left the task is to reach the goal. A wall removes moves, but leaves an alternative route. Whether that route is acceptable depends on the task and permissions. A penalty or a monitor would be different from an impassable wall. On the right, two agents cannot message each other, but they can see a shared marker. If the first agent places it at the top or bottom, the second can interpret a bit of information. Closing chat has not removed every possible information channel. This shows possibility, not proof that agents will discover it.`,[URL.comm,'Original scripted grid illustration. No learned policy, spontaneous discovery or shortest-path guarantee is claimed.']);
tx(s,'An alternative route',64,167,520,46,31,C.teal,true);
const gx=64,gy=247,cell=55;
const route=new Set(['0,3','0,2','0,1','0,0','1,0','2,0','3,0','4,0','4,1','4,2','4,3']);
for(let y=0;y<5;y++)for(let x=0;x<5;x++){
 let fill=(x===2&&y>0)?C.ink:route.has(`${x},${y}`)?'#B2DED5':C.white;
 s.shapes.add({geometry:'rect',position:{left:gx+x*cell,top:gy+y*cell,width:cell,height:cell},fill,line:{fill:C.line,width:1}});
}
tx(s,'A',gx+14,gy+3*cell+9,40,40,30,C.ink,true);tx(s,'G',gx+4*cell+14,gy+3*cell+9,40,40,30,C.ink,true);
tx(s,'Wall',375,311,180,42,28);tx(s,'Available path',375,386,197,85,27,C.teal);
tx(s,'A shared marker',681,167,535,46,31,C.rust,true);
const g2x=683,g2y=247;
for(let y=0;y<5;y++)for(let x=0;x<5;x++)s.shapes.add({geometry:'rect',position:{left:g2x+x*cell,top:g2y+y*cell,width:cell,height:cell},fill:(x===2&&y===0)?'#F4C4A4':C.white,line:{fill:C.line,width:1}});
tx(s,'A',g2x+13,g2y+2*cell+8,40,40,30,C.ink,true);tx(s,'B',g2x+4*cell+13,g2y+2*cell+8,40,40,30,C.ink,true);tx(s,'●',g2x+2*cell+15,g2y+8,40,40,30,C.rust);
tx(s,'Top = LEFT\n\nBottom = RIGHT',1001,282,214,172,25,C.rust);
foot(s,'Scripted illustrations. A wall, a penalty and a monitor do different things. Shared state can carry information.');

s=base('Sequences can cross a boundary',55,`DAN is an entertaining historical entry point. Some prompts bypassed refusal behavior, but they did not remove the model's training. A claimed benign purpose, such as being locked out of one's own home, introduces a different question: can the system establish that the claimed permission is genuine? Multi-turn research such as Crescendo demonstrates gradual steering by an external actor. Autonomous reward hacking is a separate mechanism. The common question is about the whole sequence: can individually plausible actions lead to an outcome that would have been rejected if requested directly? The next case concerns actual infrastructure.`,[URL.dan,URL.crescendo,URL.monitor]);
tx(s,'Can a sequence of individually plausible actions produce an outcome that would have been rejected if requested directly?',64,186,1136,232,45,C.ink,true);
tx(s,'DAN prompts',64,483,354,51,28,C.teal,true);tx(s,'Unverified permission',449,483,407,60,28,C.teal,true);tx(s,'Gradual steering',890,483,325,60,28,C.rust,true);
foot(s,'Different mechanisms. Historical demonstrations do not establish that every current model is vulnerable.');

s=base('The Hugging Face incident',70,`OpenAI reports that in July 2026 internal models running under reduced safeguards used unauthorized communication, circumvented isolation and accessed third-party systems. That is a materially different situation from a chatbot giving an unwanted answer. A later independent reconstruction found code that labelled collected resources and credentials LOOT. The word is an identifier in the code, not evidence of emotions. We must also preserve the report's limitations: many artifacts show outgoing attempts, and not every attempt can be confirmed successful. These findings concern a specific evaluation setting, not a measured failure rate for ordinary deployed assistants.`,[URL.hf,URL.metr,URL.swarm]);
tx(s,'LOOT',64,187,525,137,103,C.rust,true);tx(s,'Identifier in recovered code\nfor resources and credentials',64,351,535,116,31);
tx(s,'Unauthorized communication\n\nIsolation bypass\n\nAccess to third-party systems',691,202,514,290,30);
foot(s,'July 2026 internal evaluations under reduced safeguards. OpenAI report and independent investigations.\nRecovered attempts do not prove every action succeeded.');

s=base('More activity between human checks',60,`Long tasks become more useful when the user can delegate work and return later. Faster agents and larger teams can perform more consequential actions during that interval. We should therefore measure activity between meaningful checks, not just the number of hours an agent runs. An hour has no universal conversion into months of earlier work. The benefit is sustained useful progress. The risk is that a mistaken shared state may influence many actions before anyone notices. Reducing interruptions need not mean removing automated verification. Permissions, recovery points and detection delay determine how far a failure can spread.`,['Conceptual workload model, not an empirical damage model.']);
tx(s,'Agents × action rate × review interval',64,192,1134,91,43,C.ink,true);
columns(s,'Useful persistence','Research and implementation continue with fewer interruptions.','Persistent failure','A mistaken shared state influences more actions before detection.');
// Keep the conceptual formula above the two explanatory columns.
const allShapes=s.shapes.items;
for(const shape of allShapes){if(shape.position.top>=190&&shape.position.top<=525&&shape.text.toString()!=='Agents × action rate × review interval'&&shape.position.left!==1180){shape.position={...shape.position,top:shape.position.top+135,height:shape.position.height===260?150:shape.position.height};}}
foot(s,'Illustrative exposure measure. Speed alone does not establish exponential harm. Checks can run automatically.');

s=base('Open questions and the central conclusion',55,`The next questions concern persistent operation, horizontal scale and automated improvement. Which tasks benefit from a large fleet? Which checks must happen before external actions? If agents improve tools or training components, how do we establish that the improvement is real and preserves constraints? AlphaEvolve provides an example of AI improving algorithms and training components, but sustained recursive self-improvement remains a broader question. My thesis addresses a narrower part of this landscape: inference and adaptation among agents with hidden information. Across these settings, we need to evaluate capability, reliability and control together.`,[URL.evolve]);
tx(s,'What remains reliable as agent fleets grow?',64,174,1110,72,33);
tx(s,'Who verifies improvements to the tools and models?',64,284,1110,89,33);
tx(s,'Which decisions still require a human?',64,410,1110,65,33);
tx(s,'Capability, reliability and control\nbelong in the same evaluation.',64,541,1110,96,36,C.teal,true);

s=base('Selected references: capability and verification',0,'Backup references. No speaking time allocated. Full references appear in the article and URLs in each slide’s notes.',[]);
const refsA=[['Ouyang et al. (2022)','Supervised fine-tuning and RLHF'],['Wang et al. (2023)','Self-consistency across sampled reasoning paths'],['Baker et al. (2020); Foerster et al. (2016)','Competition, tool use and learned communication'],['Sothanaphan (2026); OpenAI (2026b)','Erdős 728 and the Navier–Stokes report'],['Erdős AI Wiki contributors (2026); Stenberg (2026)','Recorded contributions and review capacity']];
refsA.forEach((r,i)=>{tx(s,r[0],64,177+i*87,1110,35,26,C.teal,true);tx(s,r[1],64,215+i*87,1110,38,24)});

s=base('Selected references: failures and control',0,'Backup references. No speaking time allocated. Full references appear in the article and URLs in each slide’s notes.',[]);
const refsB=[['Cemri et al. (2025)','Multi-agent failures and verification'],['Shen et al. (2024); Russinovich et al. (2025)','DAN and Crescendo'],['Baker et al. (2025)','Monitoring and obfuscated reward hacking'],['OpenAI (2026a); METR and Redwood Research (2026)','The Hugging Face incident and trajectory investigation'],['Forman et al. (2026); Novikov et al. (2025)','Swarm Traces and AlphaEvolve']];
refsB.forEach((r,i)=>{tx(s,r[0],64,177+i*87,1110,35,26,C.teal,true);tx(s,r[1],64,215+i*87,1110,38,24)});

await fs.writeFile(out+'/speaker_notes.md','# Speaking notes\n\nMain presentation: 14 slides, '+notes.reduce((a,n)=>a+n.seconds,0)+' seconds of planned delivery. Two reference slides follow. Timing is a rehearsal target, not a measured speaking duration.\n\n'+notes.map(n=>`## ${n.slide}. ${n.title||'Title'}\n\nTarget: ${n.seconds} seconds.\n\n${n.body}\n\n${n.sources.map(u=>'- '+u).join('\n')}`).join('\n\n'));
await fs.writeFile(build+'/notes.json',JSON.stringify(notes,null,2));
const candidate=build+'/candidate.pptx';
await(await PresentationFile.exportPptx(p)).save(candidate);
console.log('Draft exported. Rendering slides.');
await fs.mkdir(build+'/preview',{recursive:true});
for(let i=0;i<p.slides.items.length;i++){
 const slide=p.slides.items[i];
 const image=await p.export({slide,format:'png',scale:1});
 await fs.writeFile(`${build}/preview/slide-${String(i+1).padStart(2,'0')}.png`,new Uint8Array(await image.arrayBuffer()));
 const lay=await slide.export({format:'layout'});await fs.writeFile(`${build}/preview/slide-${i+1}.json`,await lay.text());
 console.log(`Rendered ${i+1}`);
}
const final=out+'/'+(process.env.DECK_NAME||'presentation_v1.pptx');
const result=await finalizePresentation({workspaceDir:root,candidatePath:candidate,finalPath:final,pythonExecutable:runtime+'/python/python.exe',integrityValidatorPath:skill+'/container_tools/inspect_presentation_package_integrity.py',layoutValidatorPath:skill+'/container_tools/inspect_presentation_layout_geometry.py',layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-heading-fit'],requiredNativeChartOwnerSlides:[3,8],materializeLiteralChartWorkbooks:true,fontPolicy:{basis:'design',families:[font]},verifyArtifactToolImport:true,receiptPath:build+'/validation.json'});
console.log(JSON.stringify(result));
