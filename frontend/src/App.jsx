// src/App.jsx
import React from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Home from "./pages/Home";
import Scraping from "./pages/Scraping";
import WordCloud from "./pages/WordCloud"; // Import the WordCloud page
import Visualization from "./pages/Visualization"; // Import the Visualization page
import Notfound from "./pages/Notfound";
import ProtectedRoute from "./components/ProtectedRoute";
import Layout from "./components/Layout"; // Import the Layout component
import { ChakraProvider } from "@chakra-ui/react";

function Logout() {
  localStorage.clear();
  return <Navigate to="/login" />;
}

function RegisterAndLogout() {
  localStorage.clear();
  return <Register />;
}

function App() {
  return (
    <ChakraProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/logout" element={<Logout />} />
          <Route path="/register" element={<RegisterAndLogout />} />

          {/* Wrap protected routes with the Layout */}
          <Route
            path="/"
            element={
              <ProtectedRoute>
                <Layout>
                  <Home />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/scraping"
            element={
              <ProtectedRoute>
                <Layout>
                  <Scraping />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/wordcloud/:interestId"
            element={
              <ProtectedRoute>
                <Layout>
                  <WordCloud />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/visualization"
            element={
              <ProtectedRoute>
                <Layout>
                  <Visualization />
                </Layout>
              </ProtectedRoute>
            }
          />

          <Route path="*" element={<Notfound />} />
        </Routes>
      </BrowserRouter>
    </ChakraProvider>
  );
}

export default App;
