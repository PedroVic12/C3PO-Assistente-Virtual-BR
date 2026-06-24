/* app/static/js/App.js */
async function checkApi() {
  try {
    const r = await fetch('/api/health');
    const j = await r.json();
    document.getElementById('apiStatus').textContent = j.status === 'healthy' ? 'API Online' : 'API Offline';
  } catch (e) {
    document.getElementById('apiStatus').textContent = 'Erro ao conectar API';
  }
}

async function loadExamples() {
  try {
    const r = await fetch('/api/examples');
    const j = await r.json();
    const root = document.getElementById('tableRoot');
    if (j.success && j.data.length) {
      let html = '<table class="w-full text-left"><thead><tr><th>ID</th><th>Nome</th><th>Descrição</th></tr></thead><tbody>';
      html += j.data.map(it=>`<tr><td class="pr-4">${it.id}</td><td class="pr-4">${it.name}</td><td>${it.description||''}</td></tr>`).join('');
      html += '</tbody></table>';
      root.innerHTML = html;
    } else {
      root.innerHTML = '<div class="text-gray-500">Nenhum exemplo</div>';
    }
  } catch (e) {
    console.error(e);
    document.getElementById('tableRoot').innerHTML = '<div class="text-red-500">Erro ao carregar.</div>';
  }
}

document.addEventListener('DOMContentLoaded', ()=>{
  checkApi();
  document.getElementById('btnLoad').addEventListener('click', loadExamples);
  document.getElementById('btnNew').addEventListener('click', async ()=>{
    const name = prompt('Nome:');
    if (!name) return;
    await fetch('/api/examples', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({name, description: 'Criado via UI'})});
    loadExamples();
  });
});
