import fs from 'node:fs/promises';
import {Workbook} from '@oai/artifact-tool';
const out='E:/open/SCIENCE_ADK5556_4X4_DAQ_REPLICA/R21_SCHEMATIC_ACCEPTANCE_AND_BENCH_RELEASE_PREP_V1';
const inputs=JSON.parse(await fs.readFile(out+'/TABLE_INPUTS.json','utf8'));
const wb=Workbook.create();const results=[];
for(const name of ['BENCH_TEST_MATRIX.csv','EXPECTED_NODE_RANGES.csv']){
 const rows=inputs[name],sheet=wb.worksheets.add(name==='BENCH_TEST_MATRIX.csv'?'TestMatrix':'NodeExpectations');
 const grid=sheet.getRangeByIndexes(0,0,rows.length,rows[0].length);grid.values=rows;
 grid.format.font={name:'Arial',size:11};grid.format.columnWidthPx=120;grid.format.rowHeightPx=27;
 sheet.getRangeByIndexes(0,0,1,rows[0].length).format={fill:'#21374a',font:{name:'Arial',size:11,bold:true,color:'#ffffff'}};
 sheet.showGridLines=false;sheet.freezePanes.freezeRows(1);sheet.getRange('A:A').format.columnWidthPx=160;sheet.getRange('B:B').format.columnWidthPx=210;
 sheet.getRange('C:C').format.columnWidthPx=220;sheet.getRange('D:D').format.columnWidthPx=210;
 if(name==='EXPECTED_NODE_RANGES.csv'){sheet.getRange('C:C').format.columnWidthPx=120;sheet.getRange('D:E').format.columnWidthPx=190;sheet.getRange('F:F').format.columnWidthPx=65;sheet.getRange('G:G').format.columnWidthPx=170;}
 results.push({name,sheet,rows});
}
wb.recalculate();
const checks=[];
for(const {name,sheet,rows} of results){
 const actual=sheet.getRangeByIndexes(0,0,rows.length,rows[0].length).values;
 if(JSON.stringify(actual)!==JSON.stringify(rows))throw Error('typed values differ '+name);
 const escape=v=>v===null?'':typeof v==='string'&&/[",\r\n]/.test(v)?'"'+v.replaceAll('"','""')+'"':String(v);
 await fs.writeFile(out+'/'+name,actual.map(r=>r.map(escape).join(',')).join('\r\n')+'\r\n','utf8');
 const check=await wb.inspect({kind:'table',range:sheet.name+'!A1:H4',include:'values,formulas',tableMaxRows:4,tableMaxCols:8,maxChars:1600});
 checks.push({name,rows:rows.length-1,columns:rows[0].length,allTypedValuesExact:true,staticInputContract:true,measurements:0,inspect:check.ndjson});
 if(!process.argv[2] || process.argv[2]===sheet.name){const preview=await wb.render({sheetName:sheet.name,range:name.startsWith('BENCH')?'A1:J8':'A1:G8',scale:1,format:'png'});await fs.writeFile(out+'/'+sheet.name+'_preview.png',new Uint8Array(await preview.arrayBuffer()));}
}
await fs.writeFile(out+'/TABLE_AUTHORING_CHECK.json',JSON.stringify({engine:'bundled @oai/artifact-tool',outputFormat:'requested CSV only; no extra XLSX',recalculated:true,scientificTests:0,checks},null,2)+'\n','utf8');
console.log(JSON.stringify(checks.map(x=>({name:x.name,rows:x.rows,columns:x.columns,exact:x.allTypedValuesExact}))));
