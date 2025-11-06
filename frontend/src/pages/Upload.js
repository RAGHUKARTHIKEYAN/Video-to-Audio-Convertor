import React, { useState } from 'react';
import { Container, Paper, Button, Typography, Box, Alert, LinearProgress } from '@mui/material';
import { CloudUpload } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';

const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8080";

export default function Upload() {
  const navigate = useNavigate();
  const [file, setFile] = useState(null);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [uploading, setUploading] = useState(false);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile && selectedFile.type.startsWith('video/')) {
      setFile(selectedFile);
      setError('');
    } else {
      setFile(null);
      setError('Please select a valid video file');
    }
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) {
      setError('Please select a file to upload');
      return;
    }

    setUploading(true);
    setError('');
    setSuccess('');

    try {
      const formData = new FormData();
      formData.append('file', file);

      const res = await fetch(`${API_URL}/upload`, {
        method: 'POST',
        body: formData,
      });

      if (!res.ok) {
        const text = await res.text();
        throw new Error(text || 'Upload failed');
      }

      const text = await res.text();
      setSuccess('Upload successful! Check your email for the download ID.');
      setFile(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setUploading(false);
    }
  };

  return (
    <Container maxWidth="sm">
      <Box sx={{ mt: 8, mb: 4 }}>
        <Paper elevation={3} sx={{ p: 4 }}>
          <Typography variant="h4" component="h1" gutterBottom align="center">
            Upload Video
          </Typography>

          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}

          {success && (
            <Alert severity="success" sx={{ mb: 2 }}>
              {success}
            </Alert>
          )}

          <form onSubmit={handleUpload}>
            <Box
              sx={{
                border: '2px dashed #ccc',
                borderRadius: 2,
                p: 3,
                textAlign: 'center',
                mb: 2,
                cursor: 'pointer',
                '&:hover': {
                  borderColor: 'primary.main',
                },
              }}
              onClick={() => document.getElementById('file-input').click()}
            >
              <input
                id="file-input"
                type="file"
                accept="video/*"
                onChange={handleFileChange}
                style={{ display: 'none' }}
              />
              <CloudUpload sx={{ fontSize: 48, color: 'primary.main', mb: 1 }} />
              <Typography>
                {file ? file.name : 'Click to select a video file'}
              </Typography>
            </Box>

            {uploading && <LinearProgress sx={{ mb: 2 }} />}

            <Button
              type="submit"
              fullWidth
              variant="contained"
              disabled={!file || uploading}
            >
              {uploading ? 'Uploading...' : 'Upload Video'}
            </Button>
          </form>
        </Paper>
      </Box>
    </Container>
  );
}