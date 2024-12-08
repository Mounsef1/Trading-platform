import React, { useState, useEffect } from "react";
import {
  Box,
  Select,
  Text,
  SimpleGrid,
  GridItem,
  Spinner,
  Center,
} from "@chakra-ui/react";
import api from "../api";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  PieChart,
  Pie,
  Cell,
} from "recharts";

function Visualization() {
  const [interests, setInterests] = useState([]);
  const [sources, setSources] = useState([]);
  const [selectedInterest, setSelectedInterest] = useState("");
  const [selectedSource, setSelectedSource] = useState("");
  const [timeSeriesData, setTimeSeriesData] = useState([]);
  const [wordCloud, setWordCloud] = useState(null);
  const [sentiment, setSentiment] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchInterests();
    fetchSources();
  }, []);

  const fetchInterests = () => {
    api
      .get("/api/user-interests/")
      .then((res) => setInterests(res.data))
      .catch((err) => console.error("Failed to fetch interests:", err));
  };

  const fetchSources = () => {
    api
      .get("/api/sources/")
      .then((res) => setSources(res.data))
      .catch((err) => console.error("Failed to fetch sources:", err));
  };

  const fetchVisualizationData = (interestId, source) => {
    setLoading(true);
    const params = source ? { source } : {};

    Promise.all([
      api.get(`/api/sentiment-timeseries/${interestId}/`, { params }),
      api.get(`/api/generate-wordcloud/${interestId}/`, { params }),
    ])
      .then(([timeSeriesRes, wordCloudRes]) => {
        setTimeSeriesData(timeSeriesRes.data);
        setWordCloud(wordCloudRes.data.wordcloud);
        setSentiment(wordCloudRes.data.sentiment);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Failed to fetch visualization data:", err);
        setLoading(false);
      });
  };

  const handleInterestChange = (e) => {
    const interestId = e.target.value;
    setSelectedInterest(interestId);
    if (interestId) fetchVisualizationData(interestId, selectedSource);
  };

  const handleSourceChange = (e) => {
    const source = e.target.value;
    setSelectedSource(source);
    if (selectedInterest) fetchVisualizationData(selectedInterest, source);
  };

  const sentimentData = sentiment
    ? [
        { name: "Positive", value: sentiment.pos },
        { name: "Neutral", value: sentiment.neu },
        { name: "Negative", value: sentiment.neg },
      ]
    : [];

  const COLORS = ["#0088FE", "#00C49F", "#FF8042"];

  return (
    <Box p="6">
      <Text fontSize="2xl" fontWeight="bold" mb="4">
        Visualization Dashboard
      </Text>

      {/* Dropdown to select interest */}
      <Select
        placeholder="Select a keyword"
        onChange={handleInterestChange}
        value={selectedInterest}
        mb="4"
      >
        {interests.map((interest) => (
          <option key={interest.id} value={interest.id}>
            {interest.company_name}
          </option>
        ))}
      </Select>

      {/* Dropdown to select source */}
      <Select
        placeholder="All Sources"
        onChange={handleSourceChange}
        value={selectedSource}
        mb="6"
      >
        <option value="">All Sources</option>
        {sources.map((source, index) => (
          <option key={index} value={source}>
            {source}
          </option>
        ))}
      </Select>

      {loading && (
        <Center>
          <Spinner size="xl" />
        </Center>
      )}

      {!loading && (
        <SimpleGrid columns={{ base: 1, md: 4 }} gap="6" w="100%">
          {/* Line Chart */}
          <GridItem colSpan={{ base: 1, md: 2 }}>
            {timeSeriesData.length > 0 && (
              <Box>
                <Text fontSize="xl" fontWeight="bold" mb="4">
                  Sentiment Evolution Over Time
                </Text>
                <LineChart
                  width={580} // Increased the width slightly
                  height={400}
                  data={timeSeriesData}
                  margin={{ top: 10, right: 10, left: 10, bottom: 10 }}
                >
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Line
                    type="monotone"
                    dataKey="pos"
                    stroke="#00C49F"
                    name="Positive"
                  />
                  <Line
                    type="monotone"
                    dataKey="neu"
                    stroke="#8884d8"
                    name="Neutral"
                  />
                  <Line
                    type="monotone"
                    dataKey="neg"
                    stroke="#FF8042"
                    name="Negative"
                  />
                </LineChart>
              </Box>
            )}
          </GridItem>

          {/* Word Cloud */}
          <GridItem colSpan={{ base: 1, md: 2 }}>
            {wordCloud && (
              <Box textAlign="center">
                <Text fontSize="xl" fontWeight="bold" mb="2">
                  Word Cloud
                </Text>
                <Box
                  as="img"
                  src={`data:image/png;base64,${wordCloud}`}
                  alt="Word Cloud"
                  borderRadius="md"
                  boxShadow="md"
                  width="100%" // Expand to the full column width
                  maxWidth="450px" // Make it larger
                  height="100%"
                  mx="auto"
                />
              </Box>
            )}
          </GridItem>
        </SimpleGrid>
      )}

      {/* Sentiment Pie Chart */}
      {!loading && sentiment && (
        <Box mt="8">
          <Text fontSize="xl" fontWeight="bold" mb="4">
            Sentiment Analysis
          </Text>
          <Center>
            <PieChart width={400} height={400}>
              <Pie
                data={sentimentData}
                dataKey="value"
                nameKey="name"
                cx="50%"
                cy="50%"
                outerRadius={120}
                fill="#8884d8"
              >
                {sentimentData.map((entry, index) => (
                  <Cell
                    key={`cell-${index}`}
                    fill={COLORS[index % COLORS.length]}
                  />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </Center>
        </Box>
      )}

      {!loading && !wordCloud && !sentiment && !timeSeriesData.length && (
        <Center>
          <Text>No data available for the selected interest and source.</Text>
        </Center>
      )}
    </Box>
  );
}

export default Visualization;
