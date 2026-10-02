const s=await eda.sys_FileManager.getDocumentSource();return {head:s.slice(0,600),padCount:(await eda.pcb_PrimitivePad.getAll()).length};
