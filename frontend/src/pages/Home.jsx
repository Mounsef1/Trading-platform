// src/pages/Home.jsx
import { useState, useEffect } from "react";
import { Button, Flex, Box, Text } from "@chakra-ui/react";
import api from "../api";

function Home() {
  const [username, setUsername] = useState("");

  useEffect(() => {
    getUsername();
  }, []);

  const getUsername = () => {
    api
      .get("/api/user/details/")
      .then((res) => res.data)
      .then((data) => {
        setUsername(data.username);
      })
      .catch((err) => {
        console.error("Error fetching username:", err);
        alert("Failed to fetch username");
      });
  };

  const handleLogout = () => {
    window.location.href = "/logout/";
  };

  return (
    <Flex direction="column" align="center" justify="center" h="100vh">
      <Box position="absolute" top="10px" right="10px">
        <Button colorScheme="red" onClick={handleLogout}>
          Logout
        </Button>
      </Box>
      <Text fontSize="3xl" fontWeight="bold">
        {username ? `Hello, ${username}!` : "Loading..."}
      </Text>
    </Flex>
  );
}

export default Home;
