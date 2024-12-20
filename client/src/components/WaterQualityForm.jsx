import React, { useState } from 'react';
import {
    TextField,
    Button,
    Grid,
    Paper,
    Typography,
    Alert,
} from '@mui/material';
import { evaluateWaterQuality } from '../services/api';

const WaterQualityForm = ({ onResult }) => {
    const [formData, setFormData] = useState({});
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const handleChange = (event) => {
        const { name, value } = event.target;
        setFormData({ ...formData, [name]: value ? parseFloat(value) : null });
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        setLoading(true);
        setError('');
        try {
            const result = await evaluateWaterQuality(formData);
            onResult(result);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const parameters = [
        { name: 'Temperature', label: 'Temperature (°C)', type: 'number' },
        { name: 'pH', label: 'pH', type: 'number' },
        { name: 'Turbidity', label: 'Turbidity (NTU)', type: 'number' },
        { name: 'DissolvedOxygen', label: 'Dissolved Oxygen (mg/L)', type: 'number' },
        { name: 'Conductivity', label: 'Conductivity (µS/cm)', type: 'number' },
        { name: 'TotalDissolvedSolids', label: 'Total Dissolved Solids (mg/L)', type: 'number' },
        { name: 'Nitrate', label: 'Nitrate (mg/L)', type: 'number' },
        { name: 'Phosphate', label: 'Phosphate (mg/L)', type: 'number' },
        { name: 'TotalColiforms', label: 'Total Coliforms (CFU/100mL)', type: 'number' },
        { name: 'Ecoli', label: 'E. coli (CFU/100mL)', type: 'number' },
        { name: 'BOD', label: 'BOD (mg/L)', type: 'number' },
        { name: 'COD', label: 'COD (mg/L)', type: 'number' },
        { name: 'Hardness', label: 'Hardness (mg/L as CaCO3)', type: 'number' },
        { name: 'Alkalinity', label: 'Alkalinity (mg/L as CaCO3)', type: 'number' },
        { name: 'Iron', label: 'Iron (mg/L)', type: 'number' },
    ];

    return (
        <Paper elevation={3} sx={{ p: 3 }}>
            <Typography variant="h5" gutterBottom>
                Water Quality Evaluator
            </Typography>
            <form onSubmit={handleSubmit}>
                <Grid container spacing={2}>
                    {parameters.map((param) => (
                        <Grid item xs={12} sm={6} md={4} key={param.name}>
                            <TextField
                                fullWidth
                                label={param.label}
                                name={param.name}
                                type={param.type}
                                value={formData[param.name] || ''}
                                onChange={handleChange}
                                variant="outlined"
                            />
                        </Grid>
                    ))}
                    <Grid item xs={12}>
                        <Button
                            type="submit"
                            variant="contained"
                            color="primary"
                            disabled={loading}
                        >
                            {loading ? 'Evaluating...' : 'Evaluate Water Quality'}
                        </Button>
                    </Grid>
                    {error && (
                        <Grid item xs={12}>
                            <Alert severity="error">{error}</Alert>
                        </Grid>
                    )}
                </Grid>
            </form>
        </Paper>
    );
};

export default WaterQualityForm;
