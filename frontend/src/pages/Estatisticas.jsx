import { criarSlugCategoria } from '../constants/categoriasNlp';
import { useNavigate } from 'react-router-dom';
import { useEffect, useMemo, useState } from 'react';
import {
  Award,
  BarChart3,
  PieChart as PieChartIcon,
  Users,
} from 'lucide-react';
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
  buscarRankingParlamentares,
  buscarRankingPartidos,
  buscarSubtemas,
  extrairMensagemErro,
} from '../api';

const CORES_GRAFICO = [
  '#2563EB',
  '#FACC15',
  '#0038A8',
  '#60A5FA',
  '#FF7A1A',
  '#16A34A',
];

const formatarNomeSubtema = (nome) => {
  const mapa = {
    'Cyberbullying e Crimes Virtuais': 'Cyberbullying',
    'Exploração Sexual Online e Aliciamento Digital': 'Exploração Online',
    'Proteção de Dados e Privacidade Infantil': 'Dados e Privacidade',
    'Redes Sociais e Plataformas Digitais': 'Redes e Plataformas',
    'Conteúdo Nocivo e Segurança Online': 'Conteúdo Nocivo',
    'Educação Digital e Cidadania Online': 'Educação Digital',
    'Atuação Legislativa e Fiscalização': 'Atuação Legislativa',
    'Proteção Geral no Ambiente Digital': 'Proteção Geral Digital',
  };

  return mapa[nome] || nome || 'Não classificado';
};

export default function Estatisticas() {
  const [parlamentares, setParlamentares] = useState([]);
  const [partidos, setPartidos] = useState([]);
  const [subtemas, setSubtemas] = useState([]);
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState('');
  const navigate = useNavigate();
  useEffect(() => {
    const carregarDados = async () => {
      try {
        setCarregando(true);
        setErro('');

        const [dadosParlamentares, dadosPartidos, dadosSubtemas] =
          await Promise.all([
            buscarRankingParlamentares({ limit: 10 }),
            buscarRankingPartidos({ limit: 10 }),
            buscarSubtemas({ limit: 10 }),
          ]);

        setParlamentares(Array.isArray(dadosParlamentares) ? dadosParlamentares : []);
        setPartidos(Array.isArray(dadosPartidos) ? dadosPartidos : []);
        setSubtemas(Array.isArray(dadosSubtemas) ? dadosSubtemas : []);
      } catch (error) {
        setErro(extrairMensagemErro(error));
      } finally {
        setCarregando(false);
      }
    };

    carregarDados();
  }, []);

    const dadosSubtemas = useMemo(() => {
      return subtemas.map((item) => ({
        nome: formatarNomeSubtema(item.nome),
        nomeOriginal: item.nome,
        quantidade: item.total_proposicoes || 0,
        percentual: item.percentual || 0,
      }));
    }, [subtemas]);

  if (carregando) {
    return (
      <div className="min-h-[60vh] flex items-center justify-center bg-[#E5E5E5] text-[#001B5E] font-bold">
        Carregando painel de estatísticas...
      </div>
    );
  }

  return (
    <div className="flex flex-col w-full bg-[#E5E5E5] min-h-screen pb-12">
      <section className="bg-[#FACC15] text-[#001B5E] py-10 px-8 flex justify-center shadow-inner mb-8">
        <div className="max-w-6xl w-full text-center">
          <h1 className="text-3xl md:text-4xl font-black tracking-wide leading-tight mb-2 uppercase font-serif flex items-center justify-center gap-3">
            <BarChart3 className="text-[#0038A8]" size={36} />
            Dashboard Analítico
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
          <div className="bg-gray-100 p-6 border-b border-gray-200 flex items-start gap-3">
            <PieChartIcon className="text-[#0038A8] mt-1" size={28} />

            <div>
              <h2 className="text-xl font-bold text-gray-900 font-serif uppercase tracking-wide">
                Volume de Proposições por Subtema
              </h2>

              <p className="text-xs text-gray-500 font-bold uppercase mt-1">
                Clique em uma barra para entender quais temas entram em cada categoria.
              </p>
            </div>
          </div>

          <div className="p-6 h-[430px] w-full">
            {dadosSubtemas.length ? (
              <ResponsiveContainer width="100%" height="100%">
                <BarChart
                  data={dadosSubtemas}
                  margin={{ top: 20, right: 30, left: 0, bottom: 80 }}
                >
                  <CartesianGrid
                    strokeDasharray="3 3"
                    vertical={false}
                    stroke="#E5E7EB"
                  />

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
                    formatter={(value, name, props) => {
                      const percentual = props.payload?.percentual || 0;
                      return [`${value} proposições (${percentual}%)`, 'Total'];
                    }}
                    contentStyle={{
                      borderRadius: '8px',
                      border: 'none',
                      boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
                    }}
                  />

                  <Bar
                    dataKey="quantidade"
                    name="Proposições"
                    radius={[4, 4, 0, 0]}
                    cursor="pointer"
                    onClick={(data) => {
                      const nomeCategoria =
                        data?.payload?.nomeOriginal || data?.nomeOriginal || data?.nome;

                      if (nomeCategoria) {
                        navigate(`/estatisticas/subtema/${criarSlugCategoria(nomeCategoria)}`);
                      }
                    }}
                  >
                    {dadosSubtemas.map((item, index) => {
                      const chaveSubtema = item.nomeOriginal || item.nome;

                      return (
                        <Cell
                          key={`grafico-subtema-${chaveSubtema}`}
                          fill={CORES_GRAFICO[index % CORES_GRAFICO.length]}
                        />
                      );
                    })}
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
                            {parlamentar.nome || 'Nome não informado'}
                          </p>

                          <p className="text-xs font-semibold text-gray-500 uppercase tracking-wider">
                            {parlamentar.partido || 'ND'} -{' '}
                            {parlamentar.uf || 'ND'}
                          </p>
                        </div>
                      </div>

                      <div className="flex flex-col items-end">
                        <span className="text-2xl font-black text-[#D61F26]">
                          {parlamentar.total_proposicoes || 0}
                        </span>

                        <span className="text-[10px] uppercase font-bold text-gray-400">
                          Proposições
                        </span>
                      </div>
                    </li>
                  ))}
                </ul>
              ) : (
                <p className="text-gray-500 font-medium">
                  Nenhum parlamentar encontrado.
                </p>
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
                  {partidos.map((partido, index) => {
                    const siglaPartido = partido.partido || 'ND';

                    return (
                      <li
                        key={`ranking-partido-${siglaPartido}`}
                        className="flex items-center justify-between p-4 bg-gray-50 rounded-xl border border-gray-100 hover:border-gray-300 transition shadow-sm"
                      >
                        <div className="flex items-center gap-4">
                          <span className="text-lg font-bold text-gray-400 w-6 text-center">
                            {index + 1}º
                          </span>

                          <p className="font-bold text-gray-900 text-xl">
                            {siglaPartido}
                          </p>
                        </div>

                        <div className="flex flex-col items-end">
                          <span className="text-2xl font-black text-blue-600">
                            {partido.total_proposicoes || 0}
                          </span>

                          <span className="text-[10px] uppercase font-bold text-gray-400">
                            Proposições
                          </span>
                        </div>
                      </li>
                    );
                  })}
                </ul>
              ) : (
                <p className="text-gray-500 font-medium">
                  Nenhum partido encontrado.
                </p>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}