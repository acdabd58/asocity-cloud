let uid = localStorage.getItem("uid");
if (!uid) {
  uid = "id-" + Math.random().toString(36).substring(2, 10);
  localStorage.setItem("uid", uid);
}
document.getElementById("uid-display").innerText = "Your ID: " + uid;

function depositPoints() {
  const amount = parseFloat(prompt("Deposit amount:"));
  fetch("/api/deposit", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_id: uid, amount })
  }).then(res => res.json()).then(alertResponse);
}

function withdrawPoints() {
  const amount = parseFloat(prompt("Withdraw amount:"));
  fetch("/api/withdraw", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_id: uid, amount })
  }).then(res => res.json()).then(alertResponse);
}

function transferPoints() {
  const to = prompt("Receiver ID:");
  const amount = parseFloat(prompt("Amount:"));
  fetch("/api/transfer", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ from: uid, to, amount })
  }).then(res => res.json()).then(alertResponse);
}

function viewServerBalance() {
  const key = prompt("Enter admin key:");
  fetch("/api/server-balance", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ key })
  }).then(res => res.json()).then(alertResponse);
}

function alertResponse(res) {
  alert(JSON.stringify(res));
}
