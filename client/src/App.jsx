import React, { useState } from 'react';
import { Container, Box } from '@mui/material';
import WaterQualityForm from './components/WaterQualityForm';
import WaterQualityReport from './components/WaterQualityReport';

function App() {
  const [evaluationResult, setEvaluationResult] = useState(null);

  const handleResult = (result) => {
    setEvaluationResult(result);
  };

  return (
    <Container maxWidth="lg">
      <Box my={4}>
        <WaterQualityForm onResult={handleResult} />
        {evaluationResult && (
          <WaterQualityReport result={evaluationResult} />
        )}
      </Box>
    </Container>
  );
}

export default App;
