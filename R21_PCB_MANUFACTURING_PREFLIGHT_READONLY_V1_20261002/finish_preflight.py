import pathlib,json,csv,hashlib,datetime
p=pathlib.Path(__file__).parent
rows=[]
def row(id,item,status,evidence,needed="",scope="read-only preflight"):
 rows.append({"id":id,"item":item,"status":status,"evidence":evidence,"requiredInputOrAction":needed,"scope":scope})
row("G01","Accepted electrical PCB baseline","PASS","Pro16; e9c1b72; warm/coldnativeDRCall0 inherited","no new DRC","electrical review only; not manufacture")
row("G02","Board100x90mm/fourlayer order","PASS","native POLY11 bounds100.00000066x90.00000034; layers1/15/16/2","")
row("G03","6/12/16/20mil existing traces","PASS","actual909 widths counts756/100/7/46; no edits","","existing width geometry only")
row("G04","Selected copper thickness/trace-spacing capability","PENDING_INPUT","min6mil; frozen rule TrackTrack~.102mm, pad~.152mm, zone.254mm","fabricator+outside/inside copper weight; current10mil not universal")
row("G05","297throughvias12/24mil","PASS","native drills.3048 pads.6096 ring.1524mm","","geometry dimensions, not finishedhole guarantee")
row("G06","Hole-hole and user copper-to-edge screen","PASS","min holepair.31115mm; via2.39413 trace2.44493 pad4.06926mm","","existing CAD geometry; ellipse approximation/rounded API centers, not CAM")
row("G07","4POUR and e307 region","PASS","inherited warm/cold0; keepIslandfalse; accepted fifteenfill update, existing fourlayerPNG inspected","","no obvious island in evidence; not full fabricated copper continuity")
row("G08","Selected boardedge/routing/panel process","PENDING_INPUT","currentnominalrectangular100x90; no factory data","fabroute/vcut/panel/tooling contract")
row("G09","Partpad-number coverage","PASS","176/550 actual-number sets match frozen22 nativeFP docs","","numbers only; prior electricalmapping accepted")
row("G10","OPA4388/OPA2388 package pitch","PASS","U1/U2 14pad1.27mm;U3 8pad1.27mm; prioracceptedpinmap","","currentgeometry/identity")
row("G11","TMUX1134 package pitch","PASS","U4 20pad;native TSSOP.65mm; prioracceptedpinmap","","currentgeometry/identity")
row("G12","ADS8684 package number/pitch/orientation","PASS","U5 38pads .5mm nominal rotation180 pin1rightbottom; DBT0038A","","not blanketland/stencilqualification")
row("G13","STM32G031K8T6 number/pitch/orientation","PASS","U7 32pad.8mm LQFP32 body7x7 rotation0; ST DS12992rev4","","not blanketland/stencilqualification")
row("G14","LM73100RPWR 10-electrode pattern","PASS","U9/U10 10pad;RPW0010A corners and5/6longlands; no additionalEP","","package hasmixed.45/.475 geometry")
row("G15","TPS389001DSET 6-electrode pattern","PASS","U11/U12 6pad .5mm DSE; no7thEP","","onlypin/patterncoverage")
row("G16","BAT54S215 pinpattern/polarity netmap","PASS","1GND/2V5/3output forD_TIA0;SOT23 split2+1;Nexperiap5","","assembly polarity must stillcheck")
row("G17","J1-J4 pinpitch/drill geometry","PASS","2/8/6/4nativePTHpads2.54mm;1.1/1.0/1.2/1.1mmholes","","nativeholeauthority, API summarynot drillunits")
row("G18","J1-J4 exactMPN/mechanicalmating","PENDING_INPUT","Manufacturer/MPN fourheadersblank","exactmaker/MPN/pinsection/height/matingorientation")
row("G19","ExistingstructuredBOM","PASS","176rows Manufacturer/MPN/Value/Footprint/Qty; Descriptionexcluded","","extractioncoverage;4genericheadersstillpending")
row("G20","Finepitchmask/stencil/land acceptance","PENDING_INPUT","U9/U10 maskbridge~.090081mm;U5~.096774mm; currentlandsexamplesnotstrictsame","factorymaskcapabilities+land/stencilapproval; ifrejectconcentratedminimalECO")
row("G21","Nominal2Dbodyoverlap screen","PASS","175supportedbodyoutlines,0overlappairs;min.300002mm","","notall176/fullcourtyard/3D")
row("G22","Courtyard/3D/toolspace/pin1silkscreen","PENDING_INPUT","U6supportedbodymissing; redplotcomponentmarkingnotfinalsilkcertificate","assembler+selectedparttolerance/mechanicalapproval")
row("G23","Existingprobe access","PASS","13nets candidates CSV; PGOOD R_RST.2;TIA0distinctTIA_DRV0","","padpresenceonly, no benchrelease")
row("G24","Instruments/operator/assembledsample","PENDING_INPUT","no userconcreteinputs","physicalboard/probes/operators/powerrelease")
row("C01","Fabricator/service/stackup","PENDING_INPUT","notselected","user/fabchoice")
row("C02","Boardthickness/tolerance","PENDING_INPUT","unknown","user/fab")
row("C03","Copperweights","PENDING_INPUT","unknown","user/fab")
row("C04","Laminate/core/prepreg/Tg/flame/UL","PENDING_INPUT","unknown","user/fab")
row("C05","Finish","PENDING_INPUT","unknown","user/fab")
row("C06","Maskcolor/expansion/tolerance/via treatment","PENDING_INPUT","existingrulesnotfabcontract","user/fabCAM")
row("C07","Drillplating/tolerance/finishedholedefinition","PENDING_INPUT","CADdimensionsknownnotproductionguarantee","fabricator")
row("C08","Panel/fiducials/tooling","PENDING_INPUT","no packageadded","assembler/fab")
row("C09","Stencil/reflow/inspection","PENDING_INPUT","QFN-HR/WSONbottomcontacts","assemblerprocess")
row("C10","Manufacturingdata generation/approval","PENDING_INPUT","Gerber/drill/CPL/order0","separateuserauthorizationandfabDFM")
row("N01","Controlledimpedance","NOT_APPLICABLE","none requested/nativecontract","do notintroduceSI/PI")
row("N02","Castellations/HDI/blindburied/newslots","NOT_APPLICABLE","notrequested/no suchobject","no specialprocessadded")
row("N03","Descriptionencoding/legacyPDFannotationasfabblock","NOT_APPLICABLE","excludedBOMauthority; historicdocumentsremain","no tools/libraryrepair")
with(p/"MANUFACTURING_PREFLIGHT_MATRIX.csv").open("w",encoding="utf8",newline="")as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
before=json.loads((p/"FROZEN_94_SOURCE_HASHES_BEFORE.json").read_text());root=p.parent/"R21_PCB_LOCAL_POUR_CLEARANCE_AND_FINAL_WARM_COLD_V1"
after={f.name:{"bytes":f.stat().st_size,"SHA256":hashlib.sha256(f.read_bytes()).hexdigest().upper()}for f in root.iterdir()if f.is_file()}
assert before==after
(p/"FROZEN_94_SOURCE_HASHES_AFTER.json").write_text(json.dumps({"all94Unchanged":True,"files":after},indent=2),encoding="utf8")
gates={"PCB_MANUFACTURING_PREFLIGHT_COMPLETE":True,"PCB_REVIEW_READY":True,"PCBGeometryScope":"existingnumericalgeometryandacceptednativeelectricalclosure;processpending","FootprintScope":"number/pitch/orientation no unconditional pad error found;factoryland/mask/stencil pending","ECO_REQUIRED":[],"MANUFACTURING_RELEASE":False,"BENCH_RELEASE":False,"PROCUREMENT_RELEASE":False,"GerberGenerated":False,"all94BaselineSourcesUnchanged":True,"status":"READONLY_PREFLIGHT_COMPLETE_PENDING_MANUFACTURING_INPUTS"}
(p/"GATES.json").write_text(json.dumps(gates,indent=2),encoding="utf8")
counts={s:sum(q["status"]==s for q in rows)for s in ["PASS","PENDING_INPUT","ECO_REQUIRED","NOT_APPLICABLE"]}
b=json.loads((p/"EXECUTION_BUDGET.json").read_text());b.update(status="READONLY_REVIEW_READY_FOR_FINAL_REVIEW",reviewPreparedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat());(p/"EXECUTION_BUDGET.json").write_text(json.dumps(b,indent=2),encoding="utf8")
text="""# COMPLETE R21 PCB MANUFACTURING PREFLIGHT READONLY RECEIPT
CIRCUIT-R21-PCB-MANUFACTURING-PREFLIGHT-READONLY-COMPLETE-20261002-01

PCB_MANUFACTURING_PREFLIGHT_COMPLETE。
本包按16号180min只读工程范围完成。PCB_REVIEW_READY基线保持；没有打开/保存/导出CAD，没有新DRC/仿真/Gerber/订单/制造/台架/上电。

## 冻结输入和真正结果
Accepted PCB commit e9c1b72f4d1659bb9a7a1dbe4a82e7937c5fe86a，actualnative722159bytes SHA C2D53B0B6BB438D7C916BE24CB0B0D6AE5C7D884E7784EEFFED90E61505BEE6C。
完整16号正文 PRO_MANUFACTURING_PREFLIGHT_RULING_FULL.md：assistant73707409-40eb-453d-bb08-37bbd07c9179，parentuserf5648be9-c6b7-4224-8bcc-833229a8fdfd。
94个15号源文件逐一SHA/size前后完全一致；不重保存“干净”PCB。15号rawPOURED微差/LINE表示差/迟记coldDRC偏差原记录不改，16号正式技术接受已保存。

几何：100×90mm四层；actual909LINE宽6mil756、12mil100、16mil7、20mil46；297VIA均hole12/pad24mil。via环.1524mm；via-holepair最小约.31115mm。既有用户铜距板边筛查：via≥2.39413mm、trace≥2.44493mm、pad≥4.06926mm。四POUR边界/keepIslandfalse及既有PNG/DRC支持未发现明显孤岛/e307避让问题，未生成工厂CAM或做完整独立铜连通证明。10mil是部分zone相关clearance，不是全板一律spacing；TrackTrack默认约.102mm、pad相关约.152mm。
这些是既有证据的几何可行性检查，不是重新载流、模拟稳定性、SI/PI或热仿真。

封装：176实际pad-number集合全部匹配native22库，550pads；U1/U2/U3/U4/U5/U7/U9/U10/U11/U12/BAT54S/J1–J4主要针数/间距/方向已列。没有证实必须修改铜/net的无条件封装错误，不能扩称全制造land/stencil资格PASS。
原生header孔J1/J4约1.1mm、J2约1.0mm、J3约1.2mm。API summary孔值尺度不同，native PAD.hole权威；polygon-pad API假孔也不当drill。没有把这种摘要差异误判ECO，没有研究内部格式/改库。
175支持的nativebody轮廓2D无相交、最小约.300002mm；U6该body对象缺支持，未证明176全部courtyard/3D/toolspace。
结构BOM176行不含Description，172有MPN，J1–J4四通用header exactmaker/MPN待定。13个既有探测候选具actualnet/具体ref.pad/坐标，PGOOD与外侧NRST、TIA0与TIA_DRV0分开；不默认可上电探测或加testpoint。

## 具体制造PENDING
1. 板厂、板厚/公差、外内铜重、材料/stackup、finish、mask颜色/公差/via处理未知；现有6mil不能任意换厚铜。
2. 40个同package padpair的mask桥估计<.10mm，集中在ADS/LM。native几何估计U5min.096774mm、U9/U10min.0900811mm。没有实际Gerber/CAM，不能声称已满足板厂mask能力。需要fab明确接受，若拒绝才集中提最小mask/land ECO；本包不修改。
3. ADS/STM/TPS当前land尺寸/定义与manufacturer示例非严格复制，图已检查/差异已列；工厂钢网、回流和无引脚封装检验方案待定。
4. J1–J4具体MPN/针截面/插头空间/pin1接线表、panel/fiducial/机械装配待定。
5. 最终制造数据与用户制造/采购/上电授权尚无，不能由本包或Pro文字代替。
旧PDF文字、Description乱码、909/911表示短段不是本包制造阻断项。不存在已证明的无条件ECO_REQUIRED；工艺拒收后才有条件ECO。

## 交付清单和证据范围
必需四文件 FABRICATION_INPUT_CONTRACT.md、ASSEMBLY_AND_TEST_ACCESS_CHECKLIST.md、MANUFACTURING_PREFLIGHT_MATRIX.csv、MANUFACTURING_OPEN_ITEMS.md；
176结构BOM/550nativepadCSV/22FPrawJSON/完整rulesJSON/实际13probeCSV/nominalbodynear-pairCSV/native mask gapCSV/analysisJSON/只读装配图；
六资料来源：JLC+ST+四冻结manufacturerPDF。ST直取HTTP567，officialwebPDF package text可读，本地PDF未下载成功且没有假SHA。既有LM p50/TPS p25/ADS p66/BAT p5渲染已实际查看。OPA/TMUX继承已接受pinmap，不额外读取第7份资料。
原官网HTML只本地留存不公开；制造datasheet原PDF已有官方链接，公开包优先短说明/资料页PNG/必要record/hash，不复制整站。Readable文件直接上传，非只ZIP/native/LFS。
只读装配图实际看过；component红mark不是生产silk认证，绿索引对应CSV；未显示完整真实mask/copper/silk/stencil，不可制造。分析使用nativepad/rotation/body和约束；API rounded pad screen保留并用native精细结果作待项。没有为了读取错误开启CAD。

## 执行
时间上限180min，existingEvidenceReview1/checklistContractBatch1/officialSources6；禁项全0。
两个普通解析脚本初失败（defaultGBK/JSON字符串未loads）保留说明并一次修正，非scientific/CAD运行。现有bundledPDF工具读取，未安装或修任何工具。
一次fresh-context whole-package终审后只允许普通文档修正；详见FINAL_REVIEW.md。不能追加review或科学重算。

制造前矩阵计数: COUNTS_PLACEHOLDER
MANUFACTURING_RELEASE=false；BENCH_RELEASE=false；PROCUREMENT_RELEASE=false。

END-OF-COMPLETE-R21-PCB-MANUFACTURING-PREFLIGHT-READONLY-RECEIPT
"""
(p/"COMPLETE_MANUFACTURING_PREFLIGHT_RECEIPT.md").write_text(text.replace("COUNTS_PLACEHOLDER",json.dumps(counts)),encoding="utf8")
(p/"IMPLEMENTATION_PLAN.md").write_text((p/"IMPLEMENTATION_PLAN.md").read_text(encoding="utf8")+"\nP0/P1/P2/P3 document batch complete; frozen94 unchanged, matrix "+json.dumps(counts)+"; no CAD or process installation. Ordinary parser encoding/json faults corrected, same read-only evidence review. One final review pending.\n",encoding="utf8")
print(json.dumps({"counts":counts,"frozen94PASS":before==after,"forbiddenActual":b["forbiddenActual"]}))

