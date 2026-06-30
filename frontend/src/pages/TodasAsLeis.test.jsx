import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { describe, expect, it, vi } from 'vitest';
import TodasAsLeis from './TodasAsLeis';

vi.mock('../api', () => ({
  buscarLeis: vi.fn().mockResolvedValue([
    {
      id_proposicao: 1,
      id_externo: 'camara-1',
      titulo: 'PL 123/2026',
      origem: 'Camara',
      ementa: 'Dispõe sobre segurança digital para crianças e adolescentes.',
      classificacao_nlp: 'Cyberbullying e Crimes Virtuais',
      data_apresentacao: '2026-06-23',
      nome_autor: 'Deputada Exemplo',
      partido_autor: 'ABC',
      uf_autor: 'DF',
    },
  ]),
  extrairMensagemErro: vi.fn(() => 'Erro ao carregar dados da API.'),
}));

describe('TodasAsLeis', () => {
  it('renderiza proposições retornadas pela API', async () => {
    render(
      <MemoryRouter>
        <TodasAsLeis />
      </MemoryRouter>
    );

    expect(await screen.findByText('PL 123/2026')).toBeTruthy();
    expect(screen.getByText('Cyberbullying e Crimes Virtuais')).toBeTruthy();
    expect(screen.getByText('Monitorada')).toBeTruthy();
  });
});
