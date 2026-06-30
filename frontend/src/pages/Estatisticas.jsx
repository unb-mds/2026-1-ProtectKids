import { useEffect, useMemo, useState } from 'react';
import { BarChart3, Award, Users, PieChart as PieChartIcon } from 'lucide-react';
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';
import {
  buscarLeis,
  buscarRankingParlamentares,
  buscarRankingPartidos,
  extrairMensagemErro,
} from '../api';

const CORES_GRAFICO = ['#2563EB', '#FACC15', '#0038A8', '#60A5FA', '#FF7A1A', '#16A34A'];

const SUBTEMAS_IGNORADOS = [
  'Simbólico/Ruído',
  'Simbólico',
  'Ruído',
  'Nao classificado',
  'Não classificado',
];

const formatarNomeSubtema = (nome) => {
  const mapa = {
    'Cyberbullying e Crimes Virtuais': 'Cyberbullying',
    'Violência e Abuso': 'Violência e Abuso',
    'Adoção e Orfanatos': 'Adoção e Orfanatos',
    'Educação e Cultura': 'Educação e Cultura',
  };

  return mapa[nome] || nome;
};

const gerarDadosSubtemas = (proposicoes) => {
  const contagem = {};

  proposicoes.forEach((proposicao) => {
    const chave = String(
      proposicao.classificacao_nlp || proposicao.subtema || 'Não classificado'
    ).trim();

    if (SUBTEMAS_IGNORADOS.includes(chave)) {
      return;
    }

    contagem[chave] = (contagem[chave] || 0) + 1;
  });

  return Object.entries(contagem)
    .map(([nome, quantidade]) => ({
      nome: formatarNomeSubtema(nome),
      quantidade,
    }))
    .sort((a, b) => b.quantidade - a.quantidade);
};

export default function Estatisticas() {
  const [parlamentares, setParlamentares] = useState([]);
  const [partidos, setPartidos] = useState([]);
  const [proposicoes, setProposicoes] = useState([]);
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState('');

  useEffect(() => {
    const carregarDados = async () => {
      try {
        setCarregando(true);
        setErro('');

        const [dadosParlamentares, dadosPartidos, todasAsProposicoes] =
          await Promise.all([
            buscarRankingParlamentares({ limit: 10 }),
            buscarRankingPartidos({ limit: 10 }),
            buscarLeis({ limit: 200 }),
          ]);

        setParlamentares(dadosParlamentares);
        setPartidos(dadosPartidos);
        setProposicoes(todasAsProposicoes);
      } catch (error) {
        setErro(extrairMensagemErro(error));
      } finally {
        setCarregando(false);
      }
    };

    carregarDados();
  }, []);

  const dadosSubtemas = useMemo(
    () => gerarDadosSubtemas(proposicoes),
    [proposicoes]
  );

  if (carregando) {
    return (
      <div className="text-center py-20 text-gray-500 font-medium">
        Carregando painel de inteligência de dados...
      </div>
    );
  }

  return (
    <div className="flex flex-col w-full bg-[#E5E5E5] min-h-screen pb-12">
      <section className="bg-[#FACC15] text-[#001B5E] py-10 px-8 flex justify-center shadow-inner mb-8">
        <div className="max-w-6xl w-full text-center">
          <h1 className="text-3xl md:text-4xl font-black tracking-wide leading-tight mb-2 uppercase font-serif flex items-center justify-center gap-3">
            <BarChart3 className="text-[#0038A8]" size={36} /> Dashboard Analítico
          </h1>
          <p className="text-black font-bold text-sm md:text-base max-w-2xl mx-auto uppercase tracking-wider">
            Monitoramento de volume de proposições e engajamento legislativo.
          </p>
        </div>
      </section>

      <div className="max-w-6xl mx-auto w-full px-4 flex flex-col gap-8">
        {erro && (
          <div className="bg-red-50 border border-red-300 text-red-700 rounded-xl p-4 font-bold">
            {erro}
          </div>
        )}

        <div className="bg-white rounded-2xl shadow-md border border-gray-200 overflow-hidden w-full">
          <div className="bg-gray-100 p-6 border-b border-gray-200 flex items-center gap-3">
            <PieChartIcon className="text-[#0038A8]" size={28} />
            <h2 className="text-xl font-bold text-gray-900 font-serif uppercase tracking-wide">
              Volume de Proposições por Subtema (NLP)
            </h2>
          </div>

          <div className="p-6 h-[430px] w-full">
            {dadosSubtemas.length ? (
              <ResponsiveContainer width="100%" height="100%">
                <BarChart
                  data={dadosSubtemas}
                  margin={{ top: 20, right: 30, left: 0, bottom: 80 }}
                >
                  <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E5E7EB" />
                  <XAxis
                    dataKey="nome"
                    interval={0}
                    angle={-18}
                    textAnchor="end"
                    height={85}
                    tick={{ fill: '#4B5563', fontSize: 11 }}
                    axisLine={false}
                    tickLine={false}
                  />
                  <YAxis
                    allowDecimals={false}
                    tick={{ fill: '#4B5563' }}
                    axisLine={false}
                    tickLine={false}
                  />
                  <Tooltip
                    cursor={{ fill: '#F3F4F6' }}
                    contentStyle={{
                      borderRadius: '8px',
                      border: 'none',
                      boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
                    }}
                  />
                  <Bar dataKey="quantidade" name="Proposições" radius={[4, 4, 0, 0]}>
                    {dadosSubtemas.map((item, index) => (
                      <Cell key={`${item.nome}-${index}`} fill={CORES_GRAFICO[index % CORES_GRAFICO.length]} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-full flex items-center justify-center text-gray-500 font-medium">
                Nenhum dado de subtema disponível.
              </div>
            )}
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div className="bg-white rounded-2xl shadow-md border border-gray-200 overflow-hidden flex flex-col">
            <div className="bg-gray-100 p-6 border-b border-gray-200 flex items-center gap-3">
              <Award className="text-yellow-600" size={28} />
              <h2 className="text-xl font-bold text-gray-900 font-serif uppercase tracking-wide">
                Top Parlamentares
              </h2>
            </div>

            <div className="p-6 flex-grow">
              {parlamentares.length ? (
                <ul className="space-y-4">
                  {parlamentares.map((parlamentar, index) => (
                    <li
                      key={`${parlamentar.nome}-${parlamentar.partido}-${parlamentar.uf}`}
                      className="flex items-center justify-between p-4 bg-gray-50 rounded-xl border border-gray-100 hover:border-gray-300 transition shadow-sm"
                    >
                      <div className="flex items-center gap-4">
                        <span className="text-lg font-bold text-gray-400 w-6 text-center">
                          {index + 1}º
                        </span>
                        <div>
                          <p className="font-bold text-gray-900 text-lg">
                            {parlamentar.nome}
                          </p>
                          <p className="text-xs font-semibold text-gray-500 uppercase tracking-wider">
                            {parlamentar.partido || 'ND'} - {parlamentar.uf || 'ND'}
                          </p>
                        </div>
                      </div>
                      <div className="flex flex-col items-end">
                        <span className="text-2xl font-black text-pk-red">
                          {parlamentar.total_proposicoes}
                        </span>
                        <span className="text-[10px] uppercase font-bold text-gray-400">
                          Proposições
                        </span>
                      </div>
                    </li>
                  ))}
                </ul>
              ) : (
                <p className="text-gray-500 font-medium">Nenhum parlamentar encontrado.</p>
              )}
            </div>
          </div>

          <div className="bg-white rounded-2xl shadow-md border border-gray-200 overflow-hidden flex flex-col">
            <div className="bg-gray-100 p-6 border-b border-gray-200 flex items-center gap-3">
              <Users className="text-blue-600" size={28} />
              <h2 className="text-xl font-bold text-gray-900 font-serif uppercase tracking-wide">
                Engajamento por Partido
              </h2>
            </div>

            <div className="p-6 flex-grow">
              {partidos.length ? (
                <ul className="space-y-4">
                  {partidos.map((partido, index) => (
                    <li
                      key={`${partido.partido}-${index}`}
                      className="flex items-center justify-between p-4 bg-gray-50 rounded-xl border border-gray-100 hover:border-gray-300 transition shadow-sm"
                    >
                      <div className="flex items-center gap-4">
                        <span className="text-lg font-bold text-gray-400 w-6 text-center">
                          {index + 1}º
                        </span>
                        <p className="font-bold text-gray-900 text-xl">
                          {partido.partido || 'ND'}
                        </p>
                      </div>
                      <div className="flex flex-col items-end">
                        <span className="text-2xl font-black text-blue-600">
                          {partido.total_proposicoes}
                        </span>
                        <span className="text-[10px] uppercase font-bold text-gray-400">
                          Proposições
                        </span>
                      </div>
                    </li>
                  ))}
                </ul>
              ) : (
                <p className="text-gray-500 font-medium">Nenhum partido encontrado.</p>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}