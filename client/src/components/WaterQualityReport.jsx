import React from 'react';
import { Typography, Paper } from '@mui/material';

const WaterQualityReport = ({ result }) => {
    const { quality_score, report, graph } = result;

    return (
        <Paper elevation={3} sx={{ p: 3, mt: 3 }}>
            <Typography variant="h5" gutterBottom>
                Water Quality Report
            </Typography>

            <Typography variant="h6">
                Overall Quality Score: {quality_score.toFixed(2)} / 100
            </Typography>

            <Typography variant="body1" sx={{ whiteSpace: 'pre-line' }}>
                {report}
            </Typography>

            <div style={{ marginTop: 20 }}>
                <img
                    src={`data:image/png;base64,${graph}`}
                    alt="Water Quality Graph"
                    style={{ width: '100%' }}
                />
            </div>
        </Paper>
    );
};

export default WaterQualityReport;
