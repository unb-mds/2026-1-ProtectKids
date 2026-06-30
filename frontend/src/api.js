import axios from 'axios';

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
});

export const buscarLeis = async (filtros = {}) => {
  const { data } = await api.get('/proposicoes', {
    params: filtros,
  });

  return data;
};

export const buscarLeiPorId = async (id) => {
  const { data } = await api.get(`/proposicoes/${id}`);
  return data;
};

export const buscarTramitacoes = async (idExterno) => {
  const { data } = await api.get(`/proposicoes/${idExterno}/tramitacoes`);
  return data;
};

export const buscarRankingParlamentares = async (filtros = {}) => {
  const { data } = await api.get('/analytics/parlamentares/ranking', {
    params: filtros,
  });

  return data;
};

export const buscarRankingPartidos = async (filtros = {}) => {
  const { data } = await api.get('/analytics/partidos/ranking', {
    params: filtros,
  });

  return data;
};

export const buscarNuvemPalavras = async (filtros = {}) => {
  const { data } = await api.get('/analytics/nuvem-palavras', {
    params: filtros,
  });

  return data;
};

export const extrairMensagemErro = (error) => {
  return error.response?.data?.detail || 'Erro ao carregar dados da API.';
};