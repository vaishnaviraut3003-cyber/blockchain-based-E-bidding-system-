document.addEventListener("DOMContentLoaded",()=>{
  const path=location.pathname.toLowerCase();
  document.querySelectorAll(".sidebar a[data-page]").forEach(a=>{
    if((a.dataset.page==="dashboard"&&path.endsWith("dashboard.html"))||
       (a.dataset.page==="tenders"&&(path.endsWith("tenders.html")||path.endsWith("create-tender.html")||path.endsWith("tender-details.html")))||
       (a.dataset.page==="bids"&&(path.endsWith("place-bid.html")||path.endsWith("my-bids.html")))||
       (a.dataset.page==="audit"&&(path.endsWith("audit.html")||path.endsWith("verification.html")))||
       (a.dataset.page==="reports"&&path.endsWith("reports.html"))) a.style.background="#123a5e";
  });
});
function showHelp(){alert("Nivida Help: use the navigation to create tenders, submit bids and verify bid hashes.");}
