const pr=await eda.dmt_Project.getCurrentProjectInfo();if(pr.uuid!=="02ea8fb2e66040299c1c16192899224e7332b1b47147f009f3b0e759a20328af")throw Error('Wrong10');
await eda.dmt_EditorControl.openDocument('52a8a60e5711e55b');
const t=(await eda.sch_PrimitiveText.getAll()).sort((a,b)=>a.getState_Y()-b.getState_Y());if(t.length!==4)throw Error('Expected4 notes');
const texts=['R2.1 REVIEW ONLY - MCU interfaces: independent SWD/UART 3V3 SENSE - 5/6','J3.1/J4.1 are sense only (NOT power inputs), each4.99k; NRST1k OD/OC VOL<=0.4V HiZ','8state/288transfers32dummy256valid; epoch/replay/progress/two good frames; 100fps BENCH_PENDING','SWD series4.99k retained: start about100kHz; normal1-7k/10%; 300us/calibration BENCH_PENDING'];
const before=await eda.sys_FileManager.getDocumentSource();
for(let i=0;i<4;i++)await eda.sch_PrimitiveText.modify(t[i],{value:texts[i]});
const saved=await eda.sch_Document.save();if(saved!==true)throw Error('Savefailed');return {project:pr.uuid,texts,before,after:await eda.sys_FileManager.getDocumentSource(),saved,attemptCount:1};
