import { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import {
  ArrowLeft,
  BookOpen,
  FileText,
  Lightbulb,
  Search,
  Tags,
} from 'lucide-react';
import { buscarLeis, extrairMensagemErro } from '../api';
import { obterCategoriaPorSlug } from '../constants/categoriasNlp';

const formatarData = (data) => {
  if (!data) return 'Data não informada';

  const dataObj = new Date(data);

  if (Number.isNaN(dataObj.getTime())) {
    return 'Data inválida';
  }

  return new Intl.DateTimeFormat('pt-BR').format(dataObj);
};

export default function DetalhesSubtema() {
  const { slug } = useParams();
  const categoria = obterCategoriaPorSlug(slug);

  const [proposicoes, setProposicoes] = useState([]);
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState('');

  useEffect(() => {
    const carregarProposicoes = async () => {
      if (!categoria) {
        setCarregando(false);
        return;
      }

      try {
        setCarregando(true);
        setErro('');

        const dados = await buscarLeis({
          tema_nlp: categoria.nome,
          limit: 30,
        });

        setProposicoes(Array.isArray(dados) ? dados : []);
      } catch (error) {
        setErro(extrairMensagemErro(error));
      } finally {
        setCarregando(false);
      }
    };

    carregarProposicoes();
  }, [categoria]);

  if (!categoria) {
    return (
      <div className="min-h-screen bg-[#E5E5E5] px-6 py-12">
        <div className="max-w-5xl mx-auto bg-white rounded-2xl border border-gray-200 p-8 shadow-md">
          <Link
            to="/estatisticas"
            className="inline-flex items-center gap-2 text-[#0038A8] font-bold mb-6 hover:underline"
          >
            <ArrowLeft size={18} />
            Voltar para Estatísticas
          </Link>

          <h1 className="text-2xl font-black text-gray-900 font-serif">
            Categoria não encontrada
          </h1>

          <p className="mt-3 text-gray-600">
            Não foi possível localizar uma explicação cadastrada para este subtema.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#E5E5E5]">
      <section className="bg-[#FACC15] px-6 md:px-12 py-8">
        <div className="max-w-7xl mx-auto">
          <Link
            to="/estatisticas"
            className="inline-flex items-center gap-2 text-[#001B5E] font-black mb-5 hover:underline"
          >
            <ArrowLeft size={18} />
            Voltar para Estatísticas
          </Link>

          <h1 className="font-serif text-3xl md:text-4xl font-black uppercase text-[#001B5E]">
            {categoria.titulo}
          </h1>

          <p className="mt-3 max-w-4xl text-sm md:text-base font-bold text-black leading-relaxed">
            {categoria.resumo}
          </p>
        </div>
      </section>

      <main className="max-w-7xl mx-auto px-6 md:px-12 py-10 space-y-8">
        {erro && (
          <div className="bg-red-50 border border-red-300 text-red-700 rounded-xl p-4 font-bold">
            {erro}
          </div>
        )}

        <section className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="bg-white rounded-2xl border border-gray-200 shadow-md p-6">
            <div className="flex items-center gap-2 mb-4">
              <BookOpen className="text-[#0038A8]" size={24} />
              <h2 className="font-serif text-xl font-black text-gray-900">
                O que entra aqui?
              </h2>
            </div>

            <ul className="space-y-3 text-sm text-gray-700 font-medium">
              {categoria.inclui.map((item) => (
                <li key={item} className="flex gap-2">
                  <span className="text-[#0038A8] font-black">•</span>
                  <span>{item}</span>
                </li>
              ))}
            </ul>
          </div>

          <div className="bg-white rounded-2xl border border-gray-200 shadow-md p-6">
            <div className="flex items-center gap-2 mb-4">
              <Tags className="text-[#FF7A1A]" size={24} />
              <h2 className="font-serif text-xl font-black text-gray-900">
                Palavras-chave
              </h2>
            </div>

            <div className="flex flex-wrap gap-2">
              {categoria.palavrasChave.map((palavra) => (
                <span
                  key={palavra}
                  className="bg-blue-50 text-[#0038A8] border border-blue-100 rounded-full px-3 py-1 text-xs font-black"
                >
                  {palavra}
                </span>
              ))}
            </div>
          </div>

          <div className="bg-white rounded-2xl border border-gray-200 shadow-md p-6">
            <div className="flex items-center gap-2 mb-4">
              <Lightbulb className="text-yellow-600" size={24} />
              <h2 className="font-serif text-xl font-black text-gray-900">
                Exemplos
              </h2>
            </div>

            <ul className="space-y-3 text-sm text-gray-700 font-medium">
              {categoria.exemplos.map((item) => (
                <li key={item} className="flex gap-2">
                  <span className="text-yellow-600 font-black">•</span>
                  <span>{item}</span>
                </li>
              ))}
            </ul>
          </div>
        </section>

        <section className="bg-white rounded-2xl border border-gray-200 shadow-md overflow-hidden">
          <div className="bg-gray-100 border-b border-gray-200 p-6 flex items-center justify-between gap-4">
            <div className="flex items-center gap-3">
              <FileText className="text-[#0038A8]" size={26} />
              <div>
                <h2 className="font-serif text-xl font-black text-gray-900 uppercase">
                  Proposições classificadas neste subtema
                </h2>
                <p className="text-sm text-gray-500 font-medium">
                  Dados filtrados pelo backend usando a classificação NLP.
                </p>
              </div>
            </div>

            <span className="bg-[#0038A8] text-white rounded-full px-4 py-2 text-sm font-black">
              {proposicoes.length}
            </span>
          </div>

          <div className="p-6">
            {carregando ? (
              <div className="text-center text-gray-500 font-bold py-10">
                Carregando proposições...
              </div>
            ) : proposicoes.length ? (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
                {proposicoes.map((proposicao) => (
                  <article
                    key={proposicao.id_externo}
                    className="border border-gray-200 rounded-xl p-5 bg-gray-50 hover:bg-white hover:shadow-md transition"
                  >
                    <div className="flex flex-wrap gap-2 mb-3">
                      <span className="bg-[#FACC15] text-[#111827] rounded-full px-3 py-1 text-xs font-black">
                        {proposicao.titulo}
                      </span>

                      <span className="bg-blue-100 text-blue-700 rounded-full px-3 py-1 text-xs font-black">
                        {proposicao.origem === 'Camara'
                          ? 'Câmara'
                          : proposicao.origem || 'Fonte'}
                      </span>
                    </div>

                    <p className="text-sm text-gray-800 leading-relaxed font-medium">
                      {proposicao.ementa?.length > 220
                        ? `${proposicao.ementa.slice(0, 220)}...`
                        : proposicao.ementa}
                    </p>

                    <div className="mt-4 text-xs text-gray-600 space-y-1">
                      <p>
                        <strong>Autor:</strong>{' '}
                        {proposicao.nome_autor || 'Autor desconhecido'}
                      </p>

                      <p>
                        <strong>Data:</strong>{' '}
                        {formatarData(proposicao.data_apresentacao)}
                      </p>
                    </div>

                    <Link
                      to={`/leis/${proposicao.id_proposicao}`}
                      className="mt-4 inline-flex items-center gap-2 bg-[#FF7A1A] hover:bg-[#EA580C] text-white rounded-md px-4 py-2 text-xs font-black transition"
                    >
                      <Search size={14} />
                      Ver detalhes
                    </Link>
                  </article>
                ))}
              </div>
            ) : (
              <div className="text-center text-gray-500 font-bold py-10">
                Nenhuma proposição encontrada para este subtema.
              </div>
            )}
          </div>
        </section>
      </main>
    </div>
  );
}