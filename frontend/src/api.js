import axios from 'axios';

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
});

export const buscarLeis = async (filtros = {}) => {
  const { data } = await api.get('/proposicoes', { params: filtros });
  return data;
};

export const buscarLeiPorId = async (id) => {
  const { data } = await api.get(`/proposicoes/${id}`);
  return data;
};

export const buscarTramitacoes = async (idExterno) => {
  if (!idExterno) {
    return [];
  }

  const { data } = await api.get(`/proposicoes/${idExterno}/tramitacoes`);
  return data;
};

export const buscarRankingParlamentares = async () => {
  const { data } = await api.get('/analytics/parlamentares/ranking');
  return data.map((item) => ({
    ...item,
    total_projetos: item.total_projetos ?? item.total_proposicoes ?? 0,
  }));
};

export const buscarRankingPartidos = async () => {
  const { data } = await api.get('/analytics/partidos/ranking');
  return data.map((item) => ({
    ...item,
    total_projetos: item.total_projetos ?? item.total_proposicoes ?? 0,
  }));
};