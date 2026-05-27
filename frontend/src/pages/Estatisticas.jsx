import { useEffect, useState } from 'react';
import { BarChart3, Award, Users, PieChart as PieChartIcon } from 'lucide-react';
import { buscarRankingParlamentares, buscarRankingPartidos, buscarLeis } from '../api';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Cell } from 'recharts';

export default function Estatisticas() {
  const [parlamentares, setParlamentares] = useState([]);
  const [partidos, setPartidos] = useState([]);
  const [dadosSubtemas, setDadosSubtemas] = useState([]);
  const [carregando, setCarregando] = useState(true);

  // Paleta de cores para o gráfico
  const coresGrafico = ['#8B0000', '#2563EB', '#16A34A', '#D97706', '#9333EA', '#0891B2'];

  useEffect(() => {
    // Busca os rankings e TODAS as leis simultaneamente
    Promise.all([buscarRankingParlamentares(), buscarRankingPartidos(), buscarLeis()])
      .then(([dadosParlamentares, dadosPartidos, todasAsLeis]) => {
        setParlamentares(dadosParlamentares);
        setPartidos(dadosPartidos);

        // Lógica para processar o RF05: Volume por Subtema / Classificação NLP
        const contagemTemas = todasAsLeis.reduce((acc, lei) => {
          const tema = lei.classificacao_nlp || 'Não Classificado';
          acc[tema] = (acc[tema] || 0) + 1;
          return acc;
        }, {});

        // Converte o objeto em um array compatível com o Recharts e ordena do maior pro menor
        const graficoFormatado = Object.keys(contagemTemas)
          .map(tema => ({
            nome: tema,
            quantidade: contagemTemas[tema]
          }))
          .sort((a, b) => b.quantidade - a.quantidade);

        setDadosSubtemas(graficoFormatado);
        setCarregando(false);
      })
      .catch((err) => {
        console.error("Erro ao carregar os dados do dashboard", err);
        setCarregando(false);
      });
  }, []);

  if (carregando) {
    return <div className="text-center py-20 text-gray-500 font-medium">Carregando painel de inteligência de dados...</div>;
  }

  return (
    <div className="flex flex-col w-full bg-gray-50 min-h-screen pb-12">
      
      {/* CABEÇALHO */}
      <section className="bg-pk-dark text-white py-12 px-8 flex justify-center shadow-inner mb-8">
        <div className="max-w-6xl w-full text-center">
          <h1 className="text-3xl md:text-4xl font-bold tracking-wide leading-tight mb-2 uppercase font-serif flex items-center justify-center gap-3">
            <BarChart3 className="text-pk-red" size={36} /> Dashboard Analítico
          </h1>
          <p className="text-gray-300 font-medium text-sm md:text-base max-w-2xl mx-auto uppercase tracking-wider">
            Monitoramento de volume de proposições e engajamento legislativo.
          </p>
        </div>
      </section>

      <div className="max-w-6xl mx-auto w-full px-4 flex flex-col gap-8">
        
        {/* RF05: DASHBOARD INTERATIVO DE VOLUME POR SUBTEMA */}
        <div className="bg-white rounded-2xl shadow-md border border-gray-200 overflow-hidden w-full">
          <div className="bg-gray-100 p-6 border-b border-gray-200 flex items-center gap-3">
            <PieChartIcon className="text-pk-dark" size={28} />
            <h2 className="text-xl font-bold text-gray-900 font-serif uppercase tracking-wide">
              Volume de Proposições por Subtema (NLP)
            </h2>
          </div>
          <div className="p-6 h-[400px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={dadosSubtemas} margin={{ top: 20, right: 30, left: 0, bottom: 20 }}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E5E7EB" />
                <XAxis dataKey="nome" tick={{ fill: '#4B5563', fontSize: 12 }} axisLine={false} tickLine={false} />
                <YAxis allowDecimals={false} tick={{ fill: '#4B5563' }} axisLine={false} tickLine={false} />
                <Tooltip 
                  cursor={{ fill: '#F3F4F6' }}
                  contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)' }}
                />
                <Bar dataKey="quantidade" name="Proposições" radius={[4, 4, 0, 0]}>
                  {dadosSubtemas.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={coresGrafico[index % coresGrafico.length]} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* RANKINGS (RF06 e RF07) */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          
          {/* RF06: RANKING DE DEPUTADOS */}
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

          {/* RF07: RANKING DE PARTIDOS */}
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

        </div>
      </div>
    </div>
  );
}