import React from "react";
import { Box, Image } from "@chakra-ui/react"; // Import Chakra UI components
import Form from "../components/Form";
import logo from "../assets/logo.png"; // Update with the path to your logo

function Login() {
  return (
    <Box textAlign="center" mt={10}>
      {/* Logo */}
      <Image src={logo} alt="App Logo" boxSize="150px" mx="auto" mb={6} />

      {/* Login Form */}
      <Form route="api/token/" method="login" />
    </Box>
  );
}

export default Login;
