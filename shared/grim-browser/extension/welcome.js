const words = ["Private", "Calm", "Secure", "Relaxing", "Grim"];
const el = document.getElementById("word");
let i = 0;
setTimeout(function step() {
  i++;
  el.classList.remove("flick"); void el.offsetWidth;   // restart the flicker
  el.textContent = words[i];
  el.classList.add("flick");
  if (i < words.length - 1) setTimeout(step, 1100);
  else setTimeout(() => document.getElementById("after").classList.add("show"), 900);
}, 1500);
document.getElementById("go").onclick = () => { location.href = "newtab.html"; };
document.getElementById("set").onclick = () => browser.runtime.openOptionsPage();
