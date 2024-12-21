import React from 'react';
import { Typography, Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from '@mui/material';

const WaterQualityReport = ({ result }) => {
    const { quality_score, report, graph } = result;

    return (
        <Paper elevation={3} sx={{ p: 3, mt: 3 }}>
            <Typography variant="h5" gutterBottom>
                Water Quality Report
            </Typography>

            <TableContainer sx={{ mb: 3 }}>
                <Table size="small">
                    <TableHead>
                        <TableRow>
                            <TableCell style={{ fontWeight: 'bold' }}>Parameter</TableCell>
                            <TableCell style={{ fontWeight: 'bold' }}>Recommended Range/Limit</TableCell>
                            <TableCell style={{ fontWeight: 'bold' }}>Reference</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        <TableRow>
                            <TableCell>Temperature</TableCell>
                            <TableCell>Generally should not exceed 25°C</TableCell>
                            <TableCell>WHO, 2011</TableCell>
                        </TableRow>
                        <TableRow>
                            <TableCell>pH</TableCell>
                            <TableCell>6.5 – 8.5</TableCell>
                            <TableCell>WHO, 2011</TableCell>
                        </TableRow>
                        <TableRow>
                            <TableCell>Turbidity (NTU)</TableCell>
                            <TableCell>≤1 NTU (desirable); ≤5 NTU (maximum)</TableCell>
                            <TableCell>WHO, 2011</TableCell>
                        </TableRow>
                        <TableRow>
                            <TableCell>Dissolved Oxygen (mg/L)</TableCell>
                            <TableCell>{'>'}5 mg/L for aquatic life</TableCell>
                            <TableCell>WHO, 2011</TableCell>
                        </TableRow>
                        <TableRow>
                            <TableCell>Conductivity (µS/cm)</TableCell>
                            <TableCell>≤2500 µS/cm (depending on region)</TableCell>
                            <TableCell>Kahlown & Majeed, 2003</TableCell>
                        </TableRow>
                        <TableRow>
                            <TableCell>Total Dissolved Solids (mg/L)</TableCell>
                            <TableCell>≤500 mg/L (desirable); ≤1000 mg/L (max)</TableCell>
                            <TableCell>WHO, 2011</TableCell>
                        </TableRow>
                        <TableRow>
                            <TableCell>Nitrate (mg/L as nitrogen)</TableCell>
                            <TableCell>≤10 mg/L</TableCell>
                            <TableCell>WHO, 2011; EPA, 2024</TableCell>
                        </TableRow>
                        <TableRow>
                            <TableCell>Phosphate (mg/L)</TableCell>
                            <TableCell>≤0.1 mg/L</TableCell>
                            <TableCell>EPA, 2022</TableCell>
                        </TableRow>
                        <TableRow>
                            <TableCell>Total Coliforms (CFU/100 mL)</TableCell>
                            <TableCell>0 CFU/100 mL</TableCell>
                            <TableCell>EPA, 2024</TableCell>
                        </TableRow>
                        <TableRow>
                            <TableCell>E. coli (CFU/100 mL)</TableCell>
                            <TableCell>0 CFU/100 mL</TableCell>
                            <TableCell>EPA, 2024</TableCell>
                        </TableRow>
                        <TableRow>
                            <TableCell>BOD (mg/L)</TableCell>
                            <TableCell>≤2 mg/L</TableCell>
                            <TableCell>WHO, 2011</TableCell>
                        </TableRow>
                        <TableRow>
                            <TableCell>COD (mg/L)</TableCell>
                            <TableCell>{'>'}20 mg/L for treated effluent</TableCell>
                            <TableCell>WHO, 2011</TableCell>
                        </TableRow>
                        <TableRow>
                            <TableCell>Hardness (mg/L as CaCO3)</TableCell>
                            <TableCell>≤300 mg/L (desirable); ≤500 mg/L (max)</TableCell>
                            <TableCell>WHO, 2011</TableCell>
                        </TableRow>
                        <TableRow>
                            <TableCell>Alkalinity (mg/L as CaCO3)</TableCell>
                            <TableCell>20 – 200 mg/L</TableCell>
                            <TableCell>Kahlown & Majeed, 2003</TableCell>
                        </TableRow>
                        <TableRow>
                            <TableCell>Iron (mg/L)</TableCell>
                            <TableCell>≤0.3 mg/L</TableCell>
                            <TableCell>EPA, 2024</TableCell>
                        </TableRow>
                    </TableBody>
                </Table>
            </TableContainer>

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

            <Typography variant="caption" display="block" sx={{ mt: 2, textAlign: 'center', color: 'text.secondary' }}>
                Made For Experimental Design Report by Necdet Ömer Barut
            </Typography>
        </Paper>
    );
};

export default WaterQualityReport;