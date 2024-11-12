import { NavLink } from "react-router-dom";
import { VStack, Text, Link, Box } from "@chakra-ui/react";

function SideNav() {
  return (
    <Box w="200px" bg="gray.700" color="white" p="4" minH="100vh">
      <VStack align="start" spacing="4">
        <Text fontSize="2xl" fontWeight="bold">
          Menu
        </Text>
        <Link as={NavLink} to="/" exact="true" fontSize="lg">
          Home
        </Link>
        <Link as={NavLink} to="/scraping" exact="true" fontSize="lg">
          Scraping
        </Link>
      </VStack>
    </Box>
  );
}

export default SideNav;
