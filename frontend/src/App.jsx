import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import Footer from './components/Footer';
import Inicio from './pages/Inicio';
import TodasAsLeis from './pages/TodasAsLeis';
import DetalhesLei from './pages/DetalhesLei';
import Sobre from './pages/Sobre';
import Estatisticas from './pages/Estatisticas';

export default function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen flex flex-col bg-[#E5E5E5]">
        <Header />

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
