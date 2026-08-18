const form=document.getElementById("productionForm");
const dateInput=document.getElementById("date");
const message=document.getElementById("message");

dateInput.value=new Date().toISOString().slice(0,10);

form.addEventListener("submit",(e)=>{
  e.preventDefault();
  const record={
    DATE:dateInput.value,
    LINE_ID:document.getElementById("line").value,
    FO:document.getElementById("fo").value.trim(),
    TIME_SLOT:document.getElementById("timeSlot").value,
    OUTPUT_QTY:Number(document.getElementById("outputQty").value),
    TIMESTAMP:new Date().toISOString()
  };

  if(!record.DATE||!record.LINE_ID||!record.FO||!record.TIME_SLOT||Number.isNaN(record.OUTPUT_QTY)){
    showMessage("กรุณากรอกข้อมูลให้ครบ","error");
    return;
  }

  const rows=JSON.parse(localStorage.getItem("production_output")||"[]");
  rows.push(record);
  localStorage.setItem("production_output",JSON.stringify(rows));

  showMessage("บันทึกยอดผลิตเรียบร้อย","success");
  document.getElementById("outputQty").value="";
});

function showMessage(text,type){
  message.textContent=text;
  message.className=`message ${type}`;
}
