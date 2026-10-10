async function connectWallet(){
  if(!window.ethereum){alert("MetaMask is not installed. Install MetaMask first.");return null;}
  try{
    const accounts=await window.ethereum.request({method:"eth_requestAccounts"});
    const account=accounts[0];
    localStorage.setItem("walletAddress",account);
    alert("MetaMask connected:\n"+account);
    return account;
  }catch(e){alert("MetaMask connection cancelled.");}
}
async function sha256(text){
  const data=new TextEncoder().encode(text);
  const hash=await crypto.subtle.digest("SHA-256",data);
  return [...new Uint8Array(hash)].map(b=>b.toString(16).padStart(2,"0")).join("");
}
