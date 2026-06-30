const cores = [
  '#60A5FA',
  '#2563EB',
  '#FACC15',
  '#FB923C',
  '#4ADE80',
  '#A855F7',
];

const calcularTamanho = (valor, maiorValor) => {
  if (!maiorValor) return 16;

  const minimo = 14;
  const maximo = 52;
  const proporcao = valor / maiorValor;

  return Math.round(minimo + proporcao * (maximo - minimo));
};

const calcularRotacao = (index) => {
  const rotacoes = [-4, -2, 0, 2, 4, -3, 3];
  return rotacoes[index % rotacoes.length];
};

export default function NuvemPalavras({ palavras = [] }) {
  if (!palavras.length) {
    return (
      <div className="min-h-[190px] flex items-center justify-center text-gray-400 italic">
        Nenhuma palavra disponível.
      </div>
    );
  }

  const maiorValor = Math.max(...palavras.map((item) => item.value));

  return (
    <div
      className="min-h-[220px] flex flex-wrap items-center justify-center gap-x-5 gap-y-4 px-4 py-6"
      aria-label="Nuvem de palavras das proposições monitoradas"
    >
      {palavras.map((palavra, index) => {
        const tamanho = calcularTamanho(palavra.value, maiorValor);
        const cor = cores[index % cores.length];
        const rotacao = calcularRotacao(index);

        return (
          <span
            key={`${palavra.text}-${index}`}
            className="inline-block"
            style={{ transform: `rotate(${rotacao}deg)` }}
          >
            <span
              className="inline-block cursor-pointer select-none font-black tracking-wide transition-all duration-200 hover:scale-125 hover:-translate-y-1"
              style={{
                fontSize: `${tamanho}px`,
                color: cor,
                textShadow: `0 0 10px ${cor}30`,
              }}
              title={`${palavra.text}: ${palavra.value}`}
            >
              {palavra.text}
            </span>
          </span>
        );
      })}
    </div>
  );
}
