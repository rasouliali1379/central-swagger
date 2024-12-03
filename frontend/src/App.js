import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import LoginAndTable from "./pages/Login";
import MultiSwagger from "./pages/MultiSwagger";
import Services from "./pages/Services";

const App = () => {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<MultiSwagger />} />
                <Route path="/admin" element={<LoginAndTable />} />
                <Route path="/services" element={<Services />} />
            </Routes>
        </Router>
    );
};

export default App;