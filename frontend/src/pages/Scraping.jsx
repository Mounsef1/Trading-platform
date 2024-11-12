import { useState, useEffect } from "react";
import {
  Box,
  Button,
  Input,
  Wrap,
  WrapItem,
  Text,
  IconButton,
  useToast,
  Flex,
  HStack,
  Spinner,
} from "@chakra-ui/react";
import { CloseIcon } from "@chakra-ui/icons";
import api from "../api";

function Scraping() {
  const [interests, setInterests] = useState([]);
  const [newInterest, setNewInterest] = useState("");
  const [scrapingStatus, setScrapingStatus] = useState({});
  const toast = useToast();

  useEffect(() => {
    fetchInterests();
  }, []);

  const fetchInterests = () => {
    api
      .get("/api/user-interests/")
      .then((res) => setInterests(res.data))
      .catch((err) => console.error("Failed to fetch interests:", err));
  };

  const addInterest = () => {
    if (newInterest.trim() === "") return;
    api
      .post("/api/user-interests/", { company_name: newInterest })
      .then((res) => {
        setInterests([...interests, res.data]);
        setNewInterest("");
        toast({
          title: "Interest added successfully",
          status: "success",
          duration: 3000,
          isClosable: true,
        });
      })
      .catch((err) => {
        console.error("Failed to add interest:", err);
        toast({
          title: "Failed to add interest",
          status: "error",
          duration: 3000,
          isClosable: true,
        });
      });
  };

  const deleteInterest = (id) => {
    api
      .delete(`/api/user-interests/${id}/`)
      .then(() => {
        setInterests(interests.filter((interest) => interest.id !== id));
        toast({
          title: "Interest deleted",
          status: "info",
          duration: 3000,
          isClosable: true,
        });
      })
      .catch((err) => console.error("Failed to delete interest:", err));
  };

  const runScraping = () => {
    if (interests.length === 0) {
      toast({
        title: "No interests to scrape",
        description: "Please add an interest first.",
        status: "warning",
        duration: 3000,
        isClosable: true,
      });
      return;
    }

    // Start scraping each interest individually
    interests.forEach((interest) => {
      setScrapingStatus((prevStatus) => ({
        ...prevStatus,
        [interest.id]: "In Progress",
      }));

      api
        .post(`/api/user-interests/${interest.id}/run_scraper/`)
        .then(() => {
          setScrapingStatus((prevStatus) => ({
            ...prevStatus,
            [interest.id]: "Completed",
          }));
          toast({
            title: `Scraping completed for ${interest.company_name}`,
            status: "success",
            duration: 2000,
            isClosable: true,
          });
        })
        .catch(() => {
          setScrapingStatus((prevStatus) => ({
            ...prevStatus,
            [interest.id]: "Failed",
          }));
          toast({
            title: `Scraping failed for ${interest.company_name}`,
            status: "error",
            duration: 2000,
            isClosable: true,
          });
        });
    });
  };

  return (
    <Box p="6">
      {/* Interest List */}
      <Text fontSize="2xl" fontWeight="bold" mb="4">
        Saved Interests
      </Text>
      <Wrap spacing="4" mb="6">
        {interests.map((interest) => (
          <WrapItem key={interest.id}>
            <Box
              display="flex"
              alignItems="center"
              p="2"
              borderWidth="1px"
              borderRadius="md"
              borderColor="gray.300"
              bg="gray.100"
              pr="2"
            >
              <Text mr="2">{interest.company_name}</Text>
              <IconButton
                icon={<CloseIcon />}
                colorScheme="red"
                size="sm"
                onClick={() => deleteInterest(interest.id)}
                aria-label="Delete interest"
              />
              {scrapingStatus[interest.id] === "In Progress" && (
                <Spinner size="sm" ml="2" />
              )}
              {scrapingStatus[interest.id] &&
                scrapingStatus[interest.id] !== "In Progress" && (
                  <Text
                    ml="2"
                    fontSize="sm"
                    color={
                      scrapingStatus[interest.id] === "Completed"
                        ? "green.500"
                        : "red.500"
                    }
                  >
                    {scrapingStatus[interest.id]}
                  </Text>
                )}
            </Box>
          </WrapItem>
        ))}
      </Wrap>

      {/* Input and Scraping Button */}
      <Flex justify="space-between" align="center" mt="6">
        {/* Input Field for New Interest on the Left */}
        <HStack spacing="2" w="70%">
          <Input
            placeholder="Enter new interest"
            value={newInterest}
            onChange={(e) => setNewInterest(e.target.value)}
            size="md"
            borderRadius="md"
            w="100%"
          />
          <Button colorScheme="blue" onClick={addInterest}>
            Add Interest
          </Button>
        </HStack>

        {/* Scraping Button on the Right */}
        <Button colorScheme="green" onClick={runScraping} ml="4">
          Start Scraping
        </Button>
      </Flex>
    </Box>
  );
}

export default Scraping;
