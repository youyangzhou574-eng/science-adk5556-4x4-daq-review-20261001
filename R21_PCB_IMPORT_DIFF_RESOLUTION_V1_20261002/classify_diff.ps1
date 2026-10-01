$root = $PSScriptRoot
$sch = Get-Content -Raw -LiteralPath "$root\..\R21_PCB_FLOORPLAN_AND_LAYOUT_V1\ACCEPTED_SCHEMATIC_JLC_NETLIST.json" | ConvertFrom-Json
$byRef = @{}
foreach ($c in $sch.components.PSObject.Properties) { $byRef[$c.Value.props.Designator] = $c.Value }
$map = @{'值'='Value'; '通道ID'='Channel ID'; '名称'='Name'; '制造商'='Manufacturer'; '制造商编号'='Manufacturer Part'; '供应商'='Supplier'; '供应商封装'='Supplier Footprint'; '立创元件名'='LCSC Part Name'; '描述'='Description'; '嘉立创库类别'='JLCPCB Part Class'; '容差'='Tolerance'; '数据手册'='Datasheet'}
$rows = Import-Csv -LiteralPath "$root\IMPORT_CHANGE_DIFF.csv" -Delimiter "`t"
$out = foreach ($r in $rows) {
 if (-not $r.动作) { continue }
 $ref, $field = $r.对象 -split ':',2
 $key = if ($map.ContainsKey($field)) {$map[$field]} else {$field}
 $c = $byRef[$ref]
 $expected = $c.props.PSObject.Properties[$key]
 $value = if ($expected) {[string]$expected.Value} else {''}
 $match = $c -and ($value -ceq [string]$r.导入后)
 [pscustomobject]@{Action=$r.动作; Object=$r.对象; Before=$r.导入前; After=$r.导入后; SourceProperty=$key; AcceptedSourceAfter=$value; SourceMatch=[bool]$match; Classification=if (-not $match) {'REVIEW_REQUIRED'} elseif ($r.导入前 -and -not $r.导入后) {'HISTORICAL_LIBRARY_METADATA_RESIDUE_SOURCE_SYNC'} else {'ACCEPTABLE_PROPERTY_SYNC'}; ChangesConnectivity=$false; ChangesFootprint=$false}
}
$out | Export-Csv -NoTypeInformation -Encoding utf8 -LiteralPath "$root\IMPORT_CHANGE_CLASSIFICATION.csv"
$summary = [ordered]@{UTC=(Get-Date).ToUniversalTime().ToString('o'); RawRows=$rows.Count; ComponentGroupRows=@($rows | Where-Object {-not $_.动作}).Count; Changes=$out.Count; Actions=@($out | Group-Object Action | Select-Object Name,Count); Classifications=@($out | Group-Object Classification | Select-Object Name,Count); SourceMismatch=@($out | Where-Object {-not $_.SourceMatch}).Count; NonPropertyActions=@($out | Where-Object {$_.Action -notin @('新增属性','修改属性')}).Count; Decision='Only decide one sync after SourceMismatch and NonPropertyActions both zero; no pin/net/footprint/component change listed. ADC library description losses are metadata only; retain original evidence; no manufacturing release.'}
$summary | ConvertTo-Json -Depth 6 | Set-Content -Encoding utf8 -LiteralPath "$root\IMPORT_DIFF_CLASSIFICATION_SUMMARY.json"
$summary | ConvertTo-Json -Depth 6
$out | Where-Object {-not $_.SourceMatch} | Select-Object -First 10 | ConvertTo-Json

