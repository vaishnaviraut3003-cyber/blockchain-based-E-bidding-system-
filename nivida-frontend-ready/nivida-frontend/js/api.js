async function apiGet(endpoint){
  const res = await fetch(API_BASE_URL + endpoint);
  if(!res.ok) throw new Error("GET "+endpoint+" failed");
  return res.json();
}
async function apiPost(endpoint, body){
  const res = await fetch(API_BASE_URL + endpoint,{
    method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)
  });
  if(!res.ok) throw new Error("POST "+endpoint+" failed");
  return res.json();
}
async function apiPut(endpoint, body){
  const res = await fetch(API_BASE_URL + endpoint,{
    method:"PUT",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)
  });
  if(!res.ok) throw new Error("PUT "+endpoint+" failed");
  return res.json();
}

const DEMO_TENDERS=[
 {id:"T-001",title:"Construction of New College Building",department:"PWD",type:"Works",deadline:"25 Sep 2026",status:"Open",description:"Construction and associated civil works for a new college building."},
 {id:"T-002",title:"Supply of Electrical Equipment",department:"PWD",type:"Goods",deadline:"28 Sep 2026",status:"Open",description:"Supply of electrical equipment according to the tender specification."},
 {id:"T-003",title:"Road Repair and Maintenance",department:"PWD",type:"Works",deadline:"30 Sep 2026",status:"Open",description:"Road repair and maintenance works."},
 {id:"T-004",title:"IT Infrastructure Setup",department:"NIC",type:"Services",deadline:"05 Oct 2026",status:"Upcoming",description:"IT infrastructure setup and support."},
 {id:"T-005",title:"Office Furniture Supply",department:"PWD",type:"Goods",deadline:"12 Aug 2026",status:"Closed",description:"Supply of office furniture."}
];

async function getTenders(){
  try{
    const data=await apiGet(API_ENDPOINTS.tenders);
    return Array.isArray(data)?data:(data.tenders||DEMO_TENDERS);
  }catch(e){return DEMO_TENDERS;}
}
