import React, { useState } from "react";
import { Routes, Route, Navigate, useLocation, useNavigate } from "react-router-dom";
import LoginPage from "./pages/Login";
import Hub from "./pages/Hub";
import Chat from "./pages/Chat";
import Footer from "./components/Footer";
import "./App.css";
import PropTypes from 'prop-types';

const Logout = ({ onLogout }) => {
  const navigate = useNavigate();

  React.useEffect(() => {
    onLogout();
    navigate("/");
  }, [onLogout, navigate]);

  return null;
};

Logout.propTypes = {
  onLogout: PropTypes.func.isRequired,
};

const App = () => {
  const [client, setClient] = useState(null);
  const location = useLocation();

  const handleLoginComplete = (matrixClient) => {
    setClient(matrixClient);
  };

  const handleLogout = () => {
    setClient(null);
  };

  const noFooterRoutes = ["/"];

  return (
    <div className="app-container">
      <div className="content">
        <Routes>
          <Route
            path="/"
            element={
              client ? (
                <Navigate to="/hub" replace />
              ) : (
                <LoginPage onLoginComplete={handleLoginComplete} />
              )
            }
          />
          <Route
            path="/hub"
            element={client ? <Hub client={client} /> : <Navigate to="/" replace />}
          />
          <Route
            path="/chat"
            element={client ? <Chat client={client} /> : <Navigate to="/" replace />}
          />
          <Route path="/logout" element={<Logout onLogout={handleLogout} />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </div>
      {!noFooterRoutes.includes(location.pathname) && <Footer />}
    </div>
  );
};

export default App;
