import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { ArrowLeft, Calendar, FileText, ExternalLink, Milestone, User } from 'lucide-react';
import { buscarLeiPorId } from '../api';

export default function DetalhesLei() {
  const { id } = useParams();
  const [lei, setLei] = useState(null);
  const [carregando, setCarregando] = useState(true);

  useEffect(() => {
    buscarLeiPorId(id).then((dados) => {
      setLei(dados);
      setCarregando(false);
    }).catch(err => {
      console.error("Erro ao buscar detalhes da lei", err);
      setCarregando(false);
    });
  }, [id]);

  if (carregando) {
    return <div className="text-center py-20 text-gray-500">Carregando detalhes da proposição...</div>;
  }

  if (!lei) {
    return (
      <div className="max-w-4xl mx-auto py-12 px-4 text-center">
        <h2 className="text-2xl font-bold text-gray-800 mb-4">Proposição não encontrada</h2>
        <Link to="/leis" className="text-pk-red hover:underline inline-flex items-center gap-2 font-semibold">
          <ArrowLeft size={18} /> Voltar para a listagem
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-5xl mx-auto py-10 px-4">
      
      {/* Botão Voltar */}
      <Link to="/leis" className="text-gray-600 hover:text-pk-red inline-flex items-center gap-2 font-semibold mb-6 transition">
        <ArrowLeft size={18} /> Voltar para todas as leis
      </Link>

      {/* CABEÇALHO */}
      <div className="bg-white rounded-2xl shadow-md border border-gray-200 p-8 mb-8">
        <div className="flex flex-wrap justify-between items-start gap-4 mb-4">
          <div>
            <span className="inline-block bg-blue-50 text-blue-600 border border-blue-100 text-xs font-bold px-3 py-1 rounded mb-2">
              {lei.classificacao_nlp}
            </span>
            <h1 className="text-3xl font-bold text-gray-950 font-serif">{lei.tipo} {lei.numero}/{lei.ano}</h1>
          </div>
          <span className="text-sm font-bold px-3 py-1.5 bg-yellow-100 text-yellow-800 rounded-full border border-yellow-200 uppercase tracking-wider">
            Em Tramitação
          </span>
        </div>
        
        <p className="text-gray-700 text-base leading-relaxed border-l-4 border-pk-red pl-4 my-6 font-medium">
          {lei.ementa}
        </p>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-4 border-t border-gray-100 text-sm text-gray-600 font-semibold">
          <div className="flex items-center gap-2">
            <Calendar size={18} className="text-gray-400" />
            <span>Apresentação: {new Date(lei.data_apresentacao).toLocaleDateString('pt-BR')}</span>
          </div>
          <div className="flex items-center gap-2">
            <User size={18} className="text-gray-400" />
            <span>Autor: {lei.nome_autor || `ID: ${lei.id_autor}`}</span>
          </div>
          <div className="flex items-center gap-2">
            <Milestone size={18} className="text-gray-400" />
            <span>Tema: {lei.tema}</span>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* COLUNA DA ESQUERDA: TEXTO INTEGRAL */}
        <div className="lg:col-span-2 flex flex-col gap-8">
          
          {/* Bloco do Texto Jurídico */}
          <div className="bg-white rounded-2xl shadow-md border border-gray-200 p-8">
            <h2 className="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2 font-serif border-b pb-2">
              <FileText size={20} className="text-pk-red" /> Texto da Proposição
            </h2>
            <div className="bg-gray-50 rounded-xl p-6 text-sm text-gray-800 font-mono whitespace-pre-line leading-relaxed max-h-[500px] overflow-y-auto border border-gray-200 shadow-inner">
              {lei.texto_integral}
            </div>
          </div>
        </div>

        {/* COLUNA DA DIREITA: LINHA DO TEMPO E LINKS */}
        <div className="flex flex-col gap-6">
          
          {/* Linha do Tempo Visual */}
          <div className="bg-white rounded-2xl shadow-md border border-gray-200 p-6">
            <h2 className="text-lg font-bold text-gray-900 mb-6 font-serif border-b pb-2">
              Status de Tramitação
            </h2>
            
            <div className="relative pl-6 border-l-2 border-blue-200 space-y-6 ml-2">
              
              {/* Ponto 1: Atual */}
              <div className="relative">
                <div className="absolute -left-[31px] top-1 bg-blue-600 w-4 h-4 rounded-full border-4 border-white shadow"></div>
                <h3 className="text-sm font-bold text-gray-900">Análise de IA (NLP) Concluída</h3>
                <p className="text-xs text-gray-500 mb-1">Classificado como: {lei.classificacao_nlp}</p>
              </div>

              {/* Ponto 2: Apresentação */}
              <div className="relative">
                <div className="absolute -left-[31px] top-1 bg-blue-400 w-4 h-4 rounded-full border-4 border-white shadow"></div>
                <h3 className="text-sm font-bold text-gray-800">Proposição Apresentada</h3>
                <p className="text-xs text-gray-500">Data: {new Date(lei.data_apresentacao).toLocaleDateString('pt-BR')}</p>
                <p className="text-xs text-gray-500">Enviado para a Mesa Diretora</p>
              </div>

            </div>
          </div>

          {/* Documento Original */}
          <div className="bg-white rounded-2xl shadow-md border border-gray-200 p-6 flex flex-col gap-4">
            <h3 className="font-bold text-gray-900 font-serif">Documentação Oficial</h3>
            <p className="text-xs text-gray-600 font-medium">Acesse a página original do inteiro teor da matéria diretamente no portal da Câmara dos Deputados.</p>
            <a 
              href={lei.url_inteiro_teor} 
              target="_blank" 
              rel="noopener noreferrer" 
              className="w-full bg-pk-dark hover:bg-gray-800 text-white font-bold py-2.5 rounded flex justify-center items-center gap-2 transition text-sm shadow-md"
            >
              Ver na Câmara <ExternalLink size={16} />
            </a>
          </div>

        </div>
      </div>

    </div>
  );
}