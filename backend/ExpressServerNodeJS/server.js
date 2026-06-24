const express = require('express');
const cors = require('cors');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

// Rota de status/healthcheck
app.get('/', (req, res) => {
  res.json({
    status: 'ONLINE',
    message: 'ExpressServerNodeJS - Batcaverna unificado funcionando!',
    timestamp: new Date()
  });
});

// Mock de rotas
app.get('/api/projects', (req, res) => {
  res.json([
    { id: 1, name: 'C3PO Assistente', status: 'Active' },
    { id: 2, name: 'Pikachu Rest API', status: 'Running' }
  ]);
});

app.listen(PORT, () => {
  console.log(`Server Express rodando em http://localhost:${PORT}`);
});
