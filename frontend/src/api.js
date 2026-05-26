import axios from 'axios';

export const api = axios.create({
  baseURL: 'http://localhost:8000', // A porta do backend Docker
});

export const buscarLeis = async (filtros = {}) => {
  const { data } = await api.get('/proposicoes', { params: filtros });
  return data;
};

export const buscarLeiPorId = async (id) => {
  const { data } = await api.get('/proposicoes');
  // Filtra a lei correspondente pelo id_proposicao
  return data.find(lei => lei.id_proposicao === parseInt(id));
};