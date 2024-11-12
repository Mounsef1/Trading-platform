// src/components/Layout.jsx
import React from "react";
import { Box, VStack, Text, Link } from "@chakra-ui/react";
import { Link as RouterLink } from "react-router-dom";

function Layout({ children }) {
  return (
    <Box display="flex" h="100vh">
      {/* Sidebar */}
      <Box w="200px" bg="gray.700" color="white" p="4">
        <VStack align="start" spacing="4">
          <Text fontSize="2xl" fontWeight="bold">
            Menu
          </Text>
          <Link as={RouterLink} to="/" fontSize="lg">
            Home
          </Link>
          <Link as={RouterLink} to="/scraping" fontSize="lg">
            Scraping
          </Link>
        </VStack>
      </Box>

      {/* Main Content */}
      <Box flex="1" p="4">
        {children}
      </Box>
    </Box>
  );
}

export default Layout;
