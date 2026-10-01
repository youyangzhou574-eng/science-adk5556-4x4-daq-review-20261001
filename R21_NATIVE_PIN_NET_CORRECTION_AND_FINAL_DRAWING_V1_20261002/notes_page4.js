const pr=await eda.dmt_Project.getCurrentProjectInfo();if(pr.uuid!=='b771f646994e1e87ccac719bcaeddd7f79898452652eb8c78e76c7463539d085')throw Error('Wrong09');
await eda.dmt_EditorControl.openDocument('52a8a60e5711e55b');
const t=(await eda.sch_PrimitiveText.getAll()).sort((a,b)=>a.getState_Y()-b.getState_Y());if(t.length!==4)throw Error('4 notes expected');
const texts=['R2.1 REVIEW ONLY - MCU / protected interfaces - 5/6','J3.5 NRST: 1k direct; external OD/OC, VOL<=0.4V, release HiZ. SWD/UART remain4.99k','BLANK0/ROW0..BLANK3/ROW3; 8x1.2ms +0.4ms; 288 transfers /32dummy /256valid','Epoch/replay/progress watchdog + two good frames; 100fps/WCET/latency BENCH_PENDING'];
for(let i=0;i<t.length;i++)await eda.sch_PrimitiveText.modify(t[i],{content:texts[i]});
return {saved:await eda.sch_Document.save(),texts};
