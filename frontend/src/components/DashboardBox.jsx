export default function DashboardBox({ titulo, icone, children }) {
  return (
    <section className="bg-white border border-gray-400 rounded-2xl overflow-hidden shadow-sm">
      <div className="bg-gradient-to-r from-white to-gray-100 border-b border-gray-300 px-4 py-2 flex items-center gap-2">
        <span className="text-xl">{icone}</span>
        <h2 className="font-serif font-black uppercase text-[#374151] text-sm md:text-base">
          {titulo}
        </h2>
      </div>

      <div className="p-4">{children}</div>
    </section>
  );
}