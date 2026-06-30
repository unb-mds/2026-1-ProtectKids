import { render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import NuvemPalavras from './NuvemPalavras';

describe('NuvemPalavras', () => {
  it('renderiza estado vazio', () => {
    render(<NuvemPalavras palavras={[]} />);

    expect(screen.getByText('Nenhuma palavra disponível.')).toBeTruthy();
  });

  it('renderiza palavras recebidas pela API', () => {
    render(
      <NuvemPalavras
        palavras={[
          { text: 'internet', value: 12 },
          { text: 'segurança', value: 8 },
        ]}
      />
    );

    expect(screen.getByText('internet')).toBeTruthy();
    expect(screen.getByText('segurança')).toBeTruthy();
  });
});
