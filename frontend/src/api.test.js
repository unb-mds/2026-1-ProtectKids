import { beforeEach, describe, expect, it, vi } from 'vitest';

const { mockGet } = vi.hoisted(() => ({
  mockGet: vi.fn(),
}));

vi.mock('axios', () => ({
  default: {
    create: vi.fn(() => ({
      get: mockGet,
    })),
  },
}));

import {
  buscarLeiPorId,
  buscarTramitacoes,
  buscarRankingParlamentares,
  buscarRankingPartidos,
} from './api';

describe('api integration helpers', () => {
  beforeEach(() => {
    mockGet.mockReset();
  });

  it('busca detalhes por id usando o endpoint dedicado', async () => {
    const resposta = { id_proposicao: 10 };
    mockGet.mockResolvedValue({ data: resposta });

    const resultado = await buscarLeiPorId(10);

    expect(mockGet).toHaveBeenCalledWith('/proposicoes/10');
    expect(resultado).toEqual(resposta);
  });

  it('busca tramitações com id_externo e evita chamada sem id', async () => {
    mockGet.mockResolvedValue({ data: [{ orgao: 'Comissão' }] });

    const comId = await buscarTramitacoes('camara-123');
    const semId = await buscarTramitacoes();

    expect(mockGet).toHaveBeenCalledWith('/proposicoes/camara-123/tramitacoes');
    expect(comId).toEqual([{ orgao: 'Comissão' }]);
    expect(semId).toEqual([]);
    expect(mockGet).toHaveBeenCalledTimes(1);
  });

  it('normaliza total_proposicoes para total_projetos nos rankings', async () => {
    mockGet
      .mockResolvedValueOnce({ data: [{ nome: 'A', total_proposicoes: 2 }] })
      .mockResolvedValueOnce({ data: [{ partido: 'P', total_proposicoes: 3 }] });

    const parlamentares = await buscarRankingParlamentares();
    const partidos = await buscarRankingPartidos();

    expect(parlamentares[0].total_projetos).toBe(2);
    expect(partidos[0].total_projetos).toBe(3);
  });
});
