const cores = [
  '#0038A8',
  '#2563EB',
  '#FACC15',
  '#FF7A1A',
  '#16A34A',
  '#7C3AED',
];

const calcularTamanho = (valor, maiorValor) => {
  if (!maiorValor) return 16;

  const minimo = 14;
  const maximo = 48;
  const proporcao = valor / maiorValor;

  return Math.round(minimo + proporcao * (maximo - minimo));
};

export default function NuvemPalavras({ palavras = [] }) {
  if (!palavras.length) {
    return (
      <div className="min-h-[170px] flex items-center justify-center text-gray-400 italic">
        Nenhuma palavra disponível.
      </div>
    );
  }

  const maiorValor = Math.max(...palavras.map((item) => item.value));

  return (
    <div className="min-h-[180px] flex flex-wrap items-center justify-center gap-x-6 gap-y-3 px-4 py-6">
      {palavras.map((palavra, index) => (
        <span
          key={`${palavra.text}-${index}`}
          className="font-black transition-transform hover:scale-110 cursor-default"
          style={{
            fontSize: `${calcularTamanho(palavra.value, maiorValor)}px`,
            color: cores[index % cores.length],
          }}
          title={`${palavra.text}: ${palavra.value}`}
        >
          {palavra.text}
        </span>
      ))}
    </div>
  );
}