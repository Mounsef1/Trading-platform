// src/components/Layout.jsx
import React from "react";
import { Box, VStack, Text, Link } from "@chakra-ui/react";
import { Link as RouterLink } from "react-router-dom";

function Layout({ children }) {
  return (
    <Box display="flex" h="100vh" overflow="hidden">
      {/* Sidebar */}
      <Box
        w="200px"
        bg="gray.700"
        color="white"
        p="4"
        position="fixed" // Fix the sidebar position
        h="100vh" // Ensure it covers the full viewport height
      >
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
          <Link as={RouterLink} to="/visualization" fontSize="lg">
            Visualization
          </Link>
        </VStack>
      </Box>

      {/* Main Content */}
      <Box
        flex="1"
        p="4"
        ml="200px" // Add margin to account for the fixed sidebar width
        overflowY="auto" // Allow scrolling for the main content
      >
        {children}
      </Box>
    </Box>
  );
}

export default Layout;
