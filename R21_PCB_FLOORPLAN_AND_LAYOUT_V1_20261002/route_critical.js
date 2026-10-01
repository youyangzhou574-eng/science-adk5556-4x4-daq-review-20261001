const pr=await eda.dmt_Project.getCurrentProjectInfo();if(pr.uuid!=='e58f223d256cd14d13a6fb04a0e150585301864f01c50827f9241f5945cf2801')throw Error('Wrong copy');await eda.dmt_EditorControl.openDocument('268e6597399ebcce');
const nets=['VCM_DRV','VCM_FB','VEXC_DRV','VEXC_FB'];for(let i=0;i<4;i++)nets.push('ROW_DRV'+i,'ROW_FB'+i,'COL_SENSE'+i,'TIA_DRV'+i);
const result=await eda.pcb_Document.autoRouting({RoutingNets:nets,layers:[1],existingPrimitiveMode:'keep',optimization:1});
return {requestedNets:nets,result,lines:(await eda.pcb_PrimitiveLine.getAll()).length,polylines:(await eda.pcb_PrimitivePolyline.getAll()).length,saved:await eda.pcb_Document.save()};
