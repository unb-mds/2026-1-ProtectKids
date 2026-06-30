export const CORES_GRAFICO = [
  '#2563EB',
  '#FACC15',
  '#0038A8',
  '#60A5FA',
  '#FF7A1A',
  '#16A34A',
];

export const SUBTEMAS_IGNORADOS = [
  'Simbólico/Ruído',
  'Simbólico',
  'Ruído',
  'Nao classificado',
  'Não classificado',
];

export const PALAVRAS_IGNORADAS = [
  'criança',
  'crianca',
  'crianças',
  'criancas',
  'adolescente',
  'adolescentes',
  'infantil',
  'infantis',
  'proteção',
  'protecao',
  'proteger',
  'direito',
  'direitos',
];

export const TAMANHO_PAGINA_API = 200;
export const LIMITE_ANALYTICS_FRONTEND = 1000;

export function formatarNomeSubtema(nome) {
  const mapa = {
    'Cyberbullying e Crimes Virtuais': 'Cyberbullying',
    'Violência e Abuso': 'Violência e Abuso',
    'Adoção e Orfanatos': 'Adoção e Orfanatos',
    'Adoção e Orfandade': 'Adoção e Orfanatos',
    'Educação e Cultura': 'Educação e Cultura',
    'Proteção Geral': 'Proteção Geral',
    'Articulação Estratégica': 'Articulação Estratégica',
  };

  return mapa[nome] || nome;
}

export function deveIgnorarSubtema(subtema) {
  const valor = String(subtema || '').trim();
  return SUBTEMAS_IGNORADOS.includes(valor);
}

export function calcularVolumePorSubtema(proposicoes) {
  const contagem = {};

  proposicoes.forEach((item) => {
    const chave = String(
      item.classificacao_nlp || item.subtema || 'Não classificado'
    ).trim();

    if (deveIgnorarSubtema(chave)) {
      return;
    }

    contagem[chave] = (contagem[chave] || 0) + 1;
  });

  return Object.entries(contagem)
    .map(([nome, total]) => ({
      nome: formatarNomeSubtema(nome),
      total,
    }))
    .sort((a, b) => b.total - a.total)
    .slice(0, 8);
}

export function gerarDadosSubtemas(proposicoes) {
  return calcularVolumePorSubtema(proposicoes).map((item) => ({
    nome: item.nome,
    quantidade: item.total,
  }));
}

export function prepararPalavrasNuvem(palavras) {
  return palavras
    .filter((item) => {
      const texto = String(item.text || '')
        .trim()
        .toLowerCase();

      return texto && !PALAVRAS_IGNORADAS.includes(texto);
    })
    .sort((a, b) => b.value - a.value)
    .slice(0, 24);
}
