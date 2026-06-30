import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import {
  ArrowLeft,
  Calendar,
  Clock,
  ExternalLink,
  FileText,
  Milestone,
  ShieldCheck,
  User,
} from 'lucide-react';
import { buscarLeiPorId, buscarTramitacoes, extrairMensagemErro } from '../api';

const formatarData = (data) => {
  if (!data) {
    return 'Data não informada';
  }

  const dataObj = new Date(data);

  if (Number.isNaN(dataObj.getTime())) {
    return 'Data inválida';
  }

  return new Intl.DateTimeFormat('pt-BR').format(dataObj);
};

const formatarDataHora = (data) => {
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

const formatarOrigem = (origem) => {
  if (origem === 'Camara') {
    return 'Câmara dos Deputados';
  }

  if (origem === 'Senado') {
    return 'Senado Federal';
  }

  return 'Fonte oficial';
};

const formatarFonteClassificacao = (fonte) => {
  if (fonte === 'texto_integral') {
    return 'texto integral';
  }

  if (fonte === 'ementa') {
    return 'ementa';
  }

  return fonte || 'fonte não informada';
};

export default function DetalhesLei() {
  const { id } = useParams();
  const [lei, setLei] = useState(null);
  const [tramitacoes, setTramitacoes] = useState([]);
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState('');

  useEffect(() => {
    const carregarDetalhes = async () => {
      try {
        setCarregando(true);
        setErro('');

        const dadosLei = await buscarLeiPorId(id);
        setLei(dadosLei);

        if (dadosLei.id_externo) {
          try {
            const dadosTramitacoes = await buscarTramitacoes(dadosLei.id_externo);
            setTramitacoes(dadosTramitacoes);
          } catch {
            setTramitacoes([]);
          }
        }
      } catch (error) {
        setErro(extrairMensagemErro(error));
        setLei(null);
      } finally {
        setCarregando(false);
      }
    };

    carregarDetalhes();
  }, [id]);

  if (carregando) {
    return (
      <div className="text-center py-20 text-gray-500">
        Carregando detalhes da proposição...
      </div>
    );
  }

  if (!lei) {
    return (
      <div className="max-w-4xl mx-auto py-12 px-4 text-center">
        <h2 className="text-2xl font-bold text-gray-800 mb-4">
          Proposição não encontrada
        </h2>

        {erro && <p className="text-sm text-red-600 font-semibold mb-6">{erro}</p>}

        <Link
          to="/leis"
          className="text-[var(--color-pk-red)] hover:underline inline-flex items-center gap-2 font-semibold"
        >
          <ArrowLeft size={18} /> Voltar para a listagem
        </Link>
      </div>
    );
  }

  const nomeFonte = formatarOrigem(lei.origem);
  const estadoAtual = tramitacoes[0];
  const textoBotaoFonte = lei.origem === 'Senado' ? 'Ver no Senado' : 'Ver na Câmara';

  return (
    <div className="max-w-5xl mx-auto py-10 px-4">
      <Link
        to="/leis"
        className="text-gray-600 hover:text-[var(--color-pk-red)] inline-flex items-center gap-2 font-semibold mb-6 transition"
      >
        <ArrowLeft size={18} /> Voltar para todas as proposições
      </Link>

      <div className="bg-white rounded-2xl shadow-md border border-gray-200 p-8 mb-8">
        <div className="flex flex-wrap justify-between items-start gap-4 mb-4">
          <div>
            <div className="flex flex-wrap gap-2 mb-3">
              <span className="inline-block bg-blue-50 text-blue-600 border border-blue-100 text-xs font-bold px-3 py-1 rounded">
                {lei.classificacao_nlp || 'Não classificado'}
              </span>

              <span className="inline-block bg-gray-100 text-gray-700 border border-gray-200 text-xs font-bold px-3 py-1 rounded">
                {nomeFonte}
              </span>
            </div>

            <h1 className="text-3xl font-bold text-gray-950 font-serif">
              {lei.titulo || `${lei.tipo} ${lei.numero}/${lei.ano}`}
            </h1>
          </div>

            <span className="text-sm font-bold px-3 py-1.5 bg-blue-100 text-blue-800 rounded-full border border-blue-200 uppercase tracking-wider">
              {estadoAtual ? 'Atualizada' : 'Monitorada'}
            </span>
        </div>

        <p 
        className="text-gray-700 text-base leading-relaxed border-l-4 border-[var(--color-pk-red)] pl-4 my-6 font-medium">
          {lei.ementa}
        </p>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-4 border-t border-gray-100 text-sm text-gray-600 font-semibold">
          <div className="flex items-center gap-2">
            <Calendar size={18} className="text-gray-400" />
            <span>Apresentação: {formatarData(lei.data_apresentacao)}</span>
          </div>
          <div className="flex items-center gap-2">
            <User size={18} className="text-gray-400" />
            <span>Autor: {lei.nome_autor || `ID: ${lei.id_autor}`}</span>
          </div>
          <div className="flex items-center gap-2">
            <Milestone size={18} className="text-gray-400" />
            <span>Tema: {lei.tema || 'Proteção Infantil'}</span>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 flex flex-col gap-8">
          {lei.fonte_classificacao && (
            <div className="bg-white rounded-2xl shadow-md border border-gray-200 p-8">
              <h2 className="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2 font-serif border-b pb-2">
                <ShieldCheck size={20} className="text-blue-600" /> Justificativa da Classificação
              </h2>

              <p className="text-sm text-gray-600 mb-4">
                Classificação baseada em:{' '}
                <strong>{formatarFonteClassificacao(lei.fonte_classificacao)}</strong>
              </p>

              {lei.trecho_classificacao ? (
                <blockquote className="border-l-4 border-blue-600 pl-4 text-sm text-gray-700 italic leading-relaxed">
                  {lei.trecho_classificacao}
                </blockquote>
              ) : (
                <p className="text-sm text-gray-500">
                  Nenhum trecho de justificativa foi registrado para esta proposição.
                </p>
              )}
            </div>
          )}

          <div className="bg-white rounded-2xl shadow-md border border-gray-200 p-8">
            <h2 className="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2 font-serif border-b pb-2">
              <FileText size={20} className="text-[var(--color-pk-red)]" /> Texto da Proposição
            </h2>
                  
          {estadoAtual && (
            <div className="bg-white rounded-2xl shadow-md border border-gray-200 p-8 mb-8">
              <h2 className="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2 font-serif border-b pb-2">
                <Milestone size={20} className="text-blue-600" />
                Estado Atual da Tramitação
              </h2>

              <div className="space-y-2 text-sm text-gray-700">
                <p>
                  <strong>Órgão atual:</strong>{' '}
                  {estadoAtual.orgao || 'Órgão não informado'}
                </p>

                <p>
                  <strong>Última atualização:</strong>{' '}
                  {formatarDataHora(estadoAtual.data_hora)}
                </p>

                <p className="leading-relaxed">
                  <strong>Situação registrada:</strong>{' '}
                  {estadoAtual.descricao || 'Descrição não informada.'}
                </p>
              </div>
            </div>
          )}
            <div className="bg-gray-50 rounded-xl p-6 text-sm text-gray-800 font-mono whitespace-pre-line leading-relaxed max-h-[500px] overflow-y-auto border border-gray-200 shadow-inner">
              {lei.texto_integral || 'Texto integral não disponível para esta proposição.'}
            </div>
          </div>
        </div>

        <div className="flex flex-col gap-6">
          <div className="bg-white rounded-2xl shadow-md border border-gray-200 p-6">
            <h2 className="text-lg font-bold text-gray-900 mb-6 font-serif border-b pb-2">
              Histórico de Tramitações
            </h2>

            {tramitacoes.length ? (
              <div className="relative pl-6 border-l-2 border-blue-200 space-y-6 ml-2">
                {tramitacoes.map((tramitacao) => {
                  const chaveTramitacao = [
                    tramitacao.data_hora || 'sem-data',
                    tramitacao.orgao || 'sem-orgao',
                    tramitacao.descricao || 'sem-descricao',
                  ].join('-');

                  return (
                    <div key={chaveTramitacao} className="relative">
                      <div className="absolute -left-[31px] top-1 bg-blue-600 w-4 h-4 rounded-full border-4 border-white shadow" />

                      <h3 className="text-sm font-bold text-gray-900">
                        {tramitacao.orgao || 'Órgão não informado'}
                      </h3>

                      <p className="text-xs text-gray-500 mb-1 flex items-center gap-1">
                        <Clock size={12} /> {formatarDataHora(tramitacao.data_hora)}
                      </p>

                      <p className="text-xs text-gray-600 leading-relaxed">
                        {tramitacao.descricao || 'Descrição não informada.'}
                      </p>
                    </div>
                  );
                })}
              </div>
            ) : (
              <p className="text-sm text-gray-500">
                Nenhuma tramitação registrada para esta proposição no banco de dados.
              </p>
            )}
          </div>

          <div className="bg-white rounded-2xl shadow-md border border-gray-200 p-6 flex flex-col gap-4">
            <h3 className="font-bold text-gray-900 font-serif">Documentação Oficial</h3>
            <p className="text-xs text-gray-600 font-medium">
              Acesse o inteiro teor da matéria diretamente no portal oficial de origem:
              {' '}{nomeFonte}.
            </p>

            {lei.url_inteiro_teor ? (
              <a
                href={lei.url_inteiro_teor}
                target="_blank"
                rel="noopener noreferrer"
                className="w-full bg-[var(--color-pk-dark)] hover:bg-gray-800 text-white font-bold py-2.5 rounded flex justify-center items-center gap-2 transition text-sm shadow-md"
              >
                {textoBotaoFonte} <ExternalLink size={16} />
              </a>
            ) : (
              <p className="text-sm text-gray-500 font-medium">
                Link oficial não disponível.
              </p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}