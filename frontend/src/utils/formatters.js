export const formatarData = (data) => {
  if (!data) {
    return 'Data não informada';
  }

  const dataObj = new Date(data);

  if (Number.isNaN(dataObj.getTime())) {
    return 'Data inválida';
  }

  return new Intl.DateTimeFormat('pt-BR').format(dataObj);
};

export const formatarDataHora = (data) => {
  if (!data) {
    return 'Data não informada';
  }

  const dataObj = new Date(data);

  if (Number.isNaN(dataObj.getTime())) {
    return 'Data inválida';
  }

  return new Intl.DateTimeFormat('pt-BR', {
    dateStyle: 'short',
    timeStyle: 'short',
  }).format(dataObj);
};

export const formatarOrigemCurta = (origem) => {
  if (origem === 'Camara') {
    return 'Câmara';
  }

  if (origem === 'Senado') {
    return 'Senado';
  }

  return origem || 'Fonte não informada';
};

export const formatarOrigemCompleta = (origem) => {
  if (origem === 'Camara') {
    return 'Câmara dos Deputados';
  }

  if (origem === 'Senado') {
    return 'Senado Federal';
  }

  return 'Fonte oficial';
};

export const formatarFonteClassificacao = (fonte) => {
  if (fonte === 'texto_integral') {
    return 'texto integral';
  }

  if (fonte === 'ementa') {
    return 'ementa';
  }

  return fonte || 'fonte não informada';
};

export const resumirTexto = (texto, limite = 180) => {
  if (!texto) {
    return 'Ementa não disponível.';
  }

  if (texto.length <= limite) {
    return texto;
  }

  return `${texto.slice(0, limite).trim()}...`;
};
