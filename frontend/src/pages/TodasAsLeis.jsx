import { useEffect, useMemo, useState } from 'react';
import { Link } from 'react-router-dom';
import { Search, SlidersHorizontal } from 'lucide-react';
import { buscarLeis, extrairMensagemErro } from '../api';

const formatarData = (data) => {
  if (!data) return 'Data não informada';

  return new Intl.DateTimeFormat('pt-BR').format(new Date(data));
};

const formatarOrigem = (origem) => {
  if (origem === 'Camara') return 'Câmara';
  return origem || 'Fonte não informada';
};

export default function TodasAsLeis() {
  const [leis, setLeis] = useState([]);
  const [busca, setBusca] = useState('');
  const [origem, setOrigem] = useState('');
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState('');

  useEffect(() => {
    const carregarLeis = async () => {
      try {
        setCarregando(true);
        setErro('');

        const dados = await buscarLeis({
          limit: 200,
          origem: origem || undefined,
        });

        setLeis(dados);
      } catch (error) {
        setErro(extrairMensagemErro(error));
      } finally {
        setCarregando(false);
      }
    };

    carregarLeis();
  }, [origem]);

  const leisFiltradas = useMemo(() => {
    const termo = busca.trim().toLowerCase();

    if (!termo) return leis;

    return leis.filter((lei) => {
      return [
        lei.titulo,
        lei.ementa,
        lei.nome_autor,
        lei.classificacao_nlp,
        lei.partido_autor,
        lei.uf_autor,
      ]
        .filter(Boolean)
        .some((campo) => String(campo).toLowerCase().includes(termo));
    });
  }, [busca, leis]);

  return (
    <div className="bg-[#E5E5E5] min-h-screen">
      <section className="bg-[#FACC15] px-6 md:px-12 py-5">
        <div className="max-w-7xl mx-auto">
          <h1 className="font-serif text-3xl md:text-4xl font-black uppercase text-[#001B5E]">
            Todas as Proposições Legislativas
          </h1>

          <p className="mt-1 text-sm font-bold text-black">
            Explore o catálogo completo de leis relacionadas à proteção infantil
            e combate ao cyberbullying.
          </p>
        </div>
      </section>

      <section className="max-w-7xl mx-auto px-6 md:px-12 py-5">
        <div className="bg-white px-5 py-4 shadow-sm">
          <div className="flex flex-col md:flex-row gap-4">
            <label className="flex-1 bg-[#EEF2F7] rounded-full px-5 py-3 flex items-center gap-3">
              <Search size={18} className="text-gray-500" />
              <input
                value={busca}
                onChange={(event) => setBusca(event.target.value)}
                placeholder="Buscar por título, ementa ou autor..."
                className="bg-transparent outline-none w-full text-sm font-bold text-gray-700 placeholder:text-gray-500"
              />
            </label>

            <label className="bg-[#EEF2F7] rounded-md px-4 py-3 flex items-center gap-2">
              <SlidersHorizontal size={18} />
              <select
                value={origem}
                onChange={(event) => setOrigem(event.target.value)}
                className="bg-transparent outline-none text-sm font-bold text-gray-700"
              >
                <option value="">Todas as Fontes</option>
                <option value="Camara">Câmara</option>
                <option value="Senado">Senado</option>
              </select>
            </label>
          </div>

          <p className="mt-3 text-sm font-bold text-gray-700">
            {leisFiltradas.length} proposições encontradas
          </p>
        </div>
      </section>

      <section className="max-w-7xl mx-auto px-6 md:px-12 py-10">
        {erro && (
          <div className="bg-red-50 border border-red-300 text-red-700 rounded-xl p-4 font-bold mb-6">
            {erro}
          </div>
        )}

        {carregando ? (
          <div className="bg-white rounded-xl p-10 text-center font-bold text-gray-500">
            Carregando proposições...
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-10">
            {leisFiltradas.map((lei) => (
              <article
                key={lei.id_externo}
                className="bg-white border border-gray-400 rounded-xl p-4 shadow-sm hover:shadow-lg transition"
              >
                <div className="flex items-start justify-between gap-3 mb-2">
                  <h2 className="font-serif font-black text-lg text-black">
                    {lei.titulo}
                  </h2>

                  <span className="text-[10px] bg-[#FEF3C7] border border-[#FACC15] text-[#92400E] rounded-full px-2 py-1 font-bold">
                    Em Tramitação
                  </span>
                </div>

                <div className="flex flex-wrap gap-2 mb-3">
                  <span className="text-[10px] bg-blue-100 text-blue-700 rounded px-2 py-1 font-bold">
                    {formatarOrigem(lei.origem)}
                  </span>

                  {lei.classificacao_nlp && (
                    <span className="text-[10px] bg-[#DBEAFE] text-[#0038A8] rounded px-2 py-1 font-bold">
                      {lei.classificacao_nlp}
                    </span>
                  )}
                </div>

                <p className="text-xs text-gray-800 leading-relaxed min-h-[72px]">
                  {lei.ementa?.length > 180
                    ? `${lei.ementa.slice(0, 180)}...`
                    : lei.ementa}
                </p>

                <div className="mt-4 text-xs text-gray-700 leading-relaxed">
                  <p>
                    Apresentada em{' '}
                    <strong>{formatarData(lei.data_apresentacao)}</strong>
                  </p>
                  <p>
                    {lei.nome_autor || 'Autor desconhecido'} -{' '}
                    {lei.partido_autor || 'ND'}/{lei.uf_autor || 'ND'}
                  </p>
                </div>

                <Link
                  to={`/leis/${lei.id_proposicao}`}
                  className="mt-4 block w-full text-center bg-[#FF7A1A] hover:bg-[#EA580C] text-white rounded-md py-2 text-xs font-black transition"
                >
                  Ver Detalhes Completos →
                </Link>
              </article>
            ))}
          </div>
        )}
      </section>
    </div>
  );
}