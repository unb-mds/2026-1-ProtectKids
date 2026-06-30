import { render, screen } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import App from './App';

vi.mock('./api', () => ({
  buscarTodasLeisPaginadas: vi.fn().mockResolvedValue([]),
  buscarNuvemPalavras: vi.fn().mockResolvedValue([]),
  buscarRankingParlamentares: vi.fn().mockResolvedValue([]),
  buscarRankingPartidos: vi.fn().mockResolvedValue([]),
  buscarLeis: vi.fn().mockResolvedValue([]),
  buscarLeiPorId: vi.fn().mockResolvedValue(null),
  buscarTramitacoes: vi.fn().mockResolvedValue([]),
  extrairMensagemErro: vi.fn(() => 'Erro ao carregar dados da API.'),
}));

describe('Aplicação ProtectKids', () => {
  it('renderiza a estrutura principal sem quebrar', () => {
    render(<App />);

    expect(screen.getAllByText('Protect').length).toBeGreaterThan(0);
    expect(screen.getByText('Início')).toBeTruthy();
    expect(screen.getByText('Todas as Leis')).toBeTruthy();
  });
});
