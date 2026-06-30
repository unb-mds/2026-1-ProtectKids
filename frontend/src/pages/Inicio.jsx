import { useEffect, useMemo, useState } from 'react';
import { Link } from 'react-router-dom';
import {
  Bar,
  BarChart,
  Cell,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';
import {
  buscarLeis,
  buscarNuvemPalavras,
  buscarRankingParlamentares,
  buscarRankingPartidos,
  extrairMensagemErro,
} from '../api';
import NuvemPalavras from '../components/NuvemPalavras';
import DashboardBox from '../components/DashboardBox';

const cores = ['#2563EB', '#FACC15', '#0038A8', '#60A5FA', '#FF7A1A', '#16A34A'];
const SUBTEMAS_IGNORADOS = [
  'Simbólico/Ruído',
  'Simbólico',
  'Ruído',
  'Nao classificado',
  'Não classificado',
];
const PALAVRAS_IGNORADAS = [
  'criança',
  'crianca',
  'adolescente',
  'adolescente',
  'infantil',
  'proteção',
  'protecao',
];
function formatarNomeSubtema(nome) {
  const mapa = {
    'Cyberbullying e Crimes Virtuais': 'Cyberbullying',
    'Violência e Abuso': 'Violência e Abuso',
    'Adoção e Orfandade': 'Adoção e Orfandade',
    'Educação e Cultura': 'Educação e Cultura',
  };

  return mapa[nome] || nome;
}
function calcularVolumePorSubtema(proposicoes) {
  const contagem = {};

  proposicoes.forEach((item) => {
    const chaveBruta =
      item.classificacao_nlp || item.subtema || 'Não classificado';

    const chave = String(chaveBruta).trim();

    if (SUBTEMAS_IGNORADOS.includes(chave)) {
      return;
    }

    contagem[chave] = (contagem[chave] || 0) + 1;
  });

  return Object.entries(contagem)
    .map(([nome, total]) => ({
      nome: formatarNomeSubtema(nome),
      total,
    }))
    .sort((a, b) => b.total - a.total)
    .slice(0, 8);
}
function prepararPalavrasNuvem(palavras) {
  return palavras
    .filter((item) => {
      const texto = String(item.text || '')
        .trim()
        .toLowerCase();

      return texto && !PALAVRAS_IGNORADAS.includes(texto);
    })
    .sort((a, b) => b.value - a.value)
    .slice(0, 24);
}
export default function Inicio() {
  const [proposicoes, setProposicoes] = useState([]);
  const [palavras, setPalavras] = useState([]);
  const [parlamentares, setParlamentares] = useState([]);
  const [partidos, setPartidos] = useState([]);
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState('');
  const palavrasNuvem = useMemo(() => {
  return prepararPalavrasNuvem(palavras);
}, [palavras]);

  useEffect(() => {
    const carregarDados = async () => {
      try {
        setCarregando(true);
        setErro('');

        const [leis, nuvem, rankingParlamentares, rankingPartidos] =
          await Promise.all([
            buscarLeis({ limit: 200 }),
            buscarNuvemPalavras({ limit: 30 }),
            buscarRankingParlamentares({ limit: 5 }),
            buscarRankingPartidos({ limit: 6 }),
          ]);

        setProposicoes(leis);
        setPalavras(nuvem);
        setParlamentares(rankingParlamentares);
        setPartidos(rankingPartidos);
      } catch (error) {
        setErro(extrairMensagemErro(error));
      } finally {
        setCarregando(false);
      }
    };

    carregarDados();
  }, []);

  const volumePorSubtema = useMemo(
    () => calcularVolumePorSubtema(proposicoes),
    [proposicoes]
  );

  const totalProposicoes = useMemo(() => {
  return volumePorSubtema.reduce((acc, item) => acc + item.total, 0);
}, [volumePorSubtema]);

  return (
    <div className="bg-[#E5E5E5]">
      <section className="bg-[#FF7A1A] px-6 md:px-12 py-10">
        <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
          <div className="lg:col-span-7">
            <h1 className="font-serif text-3xl md:text-5xl font-black uppercase leading-tight text-black">
              Monitorando Leis de{' '}
              <span className="text-[#0038A8]">Proteção Infantil</span> e
              Combate ao Cyberbullying
            </h1>

            <p className="mt-5 text-lg md:text-xl font-bold text-black max-w-3xl">
              Acompanhe em tempo real as proposições legislativas da Câmara dos
              Deputados e do Senado Federal voltadas para a segurança digital e
              proteção de crianças e adolescentes.
            </p>

            <div className="mt-8 flex flex-wrap gap-6 justify-center lg:justify-start">
              <Link
                to="/leis"
                className="bg-[#0038A8] text-white px-8 py-3 rounded-lg font-serif font-black uppercase shadow-md hover:bg-[#002B80] transition"
              >
                Ver as proposições →
              </Link>

              <Link
                to="/sobre"
                className="bg-[#5D4E6D] text-white px-8 py-3 rounded-lg font-serif font-black uppercase shadow-md hover:bg-[#4D405A] transition"
              >
                Sobre o projeto &lt;/&gt;
              </Link>
            </div>
          </div>

          <div className="lg:col-span-5">
            <div className="h-[260px] md:h-[330px] rounded-sm overflow-hidden bg-orange-300 border-4 border-orange-400 shadow-lg">
              <img
                src="/images/hero-protectkids.png"
                alt="Criança brincando em ambiente seguro"
                className="w-full h-full object-cover"
              />
            </div>
          </div>
        </div>
      </section>

      <section className="bg-[#E5E5E5] px-6 md:px-12 py-10">
        <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="bg-[#FACC15] border-4 border-gray-500 rounded-xl p-6 text-center shadow-md">
            <h3 className="font-serif text-xl font-black text-white uppercase">
              Transparência Total
            </h3>
            <p className="mt-3 text-xs font-bold uppercase leading-relaxed text-white">
              Todos os dados são obtidos diretamente de APIs oficiais,
              garantindo informações atualizadas e confiáveis.
            </p>
            <div className="mt-4 text-3xl">🛡️</div>
          </div>

          <div className="bg-[#1D2DF3] border-4 border-gray-500 rounded-xl p-6 text-center shadow-md">
            <h3 className="font-serif text-xl font-black text-white uppercase">
              Foco Especializado
            </h3>
            <p className="mt-3 text-xs font-bold uppercase leading-relaxed text-white">
              Filtramos apenas proposições relacionadas à proteção infantil,
              cyberbullying e segurança digital.
            </p>
            <div className="mt-4 text-3xl">ⓘ</div>
          </div>

          <div className="bg-[#FF7A1A] border-4 border-gray-500 rounded-xl p-6 text-center shadow-md">
            <h3 className="font-serif text-xl font-black text-white uppercase">
              Acompanhamento em Tempo Real
            </h3>
            <p className="mt-3 text-xs font-bold uppercase leading-relaxed text-white">
              Monitore o status de cada proposição desde a apresentação até a
              aprovação ou arquivamento.
            </p>
            <div className="mt-4 text-3xl">↗</div>
          </div>
        </div>
      </section>

      <section className="bg-[#E5E5E5]">
        <div className="bg-[#FACC15] py-5 text-center">
          <h2 className="font-serif text-3xl md:text-4xl font-black uppercase text-[#001B5E]">
            Dashboard Analítico
          </h2>
        </div>

        <div className="max-w-7xl mx-auto px-6 md:px-12 py-8 space-y-6">
          {erro && (
            <div className="bg-red-50 border border-red-300 text-red-700 rounded-xl p-4 font-bold">
              {erro}
            </div>
          )}

          {carregando ? (
            <div className="bg-white rounded-2xl p-10 text-center font-bold text-gray-500">
              Carregando dados do dashboard...
            </div>
          ) : (
            <>
              <DashboardBox titulo="Nuvem de Palavras" icone="☁️">
                <NuvemPalavras palavras={palavrasNuvem} />
              </DashboardBox>

              <DashboardBox titulo="Volume de Proposições por Subtema (NLP)" icone="◷">
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                  <div>
                    <h3 className="font-bold text-sm mb-4">
                      Quantidade de proposições identificadas
                    </h3>

                    <div className="h-[280px]">
                      <ResponsiveContainer width="100%" height="100%">
                        <BarChart data={volumePorSubtema}>
                          <XAxis
                            dataKey="nome"
                            interval={0}
                            angle={-18}
                            textAnchor="end"
                            height={70}
                            tick={{ fontSize: 10 }}
                          />
                          <YAxis allowDecimals={false} />
                          <Tooltip />
                          <Bar dataKey="total">
                            {volumePorSubtema.map((_, index) => (
                              <Cell key={index} fill={cores[index % cores.length]} />
                            ))}
                          </Bar>
                        </BarChart>
                      </ResponsiveContainer>
                    </div>
                  </div>

                  <div>
                    <h3 className="font-bold text-sm mb-4">
                      Distribuição percentual
                    </h3>

                    <div className="h-[280px]">
                      <ResponsiveContainer width="100%" height="100%">
                        <PieChart>
                          <Pie
                            data={volumePorSubtema}
                            dataKey="total"
                            nameKey="nome"
                            innerRadius={55}
                            outerRadius={95}
                            label
                          >
                            {volumePorSubtema.map((_, index) => (
                              <Cell key={index} fill={cores[index % cores.length]} />
                            ))}
                          </Pie>
                          <Tooltip />
                        </PieChart>
                      </ResponsiveContainer>
                    </div>

                    <p className="text-right font-black text-[#0038A8]">
                      Total de proposições: {totalProposicoes}
                    </p>
                  </div>
                </div>
              </DashboardBox>

              <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <DashboardBox titulo="Top Parlamentares" icone="🏅">
                  <div className="space-y-3">
                    {parlamentares.map((item) => {
                      const maior = parlamentares[0]?.total_proposicoes || 1;
                      const largura = (item.total_proposicoes / maior) * 100;

                      return (
                        <div key={`${item.nome}-${item.partido}`}>
                          <div className="flex justify-between text-xs font-bold mb-1">
                            <span>
                              {item.nome} ({item.partido}/{item.uf})
                            </span>
                            <span>{item.total_proposicoes}</span>
                          </div>

                          <div className="h-3 bg-gray-200 rounded-full overflow-hidden">
                            <div
                              className="h-full bg-[#2563EB] rounded-full"
                              style={{ width: `${largura}%` }}
                            />
                          </div>
                        </div>
                      );
                    })}
                  </div>

                  <p className="mt-4 text-right font-black text-[#0038A8]">
                    Total de parlamentares: {parlamentares.length}
                  </p>
                </DashboardBox>

                <DashboardBox titulo="Engajamento por Partido" icone="👥">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 items-center">
                    <div className="h-[220px]">
                      <ResponsiveContainer width="100%" height="100%">
                        <PieChart>
                          <Pie
                            data={partidos}
                            dataKey="total_proposicoes"
                            nameKey="partido"
                            innerRadius={45}
                            outerRadius={85}
                          >
                            {partidos.map((_, index) => (
                              <Cell key={index} fill={cores[index % cores.length]} />
                            ))}
                          </Pie>
                          <Tooltip />
                        </PieChart>
                      </ResponsiveContainer>
                    </div>

                    <div className="text-xs">
                      <div className="grid grid-cols-2 font-black border-b pb-1 mb-2">
                        <span>Partido</span>
                        <span className="text-right">Proposições</span>
                      </div>

                      {partidos.map((item) => (
                        <div
                          key={item.partido}
                          className="grid grid-cols-2 py-1 border-b border-gray-100"
                        >
                          <span>{item.partido || 'ND'}</span>
                          <span className="text-right font-bold">
                            {item.total_proposicoes}
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>
                </DashboardBox>
              </div>
            </>
          )}
        </div>
      </section>
    </div>
  );
}