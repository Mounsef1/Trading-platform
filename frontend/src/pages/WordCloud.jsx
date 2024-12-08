import React, { useState, useEffect } from "react";
import {
  Box,
  Spinner,
  Image,
  Text,
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
} from "@chakra-ui/react";
import { useParams } from "react-router-dom";
import api from "../api";

function WordCloud() {
  const { interestId } = useParams(); // Get the interestId from the URL
  const [loading, setLoading] = useState(true);
  const [wordCloud, setWordCloud] = useState(null);
  const [sentiment, setSentiment] = useState(null);

  useEffect(() => {
    // Fetch the word cloud and sentiment data
    api
      .get(`/api/generate-wordcloud/${interestId}/`)
      .then((res) => {
        setWordCloud(res.data.wordcloud);
        setSentiment(res.data.sentiment);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Failed to fetch word cloud data:", err);
        setLoading(false);
      });
  }, [interestId]);

  if (loading) {
    return (
      <Box textAlign="center" mt="20">
        <Spinner size="xl" />
        <Text mt="4">Loading word cloud and sentiment analysis...</Text>
      </Box>
    );
  }

  if (!wordCloud || !sentiment) {
    return (
      <Box textAlign="center" mt="20" color="red.500">
        <Text>Failed to load word cloud or sentiment data.</Text>
      </Box>
    );
  }

  return (
    <Box p="6">
      <Text fontSize="2xl" fontWeight="bold" mb="4">
        Word Cloud and Sentiment Analysis
      </Text>
      {/* Display Word Cloud */}
      <Image
        src={`data:image/png;base64,${wordCloud}`}
        alt="Word Cloud"
        borderRadius="md"
        mb="6"
      />

      {/* Display Sentiment Analysis */}
      <Text fontSize="xl" fontWeight="bold" mb="2">
        Sentiment Analysis Scores
      </Text>
      <Table variant="striped" colorScheme="teal">
        <Thead>
          <Tr>
            <Th>Sentiment</Th>
            <Th>Score</Th>
          </Tr>
        </Thead>
        <Tbody>
          <Tr>
            <Td>Negative</Td>
            <Td>{sentiment.neg}</Td>
          </Tr>
          <Tr>
            <Td>Neutral</Td>
            <Td>{sentiment.neu}</Td>
          </Tr>
          <Tr>
            <Td>Positive</Td>
            <Td>{sentiment.pos}</Td>
          </Tr>
          <Tr>
            <Td>Compound</Td>
            <Td>{sentiment.compound}</Td>
          </Tr>
        </Tbody>
      </Table>
    </Box>
  );
}

export default WordCloud;
