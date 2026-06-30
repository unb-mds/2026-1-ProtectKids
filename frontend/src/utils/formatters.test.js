import { describe, expect, it } from 'vitest';
import {
  formatarData,
  formatarDataHora,
  formatarOrigemCurta,
  formatarOrigemCompleta,
  formatarFonteClassificacao,
  resumirTexto,
} from './formatters';

describe('formatters', () => {
  it('formata datas e trata valores inválidos', () => {
    expect(formatarData('2026-06-23')).toMatch(/22|23/);
    expect(formatarData()).toBe('Data não informada');
    expect(formatarData('data-invalida')).toBe('Data inválida');
    expect(formatarDataHora()).toBe('Data não informada');
    expect(formatarDataHora('data-invalida')).toBe('Data inválida');
    expect(formatarDataHora('2026-06-23T10:30:00')).toContain('10:30');
  });

  it('formata origens e fonte de classificação', () => {
    expect(formatarOrigemCurta('Camara')).toBe('Câmara');
    expect(formatarOrigemCurta('Senado')).toBe('Senado');
    expect(formatarOrigemCurta()).toBe('Fonte não informada');
    expect(formatarOrigemCompleta('Camara')).toBe('Câmara dos Deputados');
    expect(formatarOrigemCompleta('Senado')).toBe('Senado Federal');
    expect(formatarOrigemCompleta('Outro')).toBe('Fonte oficial');
    expect(formatarFonteClassificacao('texto_integral')).toBe('texto integral');
    expect(formatarFonteClassificacao('ementa')).toBe('ementa');
    expect(formatarFonteClassificacao()).toBe('fonte não informada');
  });

  it('resume textos longos e preserva textos curtos', () => {
    expect(resumirTexto()).toBe('Ementa não disponível.');
    expect(resumirTexto('Texto curto', 100)).toBe('Texto curto');
    expect(resumirTexto('Texto muito grande para ser exibido completo', 10)).toBe('Texto muit...');
  });
});
