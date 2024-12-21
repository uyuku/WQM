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
        setFormData({
            ...formData,
            [name]: value === '' ? '' : parseFloat(value),
        });
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        setLoading(true);
        setError('');
        try {
            const processedFormData = Object.fromEntries(
                Object.entries(formData).map(([key, value]) => [
                    key,
                    value === '' ? null : value,
                ])
            );
            const result = await evaluateWaterQuality(processedFormData);
            onResult(result);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const parameters = [
        { name: 'Temperature', label: 'Temperature (°C)', type: 'text' }, 
        { name: 'pH', label: 'pH', type: 'text' }, 
        { name: 'Turbidity', label: 'Turbidity (NTU)', type: 'text' }, 
        { name: 'DissolvedOxygen', label: 'Dissolved Oxygen (mg/L)', type: 'text' }, // Changed // Changed to 'text'to 'text'// Changed to 'text'
        { name: 'Conductivity', label: 'Conductivity (µS/cm)', type: 'text' }, // Changed to 'text'
        { name: 'TotalDissolvedSolids', label: 'Total Dissolved Solids (mg/L)', type: 'text' }, // Changed to 'text'
        { name: 'Nitrate', label: 'Nitrate (mg/L)', type: 'text' }, // Changed to 'text'
        { name: 'Phosphate', label: 'Phosphate (mg/L)', type: 'text' }, // Changed to 'text'
        { name: 'TotalColiforms', label: 'Total Coliforms (CFU/100mL)', type: 'text' }, // Changed to 'text'
        { name: 'Ecoli', label: 'E. coli (CFU/100mL)', type: 'text' }, // Changed to 'text'
        { name: 'BOD', label: 'BOD (mg/L)', type: 'text' },
        { name: 'COD', label: 'COD (mg/L)', type: 'text' }, // Changed to 'text'
        { name: 'Hardness', label: 'Hardness (mg/L as CaCO3)', type: 'text' }, // Changed to 'text'
        { name: 'Alkalinity', label: 'Alkalinity (mg/L as CaCO3)', type: 'text' }, // Changed to 'text'
        { name: 'Iron', label: 'Iron (mg/L)', type: 'text' }, // Changed to 'text'
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
                                value={formData[param.name] === 0 ? '0' : formData[param.name] || ''}
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