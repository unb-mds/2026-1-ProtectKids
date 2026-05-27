import { useEffect, useState } from 'react';
import { Search, Filter, ArrowRight } from 'lucide-react';
import { buscarLeis } from '../api';
import { Link } from 'react-router-dom';

export default function TodasAsLeis() {
  const [leis, setLeis] = useState([]);
  const [carregando, setCarregando] = useState(true);

  useEffect(() => {
    // Busca os dados reais do FastAPI ao abrir a página
    buscarLeis().then((dados) => {
      setLeis(dados);
      setCarregando(false);
    }).catch(err => {
      console.error("Erro ao buscar leis", err);
      setCarregando(false);
    });
  }, []);

  return (
    <div className="max-w-6xl mx-auto py-8 px-4">
      
      {/* CABEÇALHO DA PÁGINA */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-800 mb-2">Todas as Proposições Legislativas</h1>
        <p className="text-gray-600">Explore o catálogo completo de leis relacionadas à proteção infantil.</p>
      </div>

      {/* BARRA DE PESQUISA E FILTRO */}
      <div className="flex gap-4 mb-8">
        <div className="flex-grow flex items-center bg-white rounded-lg border border-gray-300 px-4 py-2 shadow-sm">
          <Search className="text-gray-400 mr-2" size={20} />
          <input 
            type="text" 
            placeholder="Buscar por título ou ementa..." 
            className="w-full outline-none bg-transparent"
          />
        </div>
        <button className="flex items-center gap-2 bg-white border border-gray-300 rounded-lg px-6 py-2 shadow-sm hover:bg-gray-50 font-medium text-gray-700">
          <Filter size={18} /> Todos os Status
        </button>
      </div>

      <p className="font-semibold text-gray-700 mb-6">{leis.length} proposições encontradas</p>

      {/* GRID DE CARDS COM DADOS DA API */}
      {carregando ? (
        <div className="text-center py-20 text-gray-500">Carregando dados da inteligência artificial...</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {leis.map((lei) => (
            <div key={lei.id_proposicao} className="bg-white rounded-xl shadow-md border border-gray-100 p-6 flex flex-col">
              
              <div className="flex justify-between items-start mb-4">
                <h2 className="text-xl font-bold text-gray-900">{lei.tipo} {lei.numero}/{lei.ano}</h2>
                <span className="text-xs font-semibold px-2 py-1 bg-yellow-100 text-yellow-800 rounded-full border border-yellow-200">
                  Em Tramitação
                </span>
              </div>
              
              {/* Etiqueta NLP da nossa IA */}
              <span className="inline-block bg-blue-50 text-blue-600 text-xs font-bold px-3 py-1 rounded w-max mb-4">
                {lei.classificacao_nlp || "Análise Pendente"}
              </span>

              <p className="text-gray-600 text-sm line-clamp-4 flex-grow mb-4">
                {lei.ementa}
              </p>

              <div className="text-xs text-gray-500 mb-4">
                <p>Apresentada em: {lei.ano}</p>
              </div>

              <Link to={`/leis/${lei.id_proposicao}`} className="w-full bg-pk-red hover:bg-red-900 text-white font-bold py-2.5 rounded flex justify-center items-center gap-2 transition text-center shadow-md">
             Ver Detalhes Completos <ArrowRight size={16} />
            </Link>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}