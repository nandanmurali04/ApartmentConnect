import { Routes, Route, useLocation } from "react-router-dom";

import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Flats from "./pages/Flats";
import Owners from "./pages/Owners";
import Maintenance from "./pages/Maintenance";

import Navbar from "./components/Navbar";

function App() {

  const location = useLocation();

  return (

    <>

      {location.pathname !== "/" && <Navbar />}

      <Routes>

        <Route path="/" element={<Login />} />

        <Route path="/dashboard" element={<Dashboard />} />

        <Route path="/flats" element={<Flats />} />

        <Route path="/owners" element={<Owners />} />

        <Route path="/maintenance" element={<Maintenance />} />

      </Routes>

    </>

  );

}

export default App;