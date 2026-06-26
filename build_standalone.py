"""
Monta app/standalone.html — versão única e autossuficiente do SPA para publicar
como Artifact (CSP bloqueia CDN/hosts externos):
  - inlina app/data.js no HTML
  - remove o <script> do SheetJS (CDN)
  - injeta um gerador de .xlsx em JS puro (zip 'stored' + CRC32), sem dependências
"""
from pathlib import Path
BASE = Path("C:/Users/IIA/Documents/hackathon-azzas")
html = (BASE/"app/index.html").read_text(encoding="utf-8")
data = (BASE/"app/data.js").read_text(encoding="utf-8")

# 1. remover script do SheetJS (CDN) — bloqueado pelo CSP do Artifact
html = html.replace(
    '<script src="https://cdn.sheetjs.com/xlsx-0.20.1/package/dist/xlsx.full.min.js"></script>\n', '')

# 2. inlinar data.js
html = html.replace('<script src="data.js"></script>',
                    '<script>\n'+data+'\n</script>')

# 3. gerador de xlsx puro JS (zip stored + CRC32) — substitui exportXlsx()
XLSX_WRITER = r"""
<script>
/* Gerador de .xlsx em JS puro — zip 'stored' (sem compressão) + CRC32. Sem dependências. */
(function(){
  var CRC=(function(){var t=[],c,n,k;for(n=0;n<256;n++){c=n;for(k=0;k<8;k++)c=c&1?0xEDB88320^(c>>>1):c>>>1;t[n]=c>>>0;}return t;})();
  function crc32(bytes){var c=0xFFFFFFFF;for(var i=0;i<bytes.length;i++)c=CRC[(c^bytes[i])&0xFF]^(c>>>8);return (c^0xFFFFFFFF)>>>0;}
  function strBytes(s){return new TextEncoder().encode(s);}
  function esc(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
  function colRef(n){var s='';n++;while(n>0){var m=(n-1)%26;s=String.fromCharCode(65+m)+s;n=(n-m-1)/26;}return s;}
  function sheetXml(rows){
    var x='<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'+
      '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetData>';
    rows.forEach(function(row,ri){
      x+='<row r="'+(ri+1)+'">';
      row.forEach(function(v,ci){
        var ref=colRef(ci)+(ri+1);
        if(typeof v==='number'&&isFinite(v)) x+='<c r="'+ref+'"><v>'+v+'</v></c>';
        else x+='<c r="'+ref+'" t="inlineStr"><is><t>'+esc(v)+'</t></is></c>';
      });
      x+='</row>';
    });
    return x+'</sheetData></worksheet>';
  }
  function zip(files){
    var enc=[],cen=[],off=0;
    function u16(n){return [n&255,(n>>8)&255];}
    function u32(n){return [n&255,(n>>8)&255,(n>>16)&255,(n>>24)&255];}
    files.forEach(function(f){
      var nameB=strBytes(f.name), dataB=f.data, crc=crc32(dataB);
      var local=[].concat(u32(0x04034b50),u16(20),u16(0),u16(0),u16(0),u16(0),
        u32(crc),u32(dataB.length),u32(dataB.length),u16(nameB.length),u16(0));
      enc.push(new Uint8Array(local),nameB,dataB);
      var cent=[].concat(u32(0x02014b50),u16(20),u16(20),u16(0),u16(0),u16(0),u16(0),
        u32(crc),u32(dataB.length),u32(dataB.length),u16(nameB.length),u16(0),u16(0),u16(0),u16(0),u32(0),u32(off));
      cen.push(new Uint8Array(cent),nameB);
      off+=local.length+nameB.length+dataB.length;
    });
    var cenStart=off,cenLen=0;cen.forEach(function(a){cenLen+=a.length;});
    var end=[].concat(u32(0x06054b50),u16(0),u16(0),u16(files.length),u16(files.length),u32(cenLen),u32(cenStart),u16(0));
    var parts=enc.concat(cen,[new Uint8Array(end)]),total=0;parts.forEach(function(p){total+=p.length;});
    var out=new Uint8Array(total),p=0;parts.forEach(function(a){out.set(a,p);p+=a.length;});
    return out;
  }
  window.makeXlsx=function(rows){
    var files=[
      {name:'[Content_Types].xml',data:strBytes('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/><Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/></Types>')},
      {name:'_rels/.rels',data:strBytes('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>')},
      {name:'xl/workbook.xml',data:strBytes('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets><sheet name="distribuicao" sheetId="1" r:id="rId1"/></sheets></workbook>')},
      {name:'xl/_rels/workbook.xml.rels',data:strBytes('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/></Relationships>')},
      {name:'xl/worksheets/sheet1.xml',data:strBytes(sheetXml(rows))}
    ];
    return zip(files);
  };
})();
</script>
"""

# substitui a função exportXlsx por uma que usa makeXlsx (sempre disponível offline)
old_export = """function exportXlsx(){
  const rows=dd.map(r=>({FILIAL:r.filial,PRODUTO:r.produto,COR_PRODUTO:r.cor,TAMANHO:r.tamanho,QTD_DISTRIBUIR:r.qtd}));
  if(window.XLSX){const ws=XLSX.utils.json_to_sheet(rows);const wb=XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb,ws,'distribuicao');XLSX.writeFile(wb,'distribuicao_inv26.xlsx');
    showToast('Arquivo distribuicao_inv26.xlsx exportado');}
  else{ // fallback CSV
    const head='FILIAL,PRODUTO,COR_PRODUTO,TAMANHO,QTD_DISTRIBUIR\\n';
    const body=rows.map(r=>`${r.FILIAL},${r.PRODUTO},${r.COR_PRODUTO},${r.TAMANHO},${r.QTD_DISTRIBUIR}`).join('\\n');
    const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([head+body],{type:'text/csv'}));
    a.download='distribuicao_inv26.csv';a.click();showToast('xlsx indisponível offline — exportado CSV');}
}"""
new_export = """function exportXlsx(){
  const header=['FILIAL','PRODUTO','COR_PRODUTO','TAMANHO','QTD_DISTRIBUIR'];
  const rows=[header].concat(dd.map(r=>[r.filial,r.produto,r.cor,r.tamanho,r.qtd]));
  const bytes=window.makeXlsx(rows);
  const a=document.createElement('a');
  a.href=URL.createObjectURL(new Blob([bytes],{type:'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'}));
  a.download='distribuicao_inv26.xlsx';a.click();
  showToast('Arquivo distribuicao_inv26.xlsx exportado');
}"""
assert old_export in html, "bloco exportXlsx não encontrado"
html = html.replace(old_export, new_export)

# injeta o writer antes de </body>
html = html.replace('</body>', XLSX_WRITER+'\n</body>')

(BASE/"app/standalone.html").write_text(html, encoding="utf-8")
print("OK -> app/standalone.html  (", len(html), "bytes )")
