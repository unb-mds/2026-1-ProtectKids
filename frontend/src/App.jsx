import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import TodasAsLeis from './pages/TodasAsLeis';
import Inicio from './pages/Inicio';
import DetalhesLei from './pages/DetalhesLei';
import Sobre from './pages/Sobre';
import Estatisticas from './pages/Estatisticas';
import Footer from './components/Footer';

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen flex flex-col font-sans">
        
        {/* NAVBAR */}
        <nav className="bg-pk-red text-white py-4 px-8 flex justify-between items-center shadow-md">
          <div className="font-bold text-2xl tracking-tighter">
            PROTECT<span className="text-gray-300">KIDS</span>
            <p className="text-xs font-normal text-gray-300 uppercase tracking-widest mt-1">
              Monitoramento Legislativo
            </p>
          </div>
          <div className="space-x-6 text-sm font-semibold">
            <Link to="/" className="hover:text-gray-300 transition">INÍCIO</Link>
            <Link to="/leis" className="hover:text-gray-300 transition">TODAS AS LEIS</Link>
            <Link to="/estatisticas" className="hover:text-gray-300 transition">ESTATÍSTICAS</Link>
            <Link to="/sobre" className="hover:text-gray-300 transition">SOBRE O PROJETO</Link>
          </div>
        </nav>

        {/* CONTEÚDO DINÂMICO */}
        <main className="flex-grow">
          <Routes>
            <Route path="/" element={<Inicio />} />
            <Route path="/leis" element={<TodasAsLeis />} />
            <Route path="/leis/:id" element={<DetalhesLei />} />
            <Route path="/sobre" element={<Sobre />} />
            <Route path="/estatisticas" element={<Estatisticas />} />
          </Routes>
        </main>

        <Footer />
        
      </div>
    </BrowserRouter>
  );
}

export default App;