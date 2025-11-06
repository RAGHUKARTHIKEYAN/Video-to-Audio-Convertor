import React, { useState } from 'react';
import { Container, Paper, TextField, Button, Typography, Box, Alert, CircularProgress } from '@mui/material';
import { useNavigate } from 'react-router-dom';

const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8080";

export default function Download() {
  const navigate = useNavigate();
  const [fid, setFid] = useState('');
  const [error, setError] = useState('');
  const [downloading, setDownloading] = useState(false);

  const handleDownload = async (e) => {
    e.preventDefault();
    if (!fid.trim()) {
      setError('Please enter a file ID');
      return;
    }

    setDownloading(true);
    setError('');

    try {
      const res = await fetch(
        `${API_URL}/download?fid=${encodeURIComponent(fid.trim())}`,
        {
          method: 'GET'
        }
      );

      if (!res.ok) {
        const text = await res.text();
        throw new Error(text || 'Download failed');
      }

      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${fid.trim()}.mp3`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
      setFid('');
    } catch (err) {
      setError(err.message);
    } finally {
      setDownloading(false);
    }
  };

  return (
    <Container maxWidth="sm">
      <Box sx={{ mt: 8, mb: 4 }}>
        <Paper elevation={3} sx={{ p: 4 }}>
          <Typography variant="h4" component="h1" gutterBottom align="center">
            Download MP3
          </Typography>

          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}

          <form onSubmit={handleDownload}>
            <TextField
              label="File ID (FID)"
              fullWidth
              margin="normal"
              value={fid}
              onChange={(e) => setFid(e.target.value)}
              required
              disabled={downloading}
              helperText="Enter the file ID received in your email"
            />

            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3 }}
              disabled={downloading}
              startIcon={downloading && <CircularProgress size={20} />}
            >
              {downloading ? 'Downloading...' : 'Download MP3'}
            </Button>
          </form>
        </Paper>
      </Box>
    </Container>
  );
}