import { useEffect, useState } from 'react';
import { BarChart3, Award, Users } from 'lucide-react';
import { buscarRankingParlamentares, buscarRankingPartidos } from '../api';

export default function Estatisticas() {
  const [parlamentares, setParlamentares] = useState([]);
  const [partidos, setPartidos] = useState([]);
  const [carregando, setCarregando] = useState(true);

  useEffect(() => {
    // Busca os dois rankings ao mesmo tempo para otimizar o carregamento
    Promise.all([buscarRankingParlamentares(), buscarRankingPartidos()])
      .then(([dadosParlamentares, dadosPartidos]) => {
        setParlamentares(dadosParlamentares);
        setPartidos(dadosPartidos);
        setCarregando(false);
      })
      .catch((err) => {
        console.error("Erro ao carregar os rankings", err);
        setCarregando(false);
      });
  }, []);

  if (carregando) {
    return <div className="text-center py-20 text-gray-500 font-medium">Carregando painel de inteligência de dados...</div>;
  }

  return (
    <div className="flex flex-col w-full bg-gray-50 min-h-screen">
      
      {/* CABEÇALHO */}
      <section className="bg-pk-dark text-white py-12 px-8 flex justify-center shadow-inner">
        <div className="max-w-6xl w-full text-center">
          <h1 className="text-3xl md:text-4xl font-bold tracking-wide leading-tight mb-2 uppercase font-serif flex items-center justify-center gap-3">
            <BarChart3 className="text-pk-red" size={36} /> Analytics & Rankings
          </h1>
          <p className="text-gray-300 font-medium text-sm md:text-base max-w-2xl mx-auto uppercase tracking-wider">
            Monitoramento de engajamento parlamentar e partidário na proteção infantil.
          </p>
        </div>
      </section>

      {/* CONTEÚDO DOS RANKINGS */}
      <section className="py-12 px-4 max-w-6xl mx-auto w-full grid grid-cols-1 md:grid-cols-2 gap-8">
        
        {/* COLUNA 1: DEPUTADOS */}
        <div className="bg-white rounded-2xl shadow-md border border-gray-200 overflow-hidden flex flex-col">
          <div className="bg-gray-100 p-6 border-b border-gray-200 flex items-center gap-3">
            <Award className="text-yellow-600" size={28} />
            <h2 className="text-xl font-bold text-gray-900 font-serif uppercase tracking-wide">
              Top Parlamentares
            </h2>
          </div>
          
          <div className="p-6 flex-grow">
            <ul className="space-y-4">
              {parlamentares.map((deputado, index) => (
                <li key={index} className="flex items-center justify-between p-4 bg-gray-50 rounded-xl border border-gray-100 hover:border-gray-300 transition shadow-sm">
                  <div className="flex items-center gap-4">
                    <span className="text-lg font-bold text-gray-400 w-6 text-center">{index + 1}º</span>
                    <div>
                      <p className="font-bold text-gray-900 text-lg">{deputado.nome}</p>
                      <p className="text-xs font-semibold text-gray-500 uppercase tracking-wider">
                        {deputado.partido} - {deputado.uf}
                      </p>
                    </div>
                  </div>
                  <div className="flex flex-col items-end">
                    <span className="text-2xl font-black text-pk-red">{deputado.total_projetos}</span>
                    <span className="text-[10px] uppercase font-bold text-gray-400">Projetos</span>
                  </div>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* COLUNA 2: PARTIDOS */}
        <div className="bg-white rounded-2xl shadow-md border border-gray-200 overflow-hidden flex flex-col">
          <div className="bg-gray-100 p-6 border-b border-gray-200 flex items-center gap-3">
            <Users className="text-blue-600" size={28} />
            <h2 className="text-xl font-bold text-gray-900 font-serif uppercase tracking-wide">
              Engajamento por Partido
            </h2>
          </div>
          
          <div className="p-6 flex-grow">
            <ul className="space-y-4">
              {partidos.map((partido, index) => (
                <li key={index} className="flex items-center justify-between p-4 bg-gray-50 rounded-xl border border-gray-100 hover:border-gray-300 transition shadow-sm">
                  <div className="flex items-center gap-4">
                    <span className="text-lg font-bold text-gray-400 w-6 text-center">{index + 1}º</span>
                    <p className="font-bold text-gray-900 text-xl">{partido.partido}</p>
                  </div>
                  <div className="flex flex-col items-end">
                    <span className="text-2xl font-black text-blue-600">{partido.total_projetos}</span>
                    <span className="text-[10px] uppercase font-bold text-gray-400">Projetos</span>
                  </div>
                </li>
              ))}
            </ul>
          </div>
        </div>

      </section>
    </div>
  );
}